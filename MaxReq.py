import time
import random
import concurrent.futures
Chance=3
while Chance:
    select=int(input("Select 1 for Json \nSelect 2 for SQL Lite:"))
    if(select==1):
            from ARL import Ratelimiter as Rl
            break
    elif (select==2):
            from ARL_sql import Ratelimiter as Rl
            break
    else:
        print("Select Propely")
        Chance=Chance-1
if Chance==0:
    exit()    

def simulate_request(rl, ip_pool, cooldown, allowed_freq):
    ip = random.choice(ip_pool)
    is_allowed = Rl(
        IP_Adrs=ip, 
        CooldownTime=cooldown, 
        AllowedFreq=allowed_freq,
        Cleaning=False
    )
    return ip, is_allowed

if __name__ == "__main__":
    
  
    total_requests = 1000
    ip_count = 10
    cooldown = 20
    allowed_freq = 5
    max_workers = 20 
    
    test_ips = [f"{random.randint(1, 254)}.{random.randint(1, 254)}.1.1" for _ in range(ip_count)]
    
    print(f"--- STRESS TEST: {total_requests} Requests | {max_workers} Concurrent Threads ---")
    start_time = time.perf_counter()
    
    results = {"ALLOWED": 0, "BLOCKED": 0}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(simulate_request,Rl, test_ips, cooldown, allowed_freq) for _ in range(total_requests)]
        
        for future in concurrent.futures.as_completed(futures):
            _, is_allowed = future.result()
            if is_allowed:
                results["ALLOWED"] += 1
            else:
                results["BLOCKED"] += 1

    end_time = time.perf_counter()
    
    print(f"Finished in {end_time - start_time:.2f} seconds")
    print(f"Total Allowed: {results['ALLOWED']}")
    print(f"Total Blocked: {results['BLOCKED']}")
    print(f"Expected Max Allowed: ~{ip_count * allowed_freq}")
    print("-" * 50)
    print("Check 'stress_test_limit.json' to ensure it is valid and not corrupted.")