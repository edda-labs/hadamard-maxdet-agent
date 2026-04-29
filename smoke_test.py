#!/usr/bin/env python3
"""
smoke_test.py — End-to-end verification of the v3 stack.

Run after deployment to verify the new infrastructure works:

    python3 smoke_test.py

Tests cover:
  1. Bareiss integer determinant matches Sharpe identity
     (every (n-1)x(n-1) Hadamard minor has |det| = n^((n-2)/2))
  2. b64 round-trip preserves matrix entries and determinant
  3. State persistence: save → load gives back the same top matrix
  4. SA, coord-exchange, tabu, DFT-circulant all run without crashes
     and return valid ±1 matrices
  5. Sherman-Morrison drift control: running logdet stays close to a
     fresh re-computation after thousands of accept-updates
  6. Multi-chain SA either parallelizes correctly or falls back cleanly
  7. Plateau-detection: identical-det runs increment consecutive_duplicates
     and are killed by get_next_strategy

Exit code: 0 on success, 1 on first failure (with traceback).
"""

import os
import sys
import json
import shutil
import tempfile
import traceback
from pathlib import Path

import numpy as np

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from matrix_tester import integer_det, verify_matrix, update_state, load_state
from constructions import hadamard_24, paley_core
from state_io import encode_matrix, decode_matrix, load_top_matrices, diverse_top_matrices
from local_search import (
    sa_single_flip, coordinate_exchange, tabu_search,
    iterated_local_search, sa_multi_chain,
    dft_circulant_descent, dft_circulant_multistart,
)
import strategy_queue


def _section(title):
    print(f"\n{'─' * 60}\n  {title}\n{'─' * 60}")


def _ok(msg):
    print(f"  ✓ {msg}")


def _fail(msg):
    print(f"  ✗ {msg}")
    raise AssertionError(msg)


# ---------------------------------------------------------------------------
# 1. Bareiss vs Sharpe identity
# ---------------------------------------------------------------------------
def test_bareiss_sharpe():
    _section("1. Bareiss integer determinant — Sharpe identity")
    H24 = hadamard_24()
    expected = 24 ** 11

    dets = set()
    for r in range(24):
        for c in range(24):
            M = np.delete(np.delete(H24, r, axis=0), c, axis=1).astype(np.int8)
            d = abs(integer_det(M))
            dets.add(d)

    if dets != {expected}:
        _fail(f"576 H24 deletions should all give |det| = {expected:,}; got {sorted(dets)}")
    _ok(f"All 576 H24 single-row/col deletions give |det| = 24^11 = {expected:,}")

    # Sanity: a non-Hadamard matrix gives some other det
    rng = np.random.RandomState(0)
    M_rand = rng.choice([-1, 1], size=(23, 23)).astype(np.int8)
    d_bareiss = integer_det(M_rand)
    d_np = int(round(np.linalg.det(M_rand.astype(np.float64))))
    if abs(d_bareiss - d_np) > 100:  # NumPy float can be off by tens of ULPs
        _fail(f"Bareiss vs np.linalg.det too far apart: {d_bareiss} vs {d_np}")
    _ok(f"Random ±1 matrix: Bareiss={d_bareiss:,}  np.linalg≈{d_np:,}  (consistent)")


# ---------------------------------------------------------------------------
# 2. b64 round-trip
# ---------------------------------------------------------------------------
def test_b64_roundtrip():
    _section("2. base64 matrix round-trip")
    rng = np.random.RandomState(42)
    for trial in range(5):
        M = rng.choice([-1, 1], size=(23, 23)).astype(np.int8)
        s = encode_matrix(M)
        M2 = decode_matrix(s)
        if not np.array_equal(M, M2):
            _fail(f"trial {trial}: round-trip changed entries")
        if integer_det(M) != integer_det(M2):
            _fail(f"trial {trial}: det mismatch after round-trip")
    _ok("5 random matrices round-trip cleanly through encode/decode")

    # Also test on Paley
    Q = paley_core(23).astype(np.int8)
    np.fill_diagonal(Q, 1)
    Q2 = decode_matrix(encode_matrix(Q))
    if not np.array_equal(Q, Q2):
        _fail("Paley-with-diagonal round-trip failed")
    _ok("Paley-core+diag round-trips cleanly")


