"""
Optimized Multi-Threaded Rate Limiter Tester
Tests ARL.RateLimiter at scale (~100k users) using thread pools.
"""

import time
import random
import string
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional
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
# ── Config ──────────────────────────────────────────────────────────────────

@dataclass
class TestConfig:
    total_users:    int   = 100_000   # unique user IDs to simulate
    rounds:         int   = 100       # outer rounds
    sample_size:    int   = 1_000     # IDs in each round's sample
    max_workers:    int   = 64        # thread-pool size
    cleaning_freq:  int   = 17        # passed to API_RL
    fail_threshold: int   = 100       # pause after this many failures/batch
    fail_sleep:     float = 8.0       # seconds to sleep on threshold hit
    round_sleep:    float = 1.0       # seconds between rounds
    seed:           int   = 42        # RNG seed for reproducibility
    verbose:        bool  = True      # per-round console output

# ── Thread-safe counters ─────────────────────────────────────────────────────

class AtomicCounters:
    def __init__(self):
        self._lock  = threading.Lock()
        self.succ   = 0
        self.fail   = 0
        self.total  = 0

    def record(self, value: int):
        with self._lock:
            self.total += 1
            if value == 1:
                self.succ += 1
            else:
                self.fail += 1

    def snapshot(self) -> dict:
        with self._lock:
            return {"succ": self.succ, "fail": self.fail, "total": self.total}

    def reset(self):
        with self._lock:
            self.succ = self.fail = self.total = 0

# ── Worker ───────────────────────────────────────────────────────────────────

def _call_api(rl: Rl, ip: str, cleaning_freq: int) -> int:
    """Single API call; returns 1 on success, 0 on failure."""
    try:
        return rl(IP_Adrs=ip, Cleaning=False, CleaningFreq=cleaning_freq)
    except Exception:
        return 0

# ── Core runner ───────────────────────────────────────────────────────────────

def run_test(cfg: TestConfig = TestConfig()) -> dict:
    rng    = random.Random(cfg.seed)
    totals = AtomicCounters()

    # Pre-generate the full user pool once
    pool = [
        ''.join(rng.choices(string.ascii_letters, k=15))
        for _ in range(cfg.total_users)
    ]

    grand: dict = defaultdict(int)
    count = 0

    for round_idx in range(cfg.rounds):
        sample  = rng.sample(pool, min(cfg.sample_size, len(pool)))
        totals.reset()
        futures = {}

        with ThreadPoolExecutor(max_workers=cfg.max_workers) as exe:
            for user in sample:
                count += 1
                ip = f"{user}{count}"
                fut = exe.submit(_call_api, Rl, ip, cfg.cleaning_freq)
                futures[fut] = ip

            batch_fail = 0
            for fut in as_completed(futures):
                val = fut.result()
                totals.record(val)
                if val != 1:
                    batch_fail += 1

        snap = totals.snapshot()
        grand["succ"]  += snap["succ"]
        grand["fail"]  += snap["fail"]
        grand["total"] += snap["total"]

        if cfg.verbose:
            sr = snap["succ"] / snap["total"] * 100 if snap["total"] else 0
            print(
                f"[Round {round_idx + 1:>4}/{cfg.rounds}] "
                f"✓ {snap['succ']:>6}  ✗ {snap['fail']:>6}  "
                f"total {snap['total']:>6}  success-rate {sr:.1f}%"
            )

        if batch_fail >= cfg.fail_threshold:
            if cfg.verbose:
                print(f"  ⚠  failure threshold hit – sleeping {cfg.fail_sleep}s")
            time.sleep(cfg.fail_sleep)

        time.sleep(cfg.round_sleep)

    # Final summary
    grand["success_rate_pct"] = (
        grand["succ"] / grand["total"] * 100 if grand["total"] else 0
    )
    return dict(grand)

# ── CLI entry-point ───────────────────────────────────────────────────────────

def _parse_args() -> TestConfig:
    p = argparse.ArgumentParser(description="ARL RateLimiter stress-tester")
    p.add_argument("--users",      type=int,   default=100_000)
    p.add_argument("--rounds",     type=int,   default=100)
    p.add_argument("--sample",     type=int,   default=1_000)
    p.add_argument("--workers",    type=int,   default=64)
    # p.add_argument("--clean-freq", type=int,   default=17)
    p.add_argument("--fail-thr",   type=int,   default=100)
    p.add_argument("--fail-sleep", type=float, default=8.0)
    p.add_argument("--round-sleep",type=float, default=1.0)
    p.add_argument("--seed",       type=int,   default=42)
    p.add_argument("--quiet",      action="store_true")
    a = p.parse_args()

    return TestConfig(
        total_users    = a.users,
        rounds         = a.rounds,
        sample_size    = a.sample,
        max_workers    = a.workers,
        # cleaning_freq  = a.clean_freq,
        fail_threshold = a.fail_thr,
        fail_sleep     = a.fail_sleep,
        round_sleep    = a.round_sleep,
        seed           = a.seed,
        verbose        = not a.quiet,
    )

if __name__ == "__main__":

    cfg = _parse_args()

    print("=" * 60)
    print("  ARL Rate Limiter – Multi-Threaded Stress Test")
    print("=" * 60)
    print(f"  Users      : {cfg.total_users:,}")
    print(f"  Rounds     : {cfg.rounds}")
    print(f"  Sample/rnd : {cfg.sample_size}")
    print(f"  Workers    : {cfg.max_workers}")
    print("=" * 60)

    t0     = time.perf_counter()
    result = run_test(cfg)
    elapsed = time.perf_counter() - t0

    print()
    print("=" * 60)
    print("  FINAL RESULTS")
    print("=" * 60)
    print(f"  Total calls  : {result['total']:,}")
    print(f"  Successes    : {result['succ']:,}")
    print(f"  Failures     : {result['fail']:,}")
    print(f"  Success rate : {result['success_rate_pct']:.2f}%")
    print(f"  Wall time    : {elapsed:.1f}s")
    print(f"  Throughput   : {result['total'] / elapsed:,.0f} calls/s")
    print("=" * 60)