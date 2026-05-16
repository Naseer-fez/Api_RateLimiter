import os
import time
import json
import psutil
import threading
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures
from datetime import datetime

# Import the actual Rate Limiter
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
# Output directories
GRAPH_DIR = os.path.join("benchmark_results", "graphs", "real")
LOG_DIR = os.path.join("benchmark_results", "logs", "real")
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.family": "serif", "font.size": 11, "figure.dpi": 200})

def save(fig, name):
    path = os.path.join(GRAPH_DIR, f"{name}.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  Saved {path}")

def clean_data_file():
    """Ensure we start fresh for each test"""
    try:
        if os.path.exists("real_benchmark.json"):
            os.remove("real_benchmark.json")
    except Exception:
        pass

# ── 1. Response Time vs Concurrent Users (REAL) ─────────────────────────
def run_response_time_benchmark():
    print("  Running Response Time vs Users benchmark...")
    users_arr = [1, 5, 10, 20, 50, 100] # Kept smaller to avoid crashing python instantly
    mean_rt, p95_rt, p99_rt = [], [], []
    
    for users in users_arr:
        clean_data_file()
        latencies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
            def worker():
                t0 = time.perf_counter()
                Ratelimiter("192.168.1.1", False, 20, 1000, 80, 8, Filename="app", FileType="json")
                return time.perf_counter() - t0
            
            # Submit enough requests to get a good sample
            futures = [executor.submit(worker) for _ in range(users * 5)]
            for future in concurrent.futures.as_completed(futures):
                latencies.append(future.result())
                
        latencies = np.array(latencies) * 1000 # convert to ms
        mean_rt.append(np.mean(latencies))
        p95_rt.append(np.percentile(latencies, 95))
        p99_rt.append(np.percentile(latencies, 99))
        
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(users_arr, mean_rt, "o-", label="Mean", color="#2563eb")
    ax.plot(users_arr, p95_rt, "s--", label="P95", color="#f59e0b")
    ax.plot(users_arr, p99_rt, "^:", label="P99", color="#ef4444")
    ax.set(xlabel="Concurrent Threads", ylabel="Response Time (ms)",
           title="Real Benchmark: Response Time vs Concurrent Users")
    ax.set_xscale("log"); ax.legend(); ax.grid(True, alpha=0.3)
    save(fig, "real_response_time_vs_users")

# ── 2. Throughput vs Load (REAL) ────────────────────────────────────────
def run_throughput_benchmark():
    print("  Running Throughput vs Load benchmark...")
    load_arr = [10, 50, 100, 200, 500]
    throughput_arr = []
    
    for load in load_arr:
        clean_data_file()
        # We try to send 'load' requests in exactly 1 second using threading
        t_start = time.perf_counter()
        completed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(64, load)) as executor:
            futures = [executor.submit(Ratelimiter, f"10.0.0.{i%20}", False, 20, 1000, 80, 8, "app", None, "json") for i in range(load)]
            for future in concurrent.futures.as_completed(futures):
                future.result()
                completed += 1
                
        t_end = time.perf_counter()
        elapsed = t_end - t_start
        throughput_arr.append(completed / elapsed)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(load_arr, throughput_arr, "o-", color="#059669", linewidth=2, markersize=5)
    ax.fill_between(load_arr, np.array(throughput_arr)*0.9, np.array(throughput_arr)*1.1, alpha=0.1, color="#059669")
    ax.set(xlabel="Target Load (req/s)", ylabel="Actual Throughput (req/s)",
           title="Real Benchmark: System Throughput vs Target Load")
    ax.grid(True, alpha=0.3)
    save(fig, "real_throughput_vs_load")

# ── 3. Allowed vs Blocked (REAL) ──────────────────────────────
def run_allowed_vs_blocked():
    print("  Running Allowed vs Blocked benchmark...")
    clean_data_file()
    
    ips = [f"Client {i+1}" for i in range(5)]
    allowed = []
    blocked = []
    
    # We send exactly 15 requests per IP. Allowed limit is 8.
    for i, ip_label in enumerate(ips):
        ip = f"172.16.0.{i+1}"
        a, b = 0, 0
        for _ in range(15):
            res = Ratelimiter(ip, False, 20, 8, 80, 8, Filename="app", FileType="json")
            if res == 1:
                a += 1
            else:
                b += 1
        allowed.append(a)
        blocked.append(b)

    x = np.arange(len(ips))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - 0.2, allowed, 0.4, label="Allowed", color="#22c55e")
    ax.bar(x + 0.2, blocked, 0.4, label="Blocked", color="#ef4444")
    ax.set(xlabel="Client IP", ylabel="Request Count",
           title="Real Benchmark: Allowed vs Blocked Requests (Limit=8)")
    ax.set_xticks(x); ax.set_xticklabels(ips, rotation=30)
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    save(fig, "real_allowed_vs_blocked")

