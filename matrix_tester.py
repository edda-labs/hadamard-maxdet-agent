"""
matrix_tester.py — Verify determinants of candidate {±1} matrices for order 23.

Reference: OEIS A003432 / A003433
- g(n) = max |det| for n×n {±1} matrix
- g(n) = 2^(n-1) * a(n-1) where a(n-1) is max det of (n-1)×(n-1) {0,1} matrix
- For n=23 (odd, 23 ≡ 3 mod 4): Barba bound is not attainable.
  Upper bound: sqrt(45) * 22^11 ≈ 6.708 * 22^11
  Best known: 2^22 * 662_671_875 (from a(22) uncertain value)
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional
import hashlib
import json
import os

N = 23


def integer_det(matrix: np.ndarray) -> int:
    """Exact determinant for integer matrices via Bareiss (fraction-free LU).

    np.linalg.det uses float64 LU; for 23x23 ±1 matrices the true |det| sits
    around 10^15, right at float64's ~16-digit boundary, so identical matrices
    can return values that differ by tens of ULPs. That breaks equality-based
    stagnation checks and lets noise reset staleness counters. Bareiss is exact
    in Python big-int and runs in milliseconds at this size.
    """
    n = matrix.shape[0]
    A = [[int(matrix[i, j]) for j in range(n)] for i in range(n)]
    sign = 1
    prev = 1
    for i in range(n - 1):
        if A[i][i] == 0:
            pivot = -1
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    pivot = k
                    break
            if pivot < 0:
                return 0
            A[i], A[pivot] = A[pivot], A[i]
            sign = -sign
        for j in range(i + 1, n):
            for k in range(i + 1, n):
                A[j][k] = (A[j][k] * A[i][i] - A[j][i] * A[i][k]) // prev
            A[j][i] = 0
        prev = A[i][i]
    return sign * A[n - 1][n - 1]

# Current best known determinant for order 23 {±1} matrix
# g(23) = 2^22 * a(22) where a(22)=662_671_875 is the {0,1} record (UNCERTAIN)
BEST_KNOWN_G = int(2**22 * 662_671_875)

# Upper bound (Barba for odd n=23): sqrt(45) * 22^11
# sqrt(45) ≈ 6.7082, 22^11 = 22^11
BARBA_BOUND = int(np.sqrt(45) * (22**11))

# Hadamard bound (unattainable for n=23): 23^(23/2)
HADAMARD_BOUND = int(23 ** (23/2))

@dataclass
class TestResult:
    """Result of testing a candidate matrix."""
    name: str
    det_abs: int
    det_signed: int
    passes: bool  # True if determinant is non-zero (interesting)
    improves_record: bool  # True if |det| > BEST_KNOWN_G
    improvement_pct: float  # How much better than best known (may be negative)
    pct_of_barba: float  # % of Barba upper bound
    matrix_hash: str  # SHA256 of matrix for dedup
    construction_method: str


def matrix_hash(matrix: np.ndarray) -> str:
    """SHA256 hash of a matrix for deduplication."""
    return hashlib.sha256(matrix.tobytes()).hexdigest()[:16]


def verify_matrix(matrix: np.ndarray, name: str = "unnamed",
                  construction_method: str = "unknown") -> TestResult:
    """
    Compute determinant of a candidate 23×23 {±1} matrix and compare against records.
    All entries must be exactly +1 or -1.
    """
    if matrix.shape != (N, N):
        raise ValueError(f"Expected {N}×{N} matrix, got {matrix.shape}")
    if not np.all(np.isin(matrix, [-1, 1])):
        raise ValueError("Matrix must contain only +1 and -1 entries")

    det_signed = integer_det(matrix)
    det_abs = abs(det_signed)

    improves = det_abs > BEST_KNOWN_G
    improvement = ((det_abs - BEST_KNOWN_G) / BEST_KNOWN_G) * 100
    pct_barba = (det_abs / BARBA_BOUND) * 100

    return TestResult(
        name=name,
        det_abs=det_abs,
        det_signed=det_signed,
        passes=det_abs > 0,
        improves_record=improves,
        improvement_pct=improvement,
        pct_of_barba=pct_barba,
        matrix_hash=matrix_hash(matrix),
        construction_method=construction_method,
    )


def verify_batch(matrices: list[tuple[np.ndarray, str, str]]) -> list[TestResult]:
    """Test multiple matrices. Each entry: (matrix, name, construction_method)."""
    results = []
    for matrix, name, method in matrices:
        try:
            result = verify_matrix(matrix, name, method)
            results.append(result)
        except Exception as e:
            print(f"  [SKIP] {name}: {e}")
    return results


def load_state(state_path: str = "state.json") -> dict:
    """Load persistent state with best matrices and history."""
    if os.path.exists(state_path):
        with open(state_path) as f:
            return json.load(f)
    return {
        "best_known_g": BEST_KNOWN_G,
        "barba_bound": BARBA_BOUND,
        "iterations_completed": 0,
        "total_matrices_tested": 0,
        "best_determinant": None,
        "best_matrix_name": None,
        "best_construction": None,
        "top_matrices": [],  # Top 10 by determinant
        "construction_stats": {},  # method -> {count, best_det, avg_rank_pct}
        "history": [],  # Last 20 iteration summaries
    }


def save_state(state: dict, state_path: str = "state.json") -> None:
    """Save state, keeping history bounded."""
    state["history"] = state["history"][-20:]
    state["top_matrices"] = state["top_matrices"][:10]
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, default=str)


def update_state(state: dict, results: list[TestResult],
                 iteration: int, state_path: str = "state.json") -> dict:
    """Merge new test results into state, tracking best matrices."""
    state["iterations_completed"] = iteration
    state["total_matrices_tested"] += len(results)

    for r in results:
        # Update construction stats
        method = r.construction_method
        if method not in state["construction_stats"]:
            state["construction_stats"][method] = {
                "count": 0, "best_det": 0, "best_name": None
            }
        state["construction_stats"][method]["count"] += 1
        if r.det_abs > state["construction_stats"][method]["best_det"]:
            state["construction_stats"][method]["best_det"] = r.det_abs
            state["construction_stats"][method]["best_name"] = r.name

        # Update top matrices
        entry = {
            "name": r.name,
            "det_abs": r.det_abs,
            "construction": r.construction_method,
            "pct_of_barba": round(r.pct_of_barba, 4),
            "hash": r.matrix_hash,
        }
        state["top_matrices"].append(entry)
        state["top_matrices"].sort(key=lambda x: x["det_abs"], reverse=True)
        state["top_matrices"] = state["top_matrices"][:10]

    # Update best known
    if state["top_matrices"]:
        best = state["top_matrices"][0]
        if best["det_abs"] > (state["best_determinant"] or 0):
            state["best_determinant"] = best["det_abs"]
            state["best_matrix_name"] = best["name"]
            state["best_construction"] = best["construction"]

    if results:
        state.setdefault("history", []).append({
            "iteration": iteration,
            "best_det": max(r.det_abs for r in results),
            "session_best_det": state.get("best_determinant", 0),
            "n_results": len(results),
        })

    save_state(state, state_path)
    return state


def summarize_progress(state: dict) -> str:
    """Human-readable progress summary."""
    best_det = state["best_determinant"]
    if best_det is None:
        return "No matrices tested yet."

    record_beaten = "🏆 NEW RECORD! " if best_det > BEST_KNOWN_G else ""
    pct = (best_det / BARBA_BOUND) * 100
    lines = [
        f"{record_beaten}Best determinant found: {best_det:,}",
        f"  vs. best known:   {BEST_KNOWN_G:,}",
        f"  Barba bound:      {BARBA_BOUND:,} ({pct:.2f}%)",
        f"  Construction:      {state['best_construction']}",
        f"  Iterations:        {state['iterations_completed']}",
        f"  Total tested:      {state['total_matrices_tested']:,}",
    ]
    return "\n".join(lines)
