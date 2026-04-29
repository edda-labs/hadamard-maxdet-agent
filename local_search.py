"""
local_search.py — Fast local search primitives for ±1 matrix max-det.

Why Sherman-Morrison: every SA/coord-exchange step needs det(M_new) given a
single-entry flip. Recomputing det from scratch is O(n^3); maintaining M^(-1)
and using the matrix determinant lemma gives det(M_new)/det(M_old) =
1 + δ · M^(-1)[j,i] in O(1), with O(n^2) updates of M^(-1) on accept. For
n=23 this is the difference between ~300 SA steps per minute and 100k–1M.

Drift control: float M^(-1) accumulates rounding over thousands of rank-1
updates, so we periodically re-invert from scratch (every `reinvert_every`
steps).

Final accounting: SA/coord/tabu return integer ±1 matrices and a float
log|det| from running NumPy. The CALLER is responsible for re-evaluating the
returned matrix via matrix_tester.integer_det (Bareiss bigint) for the
authoritative determinant — the running float estimate is only for proposal
ranking.
"""

import multiprocessing as mp
import os
from typing import Callable, Optional

import numpy as np


def _safe_inv(M: np.ndarray) -> Optional[np.ndarray]:
    try:
        return np.linalg.inv(M)
    except np.linalg.LinAlgError:
        return None


def _safe_logdet(M: np.ndarray) -> float:
    sign, logabsdet = np.linalg.slogdet(M)
    if sign == 0:
        return -np.inf
    return float(logabsdet)


def sa_single_flip(
    M_init: np.ndarray,
    max_steps: int = 100_000,
    T_init: float = 0.3,
    T_end: float = 1e-4,
    reinvert_every: int = 500,
    seed: int = 0,
) -> tuple[np.ndarray, float, dict]:
    """Sherman-Morrison SA on ±1 matrices, maximizing log|det|.

    Cooling: geometric T(step) = T_init * (T_end/T_init)^(step/max_steps).
    Acceptance: standard Metropolis on log|det|.

    Returns (best_matrix_int8, best_logabsdet, stats).
    """
    rng = np.random.RandomState(seed)
    M = M_init.copy().astype(np.float64)
    n = M.shape[0]

    Minv = _safe_inv(M)
    if Minv is None:
        return M_init.copy().astype(np.int8), -np.inf, {"error": "singular_init"}
    cur_logdet = _safe_logdet(M)

    best_M = M_init.copy().astype(np.int8)
    best_logdet = cur_logdet

    T = T_init
    cooling = (T_end / T_init) ** (1.0 / max(1, max_steps))

    accepts = 0
    rejects = 0
    re_inversions = 0

    for step in range(max_steps):
        i = rng.randint(n)
        j = rng.randint(n)
        delta = -2.0 * M[i, j]
        ratio = 1.0 + delta * Minv[j, i]
        absratio = abs(ratio)

        if absratio < 1e-12:
            rejects += 1
            T *= cooling
            continue

        d_logdet = float(np.log(absratio))

        if d_logdet >= 0 or rng.random() < np.exp(d_logdet / max(T, 1e-12)):
            M[i, j] += delta
            col_i = Minv[:, i].copy()
            row_j = Minv[j, :].copy()
            Minv -= (delta / ratio) * np.outer(col_i, row_j)
            cur_logdet += d_logdet
            accepts += 1

            if cur_logdet > best_logdet:
                best_logdet = cur_logdet
                best_M = M.astype(np.int8).copy()
        else:
            rejects += 1

        T *= cooling

        if (step + 1) % reinvert_every == 0:
            new_inv = _safe_inv(M)
            if new_inv is None:
                # Drift made M singular — revert to best and continue
                M = best_M.astype(np.float64).copy()
                Minv = _safe_inv(M)
                if Minv is None:
                    break
                cur_logdet = _safe_logdet(M)
            else:
                Minv = new_inv
                cur_logdet = _safe_logdet(M)
            re_inversions += 1

    return best_M, best_logdet, {
        "accepts": accepts,
        "rejects": rejects,
        "re_inversions": re_inversions,
        "final_T": T,
    }


def coordinate_exchange(
    M_init: np.ndarray,
    max_passes: int = 50,
) -> tuple[np.ndarray, float, dict]:
    """D-optimal coordinate exchange: greedy single-flip improvement.

    At each pass, scan all n^2 entries; flip whenever the flip strictly
    increases |det|. Stop when a full pass finds no improvement (local
    optimum). Deterministic — useful as a polish after SA or as a baseline.
    """
    M = M_init.copy().astype(np.float64)
    n = M.shape[0]
    Minv = _safe_inv(M)
    if Minv is None:
        return M_init.copy().astype(np.int8), -np.inf, {"error": "singular_init"}
    logabsdet = _safe_logdet(M)

    flips_total = 0
    passes_done = 0
    for pass_no in range(max_passes):
        passes_done = pass_no + 1
        flipped = False
        for i in range(n):
            for j in range(n):
                delta = -2.0 * M[i, j]
                ratio = 1.0 + delta * Minv[j, i]
                if abs(ratio) > 1.0 + 1e-9:  # strict improvement
                    M[i, j] += delta
                    col_i = Minv[:, i].copy()
                    row_j = Minv[j, :].copy()
                    Minv -= (delta / ratio) * np.outer(col_i, row_j)
                    logabsdet += np.log(abs(ratio))
                    flipped = True
                    flips_total += 1
        if not flipped:
            break
        # Periodic re-inversion against drift
        if pass_no % 3 == 2:
            new_inv = _safe_inv(M)
            if new_inv is None:
                break
            Minv = new_inv
            logabsdet = _safe_logdet(M)

    return M.astype(np.int8), logabsdet, {"passes": passes_done, "flips": flips_total}


