# API Rate Limiter

A lightweight, educational implementation of an API Rate Limiting mechanism in Python.

This repository demonstrates the core logic behind tracking user request frequencies and enforcing limits. It serves as a foundational example of how rate limiters function before moving to complex, production-grade solutions like Redis or Nginx.

---

## 🚀 Features

* **Simple Request Tracking:** Tracks API usage by IP address.
* **JSON Persistence:** Stores user data in a local JSON file, ensuring data persists even if the script stops.
* **Automatic Cleanup:** Includes a background "Cleaner" thread that removes inactive IPs (stale data) to keep the data file small and efficient.
* **Configurable Limits:** (In code) limits users based on a time window and maximum attempt frequency.

## ⚠️ Disclaimer

> **Note:** This project is a **Proof of Concept (PoC)** and is **NOT intended for production environments.**

* **Performance:** Data is stored in a JSON file (`ips.json`). Every request involves Disk I/O (reading/writing the file), which is significantly slower than in-memory solutions (like Redis).
* **Scalability:** This implementation is designed to demonstrate logic, not to handle high-concurrency traffic.

## 🛠️ Usage

### Prerequisites
No external packages are required. This project uses standard Python libraries:
* `json`
* `datetime`
* `time`
* `threading`

### Example Code

```python
from rate_limiter import Api_Limit  
# 1. Initialize the Limiter
# This will create 'ips.json' if it doesn't exist
limiter = Api_Limit("ips.json")

# 2. Start the Background Cleaner (Optional)
# This removes IPs that haven't been active recently
limiter.ipcleaner(filename="ips.json", required=True)

# 3. Check a Request
user_ip = "192.168.1.50"
status = limiter.ratelimiter(user_ip, "ips.json")

if status == "Done":
    print("Request Allowed")
else:
    print(f"Rate Limit Exceeded: {status}")
```

    
⚙️ How it Works
The Check: When an IP requests access, the script calculates the time difference between the current request and the previous one.

The Decision:

If the user exceeds the frequency within the allowed time window, they are blocked, and a "Wait X seconds" message is returned.

If the time window has passed, the counter resets.

---

## 🛑 Final Warning

> [!CAUTION]
> **Data Integrity & Security:** This script writes directly to a JSON file on every request. In a real-world scenario, simultaneous requests from multiple users could lead to **Race Conditions** or **File Corruption**. 
> 
> For any project intended to handle real users, please migrate this logic to a memory-based store like **Redis** to ensure thread safety and high performance .



