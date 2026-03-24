import time
import random
from ARL import RateLimiter as Rl

if __name__ == "__main__":
    rl = Rl(filename="test_rate_limit", filetype="json")
    ip_count = 500
    test_ips = [f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(ip_count)]
    
    cooldown = 5
    allowed_freq = 3
    
    print("--- PHASE 1: Rapid Requests ---")
    for i in range(12):
        current_ip = random.choice(test_ips)
        is_allowed = rl.API_RL(
            IP_Adrs=current_ip, 
            CooldownTime=cooldown, 
            AllowedFreq=allowed_freq,
            Cleaning=False
        )
        status = "ALLOWED" if is_allowed else "BLOCKED"
        print(f"Req {i+1:02d} | IP: {current_ip:<15} | Result: {status}")
        time.sleep(0.3)

    wait_time = cooldown + 1
    print(f"\n--- PHASE 2: Waiting {wait_time}s for Cooldown ---")
    time.sleep(wait_time)

    print("\n--- PHASE 3: Post-Cooldown Verification ---")
    for i in range(5):
        current_ip = random.choice(test_ips)
        is_allowed = rl.API_RL(
            IP_Adrs=current_ip, 
            CooldownTime=cooldown, 
            AllowedFreq=allowed_freq,
            Cleaning=False
        )
        status = "ALLOWED" if is_allowed else "BLOCKED"
        print(f"Req {i+13:02d} | IP: {current_ip:<15} | Result: {status}")
        time.sleep(0.3)