def tabu_search(
    M_init: np.ndarray,
    max_iter: int = 5_000,
    tabu_tenure: int = 30,
    seed: int = 0,
) -> tuple[np.ndarray, float, dict]:
    """Tabu search: pick the BEST single flip not currently tabu.

    Tabu list = grid of "step until allowed". Aspiration criterion: a tabu
    move is allowed if it would set a new global best. Recomputes M^(-1)
    every 100 iterations against drift.
    """
    rng = np.random.RandomState(seed)
    M = M_init.copy().astype(np.float64)
    n = M.shape[0]
    Minv = _safe_inv(M)
    if Minv is None:
        return M_init.copy().astype(np.int8), -np.inf, {"error": "singular_init"}
    cur_logdet = _safe_logdet(M)

    best_M = M_init.copy().astype(np.int8)
    best_logdet = cur_logdet

    tabu_until = np.zeros((n, n), dtype=np.int32)

    last_step = 0
    for step in range(max_iter):
        last_step = step
        delta = -2.0 * M
        # ratio[i,j] = 1 + delta[i,j] * Minv[j,i]; vectorized via Minv.T
        ratios = 1.0 + delta * Minv.T
        absratios = np.abs(ratios)

        log_absratios = np.log(np.maximum(absratios, 1e-12))
        candidate_logdets = cur_logdet + log_absratios

        # Aspiration: allow tabu cells that would beat global best
        allowed = (tabu_until <= step) | (candidate_logdets > best_logdet)
        masked = np.where(allowed, absratios, -np.inf)

        flat_idx = int(np.argmax(masked))
        i, j = divmod(flat_idx, n)

        if absratios[i, j] < 1e-12:
            break

        ratio = ratios[i, j]
        d = delta[i, j]
        M[i, j] += d
        col_i = Minv[:, i].copy()
        row_j = Minv[j, :].copy()
        Minv -= (d / ratio) * np.outer(col_i, row_j)
        cur_logdet += float(np.log(abs(ratio)))

        tabu_until[i, j] = step + tabu_tenure

        if cur_logdet > best_logdet:
            best_logdet = cur_logdet
            best_M = M.astype(np.int8).copy()

        if (step + 1) % 100 == 0:
            new_inv = _safe_inv(M)
            if new_inv is None:
                M = best_M.astype(np.float64).copy()
                new_inv = _safe_inv(M)
                if new_inv is None:
                    break
                cur_logdet = _safe_logdet(M)
            else:
                Minv = new_inv
                cur_logdet = _safe_logdet(M)

    return best_M, best_logdet, {"iterations": last_step + 1}


def iterated_local_search(
    M_init: np.ndarray,
    n_restarts: int = 5,
    sa_steps: int = 30_000,
    perturbation_strength: int = 8,
    seed: int = 0,
) -> tuple[np.ndarray, float, dict]:
    """Iterated Local Search: SA → polish → kick → repeat.

    Each round: run SA from current best, polish with coord-exchange, then
    kick by flipping `perturbation_strength` random entries to escape the
    basin. Tracks the global best across restarts.
    """
    rng = np.random.RandomState(seed)
    n = M_init.shape[0]

    cur = M_init.copy().astype(np.int8)
    best_M = cur.copy()
    best_logdet = -np.inf

    for r in range(n_restarts):
        M_sa, ld_sa, _ = sa_single_flip(cur, max_steps=sa_steps, seed=seed * 1000 + r)
        M_pol, ld_pol, _ = coordinate_exchange(M_sa, max_passes=20)

        if ld_pol > best_logdet:
            best_logdet = ld_pol
            best_M = M_pol.copy()

        # Kick: flip `perturbation_strength` random entries on the polished result
        kicked = M_pol.copy()
        idxs = rng.choice(n * n, size=perturbation_strength, replace=False)
        for k in idxs:
            i, j = divmod(int(k), n)
            kicked[i, j] *= -1
        cur = kicked

    return best_M, best_logdet, {"restarts": n_restarts}


# ---------------------------------------------------------------------------
# Multi-chain parallelization (Pi 5: 4 cores)
# ---------------------------------------------------------------------------

def _sa_chain_worker(args):
    M_init, kwargs, seed = args
    return sa_single_flip(M_init, seed=seed, **kwargs)


def _ils_chain_worker(args):
    M_init, kwargs, seed = args
    return iterated_local_search(M_init, seed=seed, **kwargs)


