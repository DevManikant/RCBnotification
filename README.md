High-Availability Inventory Monitoring Pipeline

An event-driven, serverless data pipeline built on Azure Functions designed to execute high-frequency state polling, real-time change detection, and automated telemetry alerts. 

## ⚡ Core Architecture Features
* **Stateless Checking:** Implements local, isolated file caching to calculate volumetric state changes between polling cycles, suppressing redundant downstream alert traffic.
* **Network Optimization:** Enforces strict execution timeouts (10s/15s boundaries) to prevent hanging concurrent asynchronous worker threads.
* **Operational Security:** Zero hardcoded credentials. Fully integrates with platform environment variables (`os.environ`) for secret management.

