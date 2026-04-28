#!/usr/bin/env python3
"""
Autonomous wrapper: Run one iteration, check if strategies needed, inject if so.
Called by the cron agent — this script does ALL the work in one terminal call.
"""
import json, sys, os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

# 1. Run the test iteration
os.chdir(PROJECT_DIR)
ret = os.system("python3 agent.py --iterations 1 2>&1")
print(f"[agent exit: {os.waitstatus_to_exitcode(ret) if hasattr(os, 'waitstatus_to_exitcode') else ret}]")

# 2. Read state
state = json.loads((PROJECT_DIR / "state.json").read_text())
queue = json.loads((PROJECT_DIR / "strategy_queue.json").read_text())

available = [s for s in queue if s["attempts"] < 10]
print(f"\nStrategies: {len(available)} available, {len(queue)} total")
print(f"Best det: {state['best_determinant']:,} ({state['best_determinant']/state['barba_bound']*100:.2f}% Barba)")

# 3. Check if injection needed
if len(available) >= 3:
    print("Queue sufficient — no injection needed.")
else:
    print(f"Only {len(available)} strategies left — INJECTION REQUIRED.")
    print("Write new strategies to ~/.hermes/hadamard-research/INJECT_NEEDED.txt")
    # Signal that injection is needed
    (PROJECT_DIR / "INJECT_NEEDED.txt").write_text(
        f"Queue low: {len(available)} strategies available, {len(queue)} total.\n"
        f"Please inject 3+ new strategies into strategy_queue.json\n"
    )

print("\nDone.")