# ── 4. Validation Latency Distribution (REAL) ────────────────────────────────
def run_validation_latency():
    print("  Running Validation Latency benchmark...")
    clean_data_file()
    latencies = []
    
    for i in range(500):
        t0 = time.perf_counter()
        Ratelimiter(f"192.168.2.{i%50}", False, 20, 1000, 80, 8, Filename="app", FileType="json")
        latencies.append((time.perf_counter() - t0) * 1000)
        
    latencies = np.array(latencies)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(latencies, bins=50, color="#0ea5e9", edgecolor="white", alpha=0.85)
    ax.axvline(np.median(latencies), color="#ef4444", linestyle="--", label=f"Median: {np.median(latencies):.2f} ms")
    ax.axvline(np.percentile(latencies, 95), color="#f59e0b", linestyle="--", label=f"P95: {np.percentile(latencies,95):.2f} ms")
    ax.set(xlabel="Latency (ms)", ylabel="Frequency",
           title="Real Benchmark: Request Validation Latency Distribution")
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    save(fig, "real_validation_latency")

# ── 5. CPU & Memory Usage (REAL) ───────────────────────────────────────
def run_system_metrics():
    print("  Running CPU/Memory Usage benchmark...")
    clean_data_file()
    
    cpu_usage = []
    mem_usage = []
    times = []
    
    process = psutil.Process(os.getpid())
    t0 = time.time()
    
    # Background thread to record metrics
    stop_metrics = False
    def record_metrics():
        while not stop_metrics:
            cpu_usage.append(process.cpu_percent(interval=0.1))
            mem_usage.append(process.memory_info().rss / (1024 * 1024))
            times.append(time.time() - t0)
            
    metrics_thread = threading.Thread(target=record_metrics)
    metrics_thread.start()
    
    # Generate load
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(Ratelimiter, f"10.1.1.{i%100}", False, 20, 1000, 80, 8, "app", None, "json") for i in range(1000)]
        concurrent.futures.wait(futures)
        
    stop_metrics = True
    metrics_thread.join()
    
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.plot(times, cpu_usage, color="#ef4444", label="CPU (%)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("CPU Usage (%)", color="#ef4444")
    
    ax2 = ax1.twinx()
    ax2.plot(times, mem_usage, color="#3b82f6", label="Memory (MB)")
    ax2.set_ylabel("Memory (MB)", color="#3b82f6")
    
    fig.suptitle("Real Benchmark: System Resource Usage Under Load")
    fig.tight_layout()
    save(fig, "real_system_metrics")

# ── 6. Persistence File Size Growth (REAL) ─────────────────────
def run_persistence_size():
    print("  Running Persistence Size benchmark...")
    clean_data_file()
    
    entries = [10, 50, 100, 500, 1000]
    file_kb = []
    
    for count in entries:
        for i in range(count):
            Ratelimiter(f"10.2.0.{i}", False, 20, 1000, 80, 8, Filename="app", FileType="json")
        size = os.path.getsize("real_benchmark.json") / 1024
        file_kb.append(size)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(len(entries)), file_kb, color="#8b5cf6", edgecolor="white")
    ax.set_xticks(range(len(entries))); ax.set_xticklabels(entries)
    ax.set(xlabel="Number of Tracked IPs", ylabel="JSON File Size (KB)",
           title="Real Benchmark: Persistence File Size Growth")
    ax.grid(axis="y", alpha=0.3)
    save(fig, "real_persistence_size")

if __name__ == "__main__":
    print(f"Generating Real Benchmark Graphs to {GRAPH_DIR}")
    run_response_time_benchmark()
    run_throughput_benchmark()
    run_allowed_vs_blocked()
    run_validation_latency()
    run_system_metrics()
    run_persistence_size()
    clean_data_file()
    print("All real benchmarks complete!")
