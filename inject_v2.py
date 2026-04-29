#!/usr/bin/env python3
"""
inject_v2.py — Inject the second-generation strategies into strategy_queue.json.

These strategies USE state_io (warm-start from persisted top matrices) and
local_search (Sherman-Morrison SA, coordinate exchange, tabu, multi-chain) —
the infrastructure that makes long polish runs cheap and continuous across
cron invocations.
"""
import json
from pathlib import Path

NEW = [
    # -----------------------------------------------------------------------
    # 1. SA from the best persisted matrix — the canonical warm-start
    # -----------------------------------------------------------------------
    {
        "id": "v2_sa_from_top",
        "code": '''"""SA-Sherman-Morrison polish starting from each of the top persisted matrices.
Single-flip neighborhood, ~50k steps per chain. Warm-starts each candidate
from a different top matrix to diversify across the 5 returned candidates.
"""
import numpy as np

def generate_matrices():
    from state_io import diverse_top_matrices
    from local_search import sa_single_flip
    from constructions import hadamard_24, paley_core

    tops = diverse_top_matrices(k=5)
    starts = [(t["matrix"], t["name"][:24]) for t in tops]

    # Fallback if state.json has no persisted matrices yet.
    if not starts:
        H24 = hadamard_24()
        Q = paley_core(23).astype(np.int8); np.fill_diagonal(Q, 1)
        starts = [
            (np.delete(np.delete(H24, 10, 0), 3, 1).astype(np.int8), "had_seed"),
            (Q, "paley_seed"),
            (np.delete(np.delete(H24, 5, 0), 7, 1).astype(np.int8), "had_seed_b"),
            (np.delete(np.delete(H24, 0, 0), 0, 1).astype(np.int8), "had_seed_c"),
            (np.delete(np.delete(H24, 17, 0), 19, 1).astype(np.int8), "had_seed_d"),
        ]

    results = []
    for idx, (M0, name) in enumerate(starts[:5]):
        M_best, ld, _ = sa_single_flip(M0, max_steps=50_000, T_init=0.3, T_end=1e-4, seed=idx)
        results.append((M_best.astype(np.int8), f"sa_top_{name}_s{idx}"))
    return results
''',
        "rationale": "SA-SM 50k steps from each of the top-5 persisted matrices — true warm-start polish",
        "priority": 9,
    },

    # -----------------------------------------------------------------------
    # 2. Coordinate exchange polish — deterministic, fast, finds local opt
    # -----------------------------------------------------------------------
    {
        "id": "v2_coord_exchange_top",
        "code": '''"""Coordinate exchange (deterministic D-optimal greedy) on top persisted matrices.
Each pass scans all 529 entries and flips whenever |det| strictly increases.
Converges to a local optimum — useful as a polish after SA or after any
algebraic construction lands near a good basin.
"""
import numpy as np

def generate_matrices():
    from state_io import diverse_top_matrices
    from local_search import coordinate_exchange
    from constructions import hadamard_24, paley_core

    tops = diverse_top_matrices(k=5)
    starts = [(t["matrix"], t["name"][:24]) for t in tops]
    if not starts:
        H24 = hadamard_24()
        Q = paley_core(23).astype(np.int8); np.fill_diagonal(Q, 1)
        starts = [
            (np.delete(np.delete(H24, 10, 0), 3, 1).astype(np.int8), "had"),
            (Q, "paley"),
            (np.delete(np.delete(H24, 5, 0), 7, 1).astype(np.int8), "had_b"),
            (np.delete(np.delete(H24, 11, 0), 13, 1).astype(np.int8), "had_c"),
            (np.delete(np.delete(H24, 17, 0), 19, 1).astype(np.int8), "had_d"),
        ]

    results = []
    for idx, (M0, name) in enumerate(starts[:5]):
        M_best, ld, _ = coordinate_exchange(M0, max_passes=30)
        results.append((M_best.astype(np.int8), f"ce_{name}_s{idx}"))
    return results
''',
        "rationale": "Coordinate-exchange polish to local optimum from top persisted matrices",
        "priority": 8,
    },

    # -----------------------------------------------------------------------
    # 3. Tabu search — typically beats SA on plateau-heavy combinatorial probs
    # -----------------------------------------------------------------------
    {
        "id": "v2_tabu_from_top",
        "code": '''"""Tabu search from top persisted matrices.
Picks the BEST single flip not currently tabu (steepest ascent + escape).
Typically outperforms SA on plateau-heavy combinatorial landscapes —
the 24^11 plateau is exactly that.
"""
import numpy as np

def generate_matrices():
    from state_io import diverse_top_matrices
    from local_search import tabu_search
    from constructions import hadamard_24, paley_core

    tops = diverse_top_matrices(k=5)
    starts = [(t["matrix"], t["name"][:24]) for t in tops]
    if not starts:
        H24 = hadamard_24()
        Q = paley_core(23).astype(np.int8); np.fill_diagonal(Q, 1)
        starts = [
            (np.delete(np.delete(H24, 10, 0), 3, 1).astype(np.int8), "had"),
            (Q, "paley"),
            (np.delete(np.delete(H24, 5, 0), 7, 1).astype(np.int8), "had_b"),
            (np.delete(np.delete(H24, 11, 0), 13, 1).astype(np.int8), "had_c"),
            (np.delete(np.delete(H24, 17, 0), 19, 1).astype(np.int8), "had_d"),
        ]

    results = []
    for idx, (M0, name) in enumerate(starts[:5]):
        M_best, ld, _ = tabu_search(M0, max_iter=3000, tabu_tenure=30, seed=idx)
        results.append((M_best.astype(np.int8), f"tabu_{name}_s{idx}"))
    return results
''',
        "rationale": "Tabu search 3k iter from each of top-5 persisted matrices",
        "priority": 8,
    },

    # -----------------------------------------------------------------------
    # 4. Iterated local search — SA + polish + kick, repeated
    # -----------------------------------------------------------------------
    {
        "id": "v2_iterated_local_search",
        "code": '''"""Iterated Local Search: SA → coord-exchange polish → kick → repeat.
The kick is 8 random sign flips on the polished matrix, which lifts us out
of the basin without losing all structural information. This is the right
shape for plateaus where pure SA wastes most time accepting/rejecting moves
that don't change det.
"""
import numpy as np

def generate_matrices():
    from state_io import diverse_top_matrices
    from local_search import iterated_local_search
    from constructions import hadamard_24, paley_core

    tops = diverse_top_matrices(k=5)
    starts = [(t["matrix"], t["name"][:20]) for t in tops]
    if not starts:
        H24 = hadamard_24()
        starts = [(np.delete(np.delete(H24, r, 0), c, 1).astype(np.int8), f"had_r{r}_c{c}")
                  for (r, c) in [(0, 0), (5, 7), (10, 3), (11, 13), (17, 19)]]

    results = []
    for idx, (M0, name) in enumerate(starts[:5]):
        M_best, ld, _ = iterated_local_search(
            M0, n_restarts=3, sa_steps=20_000, perturbation_strength=8, seed=idx
        )
        results.append((M_best.astype(np.int8), f"ils_{name}_s{idx}"))
    return results
''',
        "rationale": "Iterated Local Search (SA+polish+kick) — best plateau-escape pattern for combinatorial max-det",
        "priority": 9,
    },

    # -----------------------------------------------------------------------
    # 5. Multi-chain SA — uses Pi 5's 4 cores
    # -----------------------------------------------------------------------
    {
        "id": "v2_sa_multichain_parallel",
        "code": '''"""Parallel multi-chain SA across the Pi's 4 cores.
Spawn 4 SA chains from the same top matrix with different seeds; the best
result wins. Diversifies across stochastic basins for the same compute as 1
chain (wall-clock).
"""
import numpy as np

def generate_matrices():
    from state_io import load_top_matrices
    from local_search import sa_multi_chain
    from constructions import hadamard_24

    tops = load_top_matrices(k=5)
    if tops:
        starts = [(t["matrix"], t["name"][:20]) for t in tops]
    else:
        H24 = hadamard_24()
        starts = [(np.delete(np.delete(H24, r, 0), c, 1).astype(np.int8), f"had_r{r}_c{c}")
                  for (r, c) in [(0, 0), (5, 7), (10, 3), (11, 13), (17, 19)]]

    results = []
    for idx, (M0, name) in enumerate(starts[:5]):
        M_best, ld, stats = sa_multi_chain(
            M0, n_chains=4, parallel=True,
            sa_kwargs=dict(max_steps=40_000, T_init=0.4, T_end=1e-4),
        )
        results.append((M_best.astype(np.int8), f"mc_sa_{name}_s{idx}"))
    return results
''',
        "rationale": "4-chain parallel SA per top matrix — uses all Pi cores",
        "priority": 9,
    },

    # -----------------------------------------------------------------------
    # 6. DFT circulant descent — README's 85.8% method
    # -----------------------------------------------------------------------
    {
        "id": "v2_dft_circulant_descent",
        "code": '''"""DFT circulant descent: optimize a circulant matrix's first-row vector
to maximize log|det| = sum log|DFT_k(v)|. The search space is 2^23 ≈ 8.4M
(vs 2^529 for full matrix), and each eval is a 23-point FFT — extremely
cheap. README reports this method independently reached 85.8% of the Orrick
record without any seeding.
"""
import numpy as np

def generate_matrices():
    from local_search import dft_circulant_descent

    results = []
    for idx in range(5):
        # Different random seeds for the multi-start
        rng = np.random.RandomState(1000 + idx)
        v0 = rng.choice([-1, 1], size=23).astype(np.int8)
        C, ld, stats = dft_circulant_descent(v0, max_passes=50, seed=idx)
        results.append((C.astype(np.int8), f"dft_circ_descent_s{idx}"))
    return results
''',
        "rationale": "DFT-circulant descent — README's 85.8% method, cheap FFT-based local search on 23-vector",
        "priority": 8,
    },

    # -----------------------------------------------------------------------
    # 7. DFT multi-start (32 random starts, take best, polish)
    # -----------------------------------------------------------------------
    {
        "id": "v2_dft_circulant_multistart",
        "code": '''"""32-start DFT circulant descent + post-polish via full-matrix coord-exchange.
The DFT-circulant gets us into a circulant local optimum; the full-matrix
coordinate exchange then breaks circulant structure if a non-circulant
neighbor is better.
"""
import numpy as np

def generate_matrices():
    from local_search import dft_circulant_multistart, coordinate_exchange

    results = []
    for idx in range(5):
        C, ld, stats = dft_circulant_multistart(n_starts=24, max_passes=40, seed=idx)
        # Now polish on full matrix
        M_polished, ld2, _ = coordinate_exchange(C, max_passes=15)
        results.append((M_polished.astype(np.int8), f"dft_ms_polish_s{idx}"))
    return results
''',
        "rationale": "DFT-circulant multistart + full-matrix coord-exchange polish — breaks circulant boundary",
        "priority": 8,
    },

    # -----------------------------------------------------------------------
    # 8. Paley-diagonal-perturbed + SA polish
    # -----------------------------------------------------------------------
    {
        "id": "v2_paley_diag_sa",
        "code": '''"""Start from Paley core with various ±1 diagonals (each gives a different
seed in the GF(23)-algebraic family), then SA-polish each. The diagonal
choice affects the Gram-matrix commutator structure and thus the search
basin entered by SA.
"""
import numpy as np

def generate_matrices():
    from constructions import paley_core
    from local_search import sa_single_flip

    Q = paley_core(23).astype(np.int8)
    residues = {pow(i, 2, 23) for i in range(1, 23)}

    diag_patterns = []
    diag_patterns.append(("alldiag1", np.ones(23, dtype=np.int8)))
    diag_patterns.append(("alldiagm1", -np.ones(23, dtype=np.int8)))
    diag_patterns.append(("qr_diag",
        np.array([1 if i in residues else -1 for i in range(23)], dtype=np.int8)))
    diag_patterns.append(("alt2_diag",
        np.where(np.arange(23) % 2 == 0, 1, -1).astype(np.int8)))
    diag_patterns.append(("split_diag",
        np.concatenate([np.ones(11, dtype=np.int8), -np.ones(12, dtype=np.int8)])))

    results = []
    for idx, (name, d) in enumerate(diag_patterns):
        M0 = Q.copy()
        M0[np.arange(23), np.arange(23)] = d
        M_best, ld, _ = sa_single_flip(M0, max_steps=40_000, T_init=0.4, T_end=1e-4, seed=idx)
        results.append((M_best.astype(np.int8), f"paley_{name}_sa_s{idx}"))
    return results
''',
        "rationale": "Paley-core + ±1 diagonal variants, SA-polished — explores 5 algebraically distinct GF(23) basins",
        "priority": 8,
    },

    # -----------------------------------------------------------------------
    # 9. Negacyclic + SA polish
    # -----------------------------------------------------------------------
    {
        "id": "v2_negacyclic_sa",
        "code": '''"""Negacyclic seed (each row is -shift of previous) + SA polish.
The negacyclic structure is one of the few non-Hadamard-equivalent classes
that can host high-det 23x23 matrices; SA breaks the strict negacyclic
constraint to explore neighbors.
"""
import numpy as np

def generate_matrices():
    from local_search import sa_single_flip

    N = 23
    rng = np.random.RandomState(31337)

    # Five distinct first-row patterns
    first_rows = [
        np.where(np.arange(N) % 2 == 0, 1, -1).astype(np.int8),
        np.tile(np.array([1, 1, -1], dtype=np.int8), 8)[:N],
        rng.choice([-1, 1], size=N).astype(np.int8),
        np.array([1] * 11 + [-1] * 12, dtype=np.int8),
        rng.choice([-1, 1], size=N).astype(np.int8),
    ]

    results = []
    for idx, fr in enumerate(first_rows):
        M0 = np.zeros((N, N), dtype=np.int8)
        M0[0] = fr
        for r in range(1, N):
            M0[r, 0] = -M0[r - 1, N - 1]
            M0[r, 1:] = -M0[r - 1, :-1]
        # If first row gave singular: skip via SA's safe handling
        M_best, ld, _ = sa_single_flip(M0, max_steps=40_000, T_init=0.3, T_end=1e-4, seed=idx)
        results.append((M_best.astype(np.int8), f"nega_sa_v{idx}"))
    return results
''',
        "rationale": "Negacyclic seeds with 5 first-row patterns + SA polish",
        "priority": 7,
    },

    # -----------------------------------------------------------------------
    # 10. Goethals-Seidel-style 4-block construction for n=23
    # -----------------------------------------------------------------------
    {
        "id": "v2_gs_block_construction",
        "code": '''"""Goethals-Seidel-style 4-block construction adapted for n=23.
Build M as a block matrix with circulant blocks of length-6 sequences chosen
for low autocorrelation — n=23 is prime so we use the 4×6 = 24 → bordered
to 23 layout. Then SA-polish to break the strict block structure.

Note: classical G-S arrays are 4t×4t, so we adapt by picking the closest
fit and accepting the border deviation.
"""
import numpy as np

def generate_matrices():
    from local_search import sa_single_flip

    N = 23
    rng = np.random.RandomState(42)

    def circulant(v):
        n = len(v)
        C = np.zeros((n, n), dtype=np.int8)
        for i in range(n):
            C[i] = np.roll(v, i)
        return C

    results = []
    for idx in range(5):
        # 4 length-6 ±1 sequences for the four blocks; final layout: 4×6 = 24,
        # delete last row+col to get 23.
        sub_seqs = [rng.choice([-1, 1], size=6).astype(np.int8) for _ in range(4)]
        A = circulant(sub_seqs[0])
        B = circulant(sub_seqs[1])
        C = circulant(sub_seqs[2])
        D = circulant(sub_seqs[3])

        # Goethals-Seidel layout for 4t×4t (with R reverse permutation)
        R = np.fliplr(np.eye(6, dtype=np.int8))
        M24 = np.zeros((24, 24), dtype=np.int8)
        # [[A, BR, CR, DR], [-BR, A, D^T R, -C^T R], [-CR, -D^T R, A, B^T R], [-DR, C^T R, -B^T R, A]]
        M24[0:6,    0:6 ]  =  A
        M24[0:6,    6:12]  =  B @ R
        M24[0:6,   12:18]  =  C @ R
        M24[0:6,   18:24]  =  D @ R
        M24[6:12,   0:6 ]  = -B @ R
        M24[6:12,   6:12]  =  A
        M24[6:12,  12:18]  =  D.T @ R
        M24[6:12,  18:24]  = -C.T @ R
        M24[12:18,  0:6 ]  = -C @ R
        M24[12:18,  6:12]  = -D.T @ R
        M24[12:18, 12:18]  =  A
        M24[12:18, 18:24]  =  B.T @ R
        M24[18:24,  0:6 ]  = -D @ R
        M24[18:24,  6:12]  =  C.T @ R
        M24[18:24, 12:18]  = -B.T @ R
        M24[18:24, 18:24]  =  A

        # Force ±1 (matrix product can give other values if seeds aren't ±1 already,
        # but circulant of ±1 stays ±1 and R is ±1; products of ±1 ±1 are ±1.)
        M24 = np.sign(M24).astype(np.int8)
        M24[M24 == 0] = 1

        # Delete last row and column to get 23×23
        M23 = M24[:23, :23].copy()

        # SA polish
        M_best, ld, _ = sa_single_flip(M23, max_steps=30_000, T_init=0.3, T_end=1e-4, seed=idx)
        results.append((M_best.astype(np.int8), f"gs_block_s{idx}"))
    return results
''',
        "rationale": "Goethals-Seidel-style 4×6 block layout adapted to n=23 + SA polish",
        "priority": 7,
    },

    # -----------------------------------------------------------------------
    # 11. Cross-pollination: row swap between two top matrices, SA polish
    # -----------------------------------------------------------------------
    {
        "id": "v2_crossover_sa",
        "code": '''"""Cross over rows between pairs of top matrices, then SA-polish.
If matrix A and matrix B both have det near the same plateau but in
different local basins, splicing rows (and maybe columns) can produce a
hybrid that sits in neither basin and is better positioned for SA escape.
"""
import numpy as np

def generate_matrices():
    from state_io import diverse_top_matrices
    from local_search import sa_single_flip
    from constructions import hadamard_24

    tops = diverse_top_matrices(k=10)
    if len(tops) < 2:
        # Fallback: cross H24 deletions
        H24 = hadamard_24()
        m1 = np.delete(np.delete(H24, 10, 0), 3, 1).astype(np.int8)
        m2 = np.delete(np.delete(H24, 5, 0), 7, 1).astype(np.int8)
        tops = [{"matrix": m1, "name": "had1"}, {"matrix": m2, "name": "had2"}]

    rng = np.random.RandomState(2024)
    results = []
    for idx in range(5):
        i1, i2 = rng.choice(len(tops), size=2, replace=False)
        A = tops[i1]["matrix"]; B = tops[i2]["matrix"]
        split = rng.randint(5, 19)
        H = np.zeros((23, 23), dtype=np.int8)
        if rng.random() < 0.5:
            H[:split] = A[:split]
            H[split:] = B[split:]
        else:
            H[:, :split] = A[:, :split]
            H[:, split:] = B[:, split:]
        M_best, ld, _ = sa_single_flip(H, max_steps=30_000, T_init=0.3, T_end=1e-4, seed=idx)
        results.append((M_best.astype(np.int8), f"cross_sa_{idx}"))
    return results
''',
        "rationale": "Row/column crossover between top-10 matrices + SA polish — basin recombination",
        "priority": 7,
    },
]


if __name__ == "__main__":
    queue_path = Path(__file__).parent / "strategy_queue.json"
    if queue_path.exists():
        queue = json.loads(queue_path.read_text())
    else:
        queue = []
    existing = {s["id"] for s in queue}

    added = 0
    for s in NEW:
        if s["id"] in existing:
            print(f"  [SKIP] {s['id']} already in queue")
            continue
        queue.append({
            **s,
            "created_by": "v2_inject",
            "attempts": 0,
            "best_det": 0,
            "best_name": None,
        })
        existing.add(s["id"])
        added += 1
        print(f"  [+]    {s['id']}  p={s['priority']}  — {s['rationale'][:70]}")

    queue.sort(key=lambda s: s.get("priority", 0), reverse=True)
    queue_path.write_text(json.dumps(queue, indent=2))
    print(f"\nInjected {added} new strategies. Queue total: {len(queue)}.")
