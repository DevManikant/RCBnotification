High-Availability Inventory Monitoring Pipeline

I made this out of love for RCB match events. As it is nearly impossible to get notofication for RCB events and even if one get a notification, by the time we visit their website, it gets sold out within a minute. Thats why i build this solution.  

## ⚡ Core Architecture Features
* **Fast Checking:** The script polls the website's dom every 30 seconds, and checks if the particular text("Sold out", "Book Now") is available or not.
* **Logical Optimization:** If the script finds "Book Now" then it will send a notification on telegram every hour or if the script finds "Sold Out" it will send a notification every 6 hours that "Script is working".
* **Operational Security:** Zero hardcoded credentials. Fully integrates with platform environment variables (`os.environ`) for secret management.