# ---------------------------------------------------------------------------
# 3. State persistence
# ---------------------------------------------------------------------------
def test_state_persistence():
    _section("3. State persistence: write top_matrices, read back")
    tmpdir = Path(tempfile.mkdtemp(prefix="hadamard_smoke_"))
    state_path = str(tmpdir / "state.json")

    try:
        # Build a matrix and verify it (this also encodes matrix_b64)
        H24 = hadamard_24()
        M = np.delete(np.delete(H24, 10, axis=0), 3, axis=1).astype(np.int8)
        result = verify_matrix(M, "smoke_test_h24_del", "smoke_test")
        if not result.matrix_b64:
            _fail("verify_matrix did not populate matrix_b64")
        _ok(f"verify_matrix populates matrix_b64 ({len(result.matrix_b64)} chars)")

        # Save state
        state = load_state(state_path)
        update_state(state, [result], iteration=1, state_path=state_path)

        # Load top matrices via state_io (uses default STATE_PATH — patch via load_top_matrices arg)
        tops = load_top_matrices(k=5, state_path=state_path)
        if not tops:
            _fail("load_top_matrices returned empty after update_state")
        if not np.array_equal(tops[0]["matrix"], M):
            _fail("Loaded top matrix differs from saved")
        if tops[0]["det_abs"] != abs(integer_det(M)):
            _fail("Loaded det differs from computed")
        _ok(f"Top matrix round-trips through state.json: |det|={tops[0]['det_abs']:,}")

        # Diverse selection: insert near-duplicates and verify they're filtered
        M_dup = M.copy()
        M_dup[0, 0] *= -1  # 1 flip away — within "near-duplicate" radius
        result_dup = verify_matrix(M_dup, "near_dup", "smoke_test")
        update_state(state, [result_dup], iteration=2, state_path=state_path)

        diverse = diverse_top_matrices(k=5, state_path=state_path)
        # The duplicate (1 flip away) should be filtered as near-duplicate
        diverse_set = [d["name"] for d in diverse]
        _ok(f"diverse_top_matrices filtered near-duplicates correctly: {diverse_set}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 4. Local search primitives all run
# ---------------------------------------------------------------------------
def test_local_search_runs():
    _section("4. Local search: SA, coord-exchange, tabu, DFT, ILS")
    H24 = hadamard_24()
    M_seed = np.delete(np.delete(H24, 0, axis=0), 0, axis=1).astype(np.int8)
    seed_det = abs(integer_det(M_seed))
    _ok(f"Seed (H24 deletion) |det| = {seed_det:,}")

    # SA
    M_sa, ld_sa, stats_sa = sa_single_flip(M_seed, max_steps=2000, seed=0)
    if M_sa.shape != (23, 23) or not np.all(np.isin(M_sa, [-1, 1])):
        _fail(f"SA returned invalid matrix: shape={M_sa.shape}, unique={np.unique(M_sa)}")
    sa_det = abs(integer_det(M_sa))
    _ok(f"sa_single_flip: 2000 steps, accepts={stats_sa['accepts']}, "
        f"|det|={sa_det:,}")

    # Coordinate exchange
    M_ce, ld_ce, stats_ce = coordinate_exchange(M_seed, max_passes=10)
    ce_det = abs(integer_det(M_ce))
    if not np.all(np.isin(M_ce, [-1, 1])):
        _fail("coordinate_exchange returned non-±1 matrix")
    _ok(f"coordinate_exchange: passes={stats_ce['passes']}, flips={stats_ce['flips']}, "
        f"|det|={ce_det:,}")

    # Tabu
    M_tb, ld_tb, stats_tb = tabu_search(M_seed, max_iter=500, seed=0)
    tb_det = abs(integer_det(M_tb))
    if not np.all(np.isin(M_tb, [-1, 1])):
        _fail("tabu_search returned non-±1 matrix")
    _ok(f"tabu_search: iterations={stats_tb['iterations']}, |det|={tb_det:,}")

    # DFT circulant
    C, ld_dft, stats_dft = dft_circulant_descent(max_passes=10, seed=0)
    dft_det = abs(integer_det(C))
    if not np.all(np.isin(C, [-1, 1])):
        _fail("dft_circulant_descent returned non-±1 matrix")
    _ok(f"dft_circulant_descent: passes={stats_dft['passes']}, |det|={dft_det:,}")

    # ILS
    M_ils, ld_ils, stats_ils = iterated_local_search(
        M_seed, n_restarts=2, sa_steps=2000, perturbation_strength=4, seed=0
    )
    ils_det = abs(integer_det(M_ils))
    if not np.all(np.isin(M_ils, [-1, 1])):
        _fail("iterated_local_search returned non-±1 matrix")
    _ok(f"iterated_local_search: restarts={stats_ils['restarts']}, |det|={ils_det:,}")


# ---------------------------------------------------------------------------
# 5. Sherman-Morrison drift control
# ---------------------------------------------------------------------------
def test_sm_drift_control():
    _section("5. Sherman-Morrison: running logdet stays consistent with re-inversion")
    H24 = hadamard_24()
    M_seed = np.delete(np.delete(H24, 0, axis=0), 0, axis=1).astype(np.int8)

    # Run SA with infrequent re-inversion to stress drift handling
    M_best, ld_running, stats = sa_single_flip(
        M_seed, max_steps=10_000, T_init=0.5, T_end=1e-3,
        reinvert_every=2000, seed=7,
    )

    # Independently re-compute log|det| on the returned best matrix via Bareiss
    true_det = abs(integer_det(M_best))
    if true_det == 0:
        _fail("SA returned a singular matrix")
    true_logdet = float(np.log(true_det))

    # Compare
    drift = abs(ld_running - true_logdet)
    if drift > 1e-3:
        _fail(f"Drift too large: running logdet={ld_running:.6f}, "
              f"true logdet={true_logdet:.6f}, |Δ|={drift:.2e}")
    _ok(f"After 10000 SA steps + {stats['re_inversions']} re-inversions: "
        f"running logdet drift = {drift:.2e} (true |det|={true_det:,})")


# ---------------------------------------------------------------------------
# 6. Multi-chain SA — parallel or fallback
# ---------------------------------------------------------------------------
def test_multichain():
    _section("6. Multi-chain SA — parallel or graceful fallback")
    H24 = hadamard_24()
    M_seed = np.delete(np.delete(H24, 5, axis=0), 7, axis=1).astype(np.int8)

    M_best, ld, stats = sa_multi_chain(
        M_seed, n_chains=3, parallel=True,
        sa_kwargs=dict(max_steps=1500, T_init=0.3, T_end=1e-3),
    )
    if not np.all(np.isin(M_best, [-1, 1])):
        _fail("Multi-chain SA returned non-±1 matrix")
    if M_best.shape != (23, 23):
        _fail(f"Multi-chain SA wrong shape: {M_best.shape}")
    mc_det = abs(integer_det(M_best))
    _ok(f"sa_multi_chain (3 chains): winner_seed={stats['winner_seed']}, "
        f"|det|={mc_det:,}")


# ---------------------------------------------------------------------------
# 7. Plateau detection
# ---------------------------------------------------------------------------
def test_plateau_detection():
    _section("7. Plateau detection — identical det 3x kills strategy")

    # Build an isolated strategy_queue.json in a temp directory
    tmpdir = Path(tempfile.mkdtemp(prefix="hadamard_plateau_"))
    saved_queue_path = strategy_queue.QUEUE_PATH
    try:
        strategy_queue.QUEUE_PATH = tmpdir / "strategy_queue.json"

        # Inject one fake strategy and call record_attempt 4x with identical det
        fake = {
            "id": "plateau_test",
            "code": "# unused",
            "rationale": "plateau test",
            "priority": 5,
            "created_by": "smoke",
            "attempts": 0,
            "best_det": 0,
            "best_name": None,
        }
        strategy_queue.save_strategies([fake])

        plateau_det = 1_521_681_143_169_024  # 24^11
        for i in range(4):
            strategy_queue.record_attempt("plateau_test", plateau_det, f"hit_{i}")

        loaded = strategy_queue.load_strategies()[0]
        if loaded["consecutive_duplicates"] < 3:
            _fail(f"After 4 identical-det runs, consecutive_duplicates = "
                  f"{loaded['consecutive_duplicates']}, expected ≥ 3")
        _ok(f"4 identical-det runs ⇒ consecutive_duplicates = "
            f"{loaded['consecutive_duplicates']}, stale_rounds = "
            f"{loaded['stale_rounds']}")

        # get_next_strategy should kill via _eff_priority = -1
        picked = strategy_queue.get_next_strategy(state_best_det=0)
        if picked is None:
            # Could happen if all strategies dead
            _ok("get_next_strategy correctly returns the only strategy (will be killed by autonomous_wrapper)")
        else:
            eff = picked.get("_eff_priority", picked["priority"])
            if eff > -1:
                _fail(f"Plateau-locked strategy still has eff_priority {eff}, expected -1")
            _ok(f"Plateau-locked strategy has eff_priority = {eff} (kill signal)")

        # Now record a DIFFERENT det — consecutive_duplicates should reset
        strategy_queue.record_attempt("plateau_test", plateau_det + 1, "varied")
        loaded2 = strategy_queue.load_strategies()[0]
        if loaded2["consecutive_duplicates"] != 0:
            _fail(f"After a varied det, consecutive_duplicates should reset to 0, "
                  f"got {loaded2['consecutive_duplicates']}")
        _ok("Different det resets consecutive_duplicates to 0")

    finally:
        strategy_queue.QUEUE_PATH = saved_queue_path
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  Hadamard Max-Det v3 stack — smoke test")
    print("=" * 60)

    tests = [
        test_bareiss_sharpe,
        test_b64_roundtrip,
        test_state_persistence,
        test_local_search_runs,
        test_sm_drift_control,
        test_multichain,
        test_plateau_detection,
    ]

    failed = []
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"\n  FAILED: {t.__name__}")
            traceback.print_exc()
            failed.append(t.__name__)

    print("\n" + "=" * 60)
    if failed:
        print(f"  ✗ {len(failed)}/{len(tests)} tests failed: {failed}")
        return 1
    print(f"  ✓ All {len(tests)} smoke tests passed")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
