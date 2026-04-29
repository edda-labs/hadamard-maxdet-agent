"""
Strategy injection — allows Hermod (the main agent) to inject new search strategies
into the autonomous Hadamard research agent.

Format: JSON array of strategy objects.
Each strategy has:
  - "id": unique identifier
  - "code": Python code to execute that generates candidate matrices
  - "rationale": human-readable explanation
  - "priority": higher = executed first
  - "created_by": who injected this strategy
  - "attempts": how many times tried
  - "best_det": best determinant from this strategy
"""

import json
import os
from pathlib import Path

QUEUE_PATH = Path(__file__).parent / "strategy_queue.json"


def load_strategies() -> list[dict]:
    """Load the strategy queue."""
    if QUEUE_PATH.exists():
        with open(QUEUE_PATH) as f:
            return json.load(f)
    return []


def save_strategies(strategies: list[dict]) -> None:
    """Save the strategy queue."""
    with open(QUEUE_PATH, "w") as f:
        json.dump(strategies, f, indent=2)


def add_strategy(code: str, rationale: str, created_by: str = "hermod",
                 priority: int = 5) -> str:
    """Add a new strategy. Returns the strategy ID."""
    import uuid
    strategies = load_strategies()

    strategy = {
        "id": uuid.uuid4().hex[:8],
        "code": code,
        "rationale": rationale,
        "priority": priority,
        "created_by": created_by,
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    }

    strategies.append(strategy)
    strategies.sort(key=lambda s: s["priority"], reverse=True)
    save_strategies(strategies)
    return strategy["id"]


def get_next_strategy(state_best_det: int = 0) -> dict | None:
    """Get the best strategy considering priority + penalty for staleness.
    
    Penalty: If a strategy produced the SAME best_det for 3+ attempts
    (matches the global state_best_det), its effective priority is halved.
    Strategies that found NEW records get a bonus.
    Crash penalty: strategies that error 3+ times in a row get demoted."""
    strategies = load_strategies()
    available = [s for s in strategies if s["attempts"] < 10]
    if not available:
        return None
    
    # Apply penalty/bonus to priorities
    for s in available:
        eff_priority = s["priority"]
        stale = s.get("stale_rounds", 0)
        last_best = s.get("last_best_det", 0)
        crash_count = s.get("crash_count", 0)
        crash_streak = s.get("crash_streak", 0)
        
        # CRASH PENALTY: repeated errors → demote hard
        if crash_streak >= 5:
            eff_priority = -2  # dead
        elif crash_streak >= 3:
            eff_priority = max(-1, eff_priority - 6)  # severe demotion
        elif crash_count >= 5:
            eff_priority = max(0, eff_priority - 3)  # persistent failures
        
        # PENALTY: stale -> priority decay
        if stale >= 5:
            eff_priority = -1  # kill it
        elif stale >= 3:
            eff_priority = max(0, eff_priority - 4)
        elif stale >= 1:
            eff_priority = max(0, eff_priority - 1)
        
        # BONUS: produced a best above global best
        if last_best > state_best_det and state_best_det > 0:
            eff_priority = min(10, eff_priority + 3)
        
        # BONUS: unexplored strategies (only if hasn't crashed yet)
        if s["attempts"] == 0 and crash_streak == 0:
            eff_priority += 1
        
        s["_eff_priority"] = eff_priority
    
    available.sort(key=lambda s: (s["_eff_priority"], s["priority"]), reverse=True)
    return available[0]


def record_error(strategy_id: str, error_msg: str) -> None:
    """Record that a strategy execution failed (crash/exception).
    
    Tracks crash streak and total crash count for penalty calculation.
    Consecutive crashes increase penalty; a successful run resets the streak."""
    strategies = load_strategies()
    for s in strategies:
        if s["id"] == strategy_id:
            s.setdefault("crash_count", 0)
            s.setdefault("crash_streak", 0)
            s["crash_count"] += 1
            s["crash_streak"] += 1
            s.setdefault("last_error", "")
            s["last_error"] = error_msg[:200]
            break
    save_strategies(strategies)


def record_attempt(strategy_id: str, det_abs: int, name: str) -> None:
    """Record that a strategy was attempted with a given result.
    
    Now tracks staleness: if a strategy produces a determinant that
    doesn't improve over its own best, increment stale_rounds.
    Resets crash_streak on successful execution."""
    strategies = load_strategies()
    for s in strategies:
        if s["id"] == strategy_id:
            s["attempts"] += 1
            
            # Initialize penalty fields
            s.setdefault("stale_rounds", 0)
            s.setdefault("consecutive_duplicates", 0)
            s.setdefault("last_best_det", 0)
            
            # Reset crash streak on success
            s["crash_streak"] = 0
            
            if det_abs > s["best_det"]:
                s["best_det"] = det_abs
                s["best_name"] = name
                s["stale_rounds"] = 0  # RESET on improvement!
                s["consecutive_duplicates"] = 0
            else:
                s["consecutive_duplicates"] += 1
                s["stale_rounds"] += 1
            
            s["last_best_det"] = det_abs
            break
    save_strategies(strategies)


def clear_queue() -> None:
    """Clear all strategies."""
    save_strategies([])


