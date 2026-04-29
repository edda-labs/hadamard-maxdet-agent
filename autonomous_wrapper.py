#!/usr/bin/env python3
"""
Autonomous wrapper: Run one iteration, check strategy health, auto-kill stale strategies.
Called by the cron agent — this script does ALL the work in one terminal call.
"""
import json, sys, os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

# 1. Run the test iteration
os.chdir(PROJECT_DIR)
ret = os.system("python3 agent.py --iterations 1 2>&1")
exit_code = os.waitstatus_to_exitcode(ret) if hasattr(os, 'waitstatus_to_exitcode') else ret
print(f"[agent exit: {exit_code}]")

# 2. Read state
state = json.loads((PROJECT_DIR / "state.json").read_text())
queue = json.loads((PROJECT_DIR / "strategy_queue.json").read_text())

# 3. Count healthy strategies (not exhausted, not stale-dead)
available = [s for s in queue if s["attempts"] < 10 and s.get("stale_rounds", 0) < 5]
just_stale = [s for s in queue if s["attempts"] < 10 and s.get("stale_rounds", 0) >= 5]
exhausted = [s for s in queue if s["attempts"] >= 10]

# 4. Auto-kill strategies with stale_rounds >= 5
if just_stale:
    queue = [s for s in queue if s not in just_stale]
    with open(PROJECT_DIR / "strategy_queue.json", 'w') as f:
        json.dump(queue, f, indent=2)
    print(f"\n☠  AUTO-KILLED {len(just_stale)} stale strategies: {[s['id'] for s in just_stale]}")

print(f"\nStrategies: {len(available)} ACTIVE | {len(just_stale)} killed | {len(exhausted)} exhausted | {len(queue)} total")
print(f"Best det: {state['best_determinant']:,} ({state['best_determinant']/state['barba_bound']*100:.2f}% Barba)")
print(f"Iterations: {state['iterations_completed']} | Tested: {state['total_matrices_tested']}")

# 5. Check if injection needed
if len(available) < 3:
    print(f"\n⚠  Only {len(available)} strategies available — INJECTION REQUIRED.")
    (PROJECT_DIR / "INJECT_NEEDED.txt").write_text(
        f"Queue low: {len(available)} active. Total: {len(queue)}.\n"
        f"Please inject 3+ new strategies.\n"
    )
else:
    print(f"Queue healthy — {len(available)} active, no injection needed.")

print("\nDone.")
