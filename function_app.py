import azure.functions as func
import requests
import logging
import os
import time
from datetime import datetime

app = func.FunctionApp()

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8788567376:AAGjmuyDnVBE0TXHtGqD5Bl0W65eFO96skg"
CHAT_ID = "1124894577"
API_URL = "https://rcbscaleapi.ticketgenie.in/ticket/eventlist/O"

def send_telegram(msg):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(api_url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        logging.error(f"Telegram failed: {e}")

@app.timer_trigger(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=True)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    now = datetime.now()
    
    # Every 6 Hours
    if now.hour % 6 == 0 and now.minute == 0:
        send_telegram("⏱️ Heartbeat: Tokenless API bot is monitoring perfectly.")

    # READ CACHE
    cache_file = "/tmp/api_state.txt"
    last_time = 0.0
    last_count = 0
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                data = f.read().strip().split(",")
                if len(data) == 2:
                    last_time, last_count = float(data[0]), int(data[1])
        except Exception: 
            pass

    # PING API
    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://shop.royalchallengers.com',
        'referer': 'https://shop.royalchallengers.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        res_data = response.json()
        
        matches = res_data.get("result", [])
        current_count = len(matches)
        current_time = time.time()

        if current_count > 0:
            
            if current_count > last_count:
                match_details = ""
                for m in matches:
                    name = m.get("event_Name", "Unknown Match")
                    price = m.get("event_Price_Range", "N/A")
                    match_details += f"🏏 {name}\n💰 {price}\n\n"

                msg = f"🚀 TICKETS ARE LIVE! 🚀\n\n{match_details}🎟️ Buy: https://shop.royalchallengers.com/ticket"
                send_telegram(msg)
                with open(cache_file, "w") as f:
                    f.write(f"{current_time},{current_count}")

            # sold out
            elif current_count < last_count:
                logging.info(f"Match count dropped from {last_count} to {current_count}.")
                with open(cache_file, "w") as f:
                    f.write(f"{last_time},{current_count}")

            # Hourly Reminder
            elif current_time - last_time >= 3600:
                send_telegram(f"🟢 REMINDER: {current_count} match(es) are still live!\n\n🎟️ https://shop.royalchallengers.com/ticket")
                with open(cache_file, "w") as f:
                    f.write(f"{current_time},{current_count}")
            
            else:
                logging.info("Tickets live. Cooldown active.")

        else:
            logging.info("API result is empty. Site is locked.")
            if last_count != 0:
                with open(cache_file, "w") as f:
                    f.write(f"{current_time},0")

    except Exception as e:
        logging.error(f"API Check failed: {e}")