def sa_multi_chain(
    M_init: np.ndarray,
    n_chains: int = 4,
    parallel: bool = True,
    sa_kwargs: Optional[dict] = None,
) -> tuple[np.ndarray, float, dict]:
    """Run n_chains SA from same start with different seeds; best wins.

    Uses multiprocessing on Linux/macOS (fork) for true parallelism. Falls
    back to sequential execution if the pool can't start (Windows-spawn quirks
    inside an exec()'d strategy namespace).
    """
    sa_kwargs = dict(sa_kwargs or {})
    sa_kwargs.setdefault("max_steps", 50_000)
    seeds = list(range(n_chains))
    args = [(M_init, sa_kwargs, s) for s in seeds]

    results = None
    if parallel and n_chains > 1:
        try:
            ctx = mp.get_context("fork") if "fork" in mp.get_all_start_methods() else mp
            workers = min(n_chains, max(1, (os.cpu_count() or 1)))
            with ctx.Pool(workers) as pool:
                results = pool.map(_sa_chain_worker, args)
        except Exception:
            results = None

    if results is None:
        results = [_sa_chain_worker(a) for a in args]

    best_idx = max(range(len(results)), key=lambda i: results[i][1])
    M_best, ld_best, stats = results[best_idx]
    return M_best, ld_best, {"n_chains": n_chains, "winner_seed": best_idx, **stats}


def ils_multi_chain(
    M_init: np.ndarray,
    n_chains: int = 4,
    parallel: bool = True,
    ils_kwargs: Optional[dict] = None,
) -> tuple[np.ndarray, float, dict]:
    """Parallel iterated local search."""
    ils_kwargs = dict(ils_kwargs or {})
    seeds = list(range(n_chains))
    args = [(M_init, ils_kwargs, s) for s in seeds]

    results = None
    if parallel and n_chains > 1:
        try:
            ctx = mp.get_context("fork") if "fork" in mp.get_all_start_methods() else mp
            workers = min(n_chains, max(1, (os.cpu_count() or 1)))
            with ctx.Pool(workers) as pool:
                results = pool.map(_ils_chain_worker, args)
        except Exception:
            results = None

    if results is None:
        results = [_ils_chain_worker(a) for a in args]

    best_idx = max(range(len(results)), key=lambda i: results[i][1])
    M_best, ld_best, stats = results[best_idx]
    return M_best, ld_best, {"n_chains": n_chains, "winner_seed": best_idx, **stats}


# ---------------------------------------------------------------------------
# DFT circulant descent (1D coordinate exchange on circulant first row)
# ---------------------------------------------------------------------------

def _circulant_logdet(v: np.ndarray) -> float:
    """log|det(C(v))| = sum_k log|DFT_k(v)|."""
    dft = np.fft.fft(v.astype(np.float64))
    absdft = np.abs(dft)
    if np.any(absdft < 1e-12):
        return -np.inf
    return float(np.sum(np.log(absdft)))


def _build_circulant(v: np.ndarray) -> np.ndarray:
    n = len(v)
    C = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        C[i] = np.roll(v, i)
    return C


def dft_circulant_descent(
    v_init: Optional[np.ndarray] = None,
    max_passes: int = 50,
    seed: int = 0,
) -> tuple[np.ndarray, float, dict]:
    """Coordinate exchange on a circulant matrix's first-row vector.

    The search space is 2^23 = 8.4M (vs. 2^529 for full matrix), and each
    eval is just an n-point FFT — extremely cheap. README mentions this
    method independently reached 85.8% of the Orrick record without seeding.
    """
    rng = np.random.RandomState(seed)
    n = 23
    v = (v_init.copy().astype(np.int8)
         if v_init is not None
         else rng.choice([-1, 1], size=n).astype(np.int8))

    cur_logdet = _circulant_logdet(v)
    flips = 0
    passes_done = 0
    for p in range(max_passes):
        passes_done = p + 1
        improved = False
        order = rng.permutation(n)
        for k in order:
            v[k] *= -1
            new_ld = _circulant_logdet(v)
            if new_ld > cur_logdet + 1e-12:
                cur_logdet = new_ld
                improved = True
                flips += 1
            else:
                v[k] *= -1
        if not improved:
            break

    C = _build_circulant(v)
    return C, cur_logdet, {"passes": passes_done, "flips": flips, "first_row": v.tolist()}


def dft_circulant_multistart(
    n_starts: int = 32,
    max_passes: int = 50,
    seed: int = 0,
) -> tuple[np.ndarray, float, dict]:
    """Multi-start DFT-circulant descent. Returns globally best."""
    rng = np.random.RandomState(seed)
    best_C = None
    best_ld = -np.inf
    for k in range(n_starts):
        v0 = rng.choice([-1, 1], size=23).astype(np.int8)
        C, ld, _ = dft_circulant_descent(v0, max_passes=max_passes, seed=seed * 1000 + k)
        if ld > best_ld:
            best_ld = ld
            best_C = C
    return best_C, best_ld, {"n_starts": n_starts}