# Default seed strategies
SEED_STRATEGIES = [
    {
        "id": "seed_local_flip",
        "code": """
# Local search: flip individual entries in best known matrix
# Start from the H24-submatrix deletion approach but try sign perturbations
import numpy as np
from constructions import hadamard_24

def generate_matrices():
    H24 = hadamard_24()
    results = []

    # Try different row/col deletions as base
    for idx, (r, c) in enumerate([(0, 0), (5, 7), (11, 13), (17, 19), (23, 1)]):
        M = np.delete(np.delete(H24, r, axis=0), c, axis=1).astype(np.int8)

        # Flip strategic entries: corners and center
        M_flipped = M.copy()
        # Flip corners
        M_flipped[0, 0] *= -1
        M_flipped[0, 22] *= -1
        M_flipped[22, 0] *= -1
        M_flipped[22, 22] *= -1
        # Flip some diagonal entries
        for i in [5, 11, 17]:
            M_flipped[i, i] *= -1
        results.append((M_flipped, f"local_search_corners_r{r}_c{c}"))

        if len(results) >= 5:
            break
    return results
""",
        "rationale": "Local perturbation of best known Hadamard submatrices — flip strategic entries",
        "priority": 8,
        "created_by": "seed",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "seed_conference_border",
        "code": """
# Build from Paley conference-like core with border variations
import numpy as np
from constructions import paley_core

def generate_matrices():
    Q = paley_core(23)  # 23x23 Paley core (skew-symmetric)
    results = []

    # Strategy 1: Direct Paley core with various diagonals
    for diag_pattern in range(5):
        M = Q.copy().astype(np.int8)
        # Different diagonal patterns
        if diag_pattern == 0:
            np.fill_diagonal(M, 1)
        elif diag_pattern == 1:
            np.fill_diagonal(M, -1)
        elif diag_pattern == 2:
            M[np.arange(23), np.arange(23)] = np.where(np.arange(23) % 2 == 0, 1, -1)
        elif diag_pattern == 3:
            M[np.arange(23), np.arange(23)] = np.where(np.arange(23) % 3 == 0, 1, -1)
        else:
            # All zeros on diagonal (not ±1! fix below)
            np.fill_diagonal(M, 1)

        results.append((M, f'paley_diag_{diag_pattern}'))

    return results[:5]
""",
        "rationale": "Use Paley core (23x23) directly with various diagonal patterns",
        "priority": 6,
        "created_by": "seed",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "seed_negacyclic_family",
        "code": """
# Negacyclic matrices: each row is negative of previous row shifted
# Variation: try different first rows
import numpy as np

def generate_matrices():
    N = 23
    rng = np.random.RandomState(42)
    results = []

    for i in range(5):
        # Generate first row with specific patterns
        if i == 0:
            first_row = np.ones(N, dtype=np.int8)
        elif i == 1:
            first_row = np.array([1, -1] * 11 + [1], dtype=np.int8)
        elif i == 2:
            first_row = np.where(np.arange(N) % 2 == 0, 1, -1).astype(np.int8)
        elif i == 3:
            first_row = rng.choice([-1, 1], size=N).astype(np.int8)
        else:
            # Alternating blocks of 3
            first_row = np.tile(np.array([1, 1, -1], dtype=np.int8), 8)[:N]

        M = np.zeros((N, N), dtype=np.int8)
        M[0] = first_row
        for r in range(1, N):
            M[r, 0] = -M[r-1, N-1]
            M[r, 1:] = -M[r-1, :-1]

        results.append((M, f'negacyclic_v{i}'))

    return results
""",
        "rationale": "Negacyclic matrices with structural first-row patterns",
        "priority": 5,
        "created_by": "seed",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "seed_kronecker_product",
        "code": """
# Kronecker product approach: 23 is prime, but try near-factorizations
# 23 = 22 + 1 or use bordering techniques
import numpy as np

def generate_matrices():
    N = 23
    results = []

    # Strategy: Build 11x11 structured blocks + 1 border
    for seed in range(5):
        rng = np.random.RandomState(100 + seed)

        # Build 11x11 block matrix
        A = rng.choice([-1, 1], size=(11, 11)).astype(np.int8)
        B = rng.choice([-1, 1], size=(11, 12)).astype(np.int8)
        C = rng.choice([-1, 1], size=(12, 11)).astype(np.int8)
        D = rng.choice([-1, 1], size=(12, 12)).astype(np.int8)

        # Assemble 23x23 = 11+12
        M = np.zeros((N, N), dtype=np.int8)
        M[:11, :11] = A
        M[:11, 11:] = B
        M[11:, :11] = C
        M[11:, 11:] = D

        results.append((M, f'block_11_12_s{seed}'))

    return results
""",
        "rationale": "Block matrix construction: 23 = 11+12 split",
        "priority": 4,
        "created_by": "seed",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "seed_symmetric_toeplitz",
        "code": """
# Symmetric Toeplitz matrices: entries depend only on |i-j|
import numpy as np

def generate_matrices():
    N = 23
    results = []

    for i in range(5):
        rng = np.random.RandomState(200 + i)
        # Generate the first row (defines the whole matrix)
        first_row = rng.choice([-1, 1], size=N).astype(np.int8)

        # Build symmetric Toeplitz
        M = np.zeros((N, N), dtype=np.int8)
        for r in range(N):
            for c in range(N):
                M[r, c] = first_row[abs(r - c)]

        results.append((M, f'sym_toeplitz_{i}'))

    return results
""",
        "rationale": "Symmetric Toeplitz — highly structured, depends on only 23 values",
        "priority": 4,
        "created_by": "seed",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
]


def init_seed_strategies():
    """Initialize strategy queue with seed strategies if empty."""
    strategies = load_strategies()
    if not strategies:
        save_strategies(SEED_STRATEGIES)
        print(f"  [STRATEGY] Initialized {len(SEED_STRATEGIES)} seed strategies")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init_seed_strategies()
        print(f"  [STRATEGY] Queue has {len(load_strategies())} strategies")
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        strategies = load_strategies()
        for s in strategies:
            print(f"  [{s['id']}] priority={s['priority']} attempts={s['attempts']} best={s['best_det']:,} — {s['rationale']}")
    else:
        print("Usage: strategy_queue.py [init|list]")
