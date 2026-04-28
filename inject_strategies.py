#!/usr/bin/env python3
"""Inject new strategies into the queue."""
import json
import importlib.util
import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the strategy queue module
from strategy_queue import load_strategies, save_strategies

# Load new strategies
spec = importlib.util.spec_from_file_location('ns', 'new_strategies.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

existing = load_strategies()

# Mark exhausted strategies (10+ attempts)
# Check construction_stats from state.json for actual best dets
try:
    with open('state.json') as f:
        state = json.load(f)
    cs = state.get('construction_stats', {})
except:
    cs = {}

exhausted = 0
for s in existing:
    strat_key = f"strategy_{s['id']}"
    # Check if this strategy has actual results in construction_stats
    actual_best = cs.get(strat_key, {}).get('best_det', 0)
    if actual_best > 0:
        s['best_det'] = actual_best
    
    if s['attempts'] >= 10:
        if s['best_det'] == 0:
            s['attempts'] = 99  # mark as done
            print(f"  [EXHAUSTED] {s['id']} — {s['attempts']} attempts, no improvement")
            exhausted += 1
        else:
            print(f"  [KEEPING] {s['id']} — {s['attempts']} attempts, best={s['best_det']:,}")

# Add new strategies (dedup by id)
new_ids = {s['id'] for s in existing}
added = 0
for s in mod.SEED_STRATEGIES:
    if s['id'] not in new_ids:
        existing.append(s)
        new_ids.add(s['id'])
        added += 1
        print(f"  + ADDED: {s['id']} (p={s['priority']}) — {s['rationale'][:80]}")

save_strategies(existing)
print(f"\nQueue: {len(existing)} total ({added} new, {exhausted} exhausted)")

# Show summary
print("\n" + "="*80)
print(f"{'Status':6s} {'Strategy ID':35s} {'P':>2s} {'Att':>4s} {'Best Det':>22s}")
print("-"*80)
for s in sorted(existing, key=lambda x: (-x['priority'], x['attempts'])):
    tag = 'ACTIVE' if s['attempts'] < 10 else ('DONE' if s['attempts'] >= 99 else 'FULL')
    best_str = f"{s['best_det']:,}" if s['best_det'] else "0"
    print(f"  [{tag}]  {s['id']:32s} {s['priority']:>2d} {s['attempts']:>4d} {best_str:>22s}")
