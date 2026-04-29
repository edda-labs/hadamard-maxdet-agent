"""
state_io.py — Persist top matrices' actual ±1 entries in state.json.

The original code stored only a hash + metadata in state["top_matrices"], so
each cron run started from scratch — strategies could not perturb the best
known matrix because its entries were gone. This module adds base64 round-trip
encoding so warm-starts are possible across runs.

Encoding: int8 bytes → base64. 23×23 = 529 bytes raw, ~712 chars b64.
Top-10 matrices add ~7 KB to state.json — negligible.
"""

import base64
import json
from pathlib import Path

import numpy as np

PROJECT_DIR = Path(__file__).parent
STATE_PATH = PROJECT_DIR / "state.json"
N = 23


def encode_matrix(matrix: np.ndarray) -> str:
    """Encode a 23×23 ±1 matrix as base64 of int8 bytes."""
    arr = np.asarray(matrix, dtype=np.int8)
    if arr.shape != (N, N):
        raise ValueError(f"Expected {N}×{N}, got {arr.shape}")
    return base64.b64encode(arr.tobytes()).decode("ascii")


def decode_matrix(s: str) -> np.ndarray:
    """Decode base64 string back to 23×23 ±1 int8 matrix."""
    data = base64.b64decode(s.encode("ascii"))
    return np.frombuffer(data, dtype=np.int8).reshape(N, N).copy()


def load_top_matrices(k: int = 10, state_path: Path = STATE_PATH) -> list[dict]:
    """Return up to k top matrices with actual entries.

    Each entry: {"name", "det_abs", "construction", "pct_of_barba", "matrix"}.
    Skips entries that lack matrix_b64 (legacy entries from before persistence).
    """
    if not Path(state_path).exists():
        return []
    with open(state_path) as f:
        state = json.load(f)
    out = []
    for entry in state.get("top_matrices", []):
        b64 = entry.get("matrix_b64")
        if not b64:
            continue
        try:
            M = decode_matrix(b64)
            out.append({
                "name": entry.get("name", ""),
                "det_abs": entry.get("det_abs", 0),
                "construction": entry.get("construction", ""),
                "pct_of_barba": entry.get("pct_of_barba", 0.0),
                "matrix": M,
            })
            if len(out) >= k:
                break
        except Exception:
            continue
    return out


def best_matrix(state_path: Path = STATE_PATH) -> np.ndarray | None:
    """Return the single best persisted matrix, or None."""
    tops = load_top_matrices(1, state_path)
    return tops[0]["matrix"] if tops else None


def diverse_top_matrices(k: int = 5, state_path: Path = STATE_PATH) -> list[dict]:
    """Return up to k matrices, picking by det but breaking near-duplicates.

    Two matrices are "near-duplicate" if their entries differ in fewer than 5
    positions — useful for SA seeding to avoid spending all chains on the same
    local optimum.
    """
    candidates = load_top_matrices(k * 5, state_path)
    if not candidates:
        return []
    selected = [candidates[0]]
    for c in candidates[1:]:
        too_close = False
        for s in selected:
            diff = int(np.sum(c["matrix"] != s["matrix"]))
            if diff < 5:
                too_close = True
                break
        if not too_close:
            selected.append(c)
        if len(selected) >= k:
            break
    return selected
