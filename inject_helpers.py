#!/usr/bin/env python3
"""
Helper: Inject strategies into the queue from command-line args.
Usage: python3 inject_helpers.py STRATEGY_JSON_1 [STRATEGY_JSON_2 ...]

Each arg is a compact strategy definition that gets expanded.
Format: "name|rationale|code"

The code should be a Python expression that, when evaluated, generates
5 candidate 23×23 ±1 matrices.

The script handles: imports, def generate_matrices() wrapper, validation.
"""
import json, sys
from pathlib import Path
import numpy as np

PROJECT_DIR = Path(__file__).parent
QUEUE_PATH = PROJECT_DIR / "strategy_queue.json"

if len(sys.argv) < 2:
    print("Usage: python3 inject_helpers.py 'id|rationale|code' [...]")
    sys.exit(1)

# Load existing queue
queue = json.loads(QUEUE_PATH.read_text())
existing_ids = {s["id"] for s in queue}

injected = 0
for arg in sys.argv[1:]:
    parts = arg.split("|", 2)
    if len(parts) != 3:
        print(f"SKIP: bad format '{arg[:50]}...'")
        continue
    
    sid, rationale, code = parts
    
    if sid in existing_ids:
        print(f"SKIP: {sid} already exists")
        continue
    
    # Wrap the code in a proper generate_matrices() function
    full_code = f"""
import numpy as np
from constructions import hadamard_24, paley_core

def generate_matrices():
    N = 23
    results = []
    {code}
    # Validate
    for m, name in results:
        assert m.shape == (23, 23), f'{{name}}: wrong shape {{m.shape}}'
        assert np.all(np.isin(m, [-1, 1])), f'{{name}}: invalid entries'
    return results[:5]
"""
    
    strategy = {
        "id": sid,
        "code": full_code,
        "rationale": rationale,
        "priority": 5,
        "created_by": "autonomous",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    }
    
    queue.append(strategy)
    existing_ids.add(sid)
    injected += 1
    print(f"INJECTED: {sid} — {rationale}")

QUEUE_PATH.write_text(json.dumps(queue, indent=2))
print(f"\nDone. {injected} new strategies. Queue: {len(queue)} total.")
