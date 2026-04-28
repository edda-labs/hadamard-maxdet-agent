import json, uuid
from pathlib import Path

NEW = [
    {
        "id": "auto_gram_target",
        "code": '''"""
Gram matrix targeting: Build matrices whose Gram matrix G = M M^T
approximates the optimal Ehlich structure for n ≡ 3 mod 4.

For n=23, Ehlich bound says optimal G is block-diagonal after subtracting J,
with block structure: 4 blocks of size 6 (first 3) and size 5 (last 1), since 23 = 6+6+6+5.

Strategy: Start from a structured base, then iteratively flip entries
to push the Gram matrix toward the ideal pattern.
"""
import numpy as np

def generate_matrices():
    N = 23
    from constructions import hadamard_24

    # Ideal Gram matrix for Ehlich structure
    # For n=23, s=6 (number of blocks from Ehlich table for 15≤n≤59)
    # Block sizes: r=3, v=5 blocks of size 4, u=1 block of size 3 → 5*4+1*3=23 ✓
    # The ideal G has blocks of (n-3)I + 4J = 20I + 4J within each cluster

    H24 = hadamard_24()
    results = []

    # Strategy: Delete row/col from H24, then try to reorganize into 4 clusters
    # by permuting rows to maximize block structure
    for deletion_idx in range(5):
        r_del = [0, 6, 12, 18, 23][deletion_idx]
        c_del = [0, 6, 12, 18, 23][deletion_idx]
        M = np.delete(np.delete(H24, r_del, axis=0), c_del, axis=1).astype(np.int8)

        # Permute rows to cluster similar rows together
        # Compute row similarities and greedily cluster
        G = M @ M.T
        # Start with first row, find similar rows
        order = [0]
        remaining = set(range(1, N))
        while remaining:
            last = order[-1]
            # Find row most correlated with last
            best = max(remaining, key=lambda i: abs(G[last, i]))
            order.append(best)
            remaining.remove(best)

        M_perm = M[order, :]

        # Now try block-negating: negate entire blocks to optimize
        block_sizes = [6, 6, 6, 5]
        offset = 0
        M_blocks = M_perm.copy()
        for bsize in block_sizes:
            # Try negating this block
            for flip in [False, True]:
                if flip:
                    M_blocks[offset:offset+bsize, :] *= -1
            offset += bsize

        results.append((M_blocks, f'gram_cluster_del{r_del}'))

    return results[:5]
''',
        "rationale": "Target the Ehlich-optimal Gram matrix structure via row clustering and block negation",
        "priority": 7,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    },
    {
        "id": "auto_genetic_crossover",
        "code": '''"""
Genetic algorithm: Breed offspring from the best-performing matrices.
Take rows from parent matrices, creating hybrids that preserve
structural properties while exploring new territory.
"""
import numpy as np
from constructions import hadamard_24, paley_core

def generate_matrices():
    N = 23
    rng = np.random.RandomState(777)

    # Build a diverse "population" of parent matrices
    parents = []

    # Parent 1: Best Hadamard submatrix (R10xC3 was best)
    H24 = hadamard_24()
    p1 = np.delete(np.delete(H24, 10, axis=0), 3, axis=1).astype(np.int8)
    parents.append(("had_best", p1))

    # Parent 2: Paley core with all-ones diagonal
    Q = paley_core(23).astype(np.int8)
    np.fill_diagonal(Q, 1)
    parents.append(("paley_all1", Q))

    # Parent 3: Paley core with alternating diagonal
    Q2 = paley_core(23).astype(np.int8)
    Q2[np.arange(N), np.arange(N)] = np.where(np.arange(N) % 2 == 0, 1, -1).astype(np.int8)
    parents.append(("paley_alt", Q2))

    # Parent 4: Negacyclic
    first_row = np.where(np.arange(N) % 2 == 0, 1, -1).astype(np.int8)
    M = np.zeros((N, N), dtype=np.int8)
    M[0] = first_row
    for r in range(1, N):
        M[r, 0] = -M[r-1, N-1]
        M[r, 1:] = -M[r-1, :-1]
    parents.append(("nega", M))

    results = []

    for offspring_idx in range(5):
        # Pick 2 parents
        p1_idx, p2_idx = rng.choice(len(parents), 2, replace=False)
        name1, P1 = parents[p1_idx]
        name2, P2 = parents[p2_idx]

        # Create offspring: take some rows from P1, some from P2
        # Use a random split: first k rows from P1, rest from P2
        split = rng.randint(5, 19)
        offspring = np.zeros((N, N), dtype=np.int8)

        # 60% chance: row-based crossover
        if rng.random() < 0.6:
            offspring[:split, :] = P1[:split, :]
            offspring[split:, :] = P2[split:, :]
        else:
            # Column-based crossover
            offspring[:, :split] = P1[:, :split]
            offspring[:, split:] = P2[:, split:]

        # Mutation: flip 1-3 random entries
        n_mutations = rng.randint(1, 4)
        for _ in range(n_mutations):
            i, j = rng.randint(0, N, 2)
            offspring[i, j] *= -1

        results.append((offspring, f'genetic_{name1}x{name2}_s{split}'))

    return results
''',
        "rationale": "Genetic crossover between best Hadamard submatrix, Paley variants, and negacyclic — preserve structural patterns via row/col inheritance",
        "priority": 6,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    },
    {
        "id": "auto_paley_permutations",
        "code": '''"""
Paley permutation ensemble: The Paley core Q has strong algebraic structure
from the quadratic character of GF(23). Applying field automorphisms
(multiplication by quadratic residues) produces equivalent but different matrices.

Strategy: Permute rows/cols of Paley core by multiplying indices by
quadratic residues mod 23, then fill diagonal intelligently.
"""
import numpy as np
from constructions import paley_core

def legendre(a, p):
    if a % p == 0:
        return 0
    ls = pow(a, (p-1)//2, p)
    return -1 if ls == p - 1 else ls

def generate_matrices():
    N = 23
    Q = paley_core(N).astype(np.int8)

    # Quadratic residues mod 23 (the squares)
    residues = sorted({(i*i) % 23 for i in range(1, 23)})
    # Non-residues
    nonresidues = [i for i in range(1, 23) if i not in residues]

    results = []

    # Strategy 1: Multiply indices by residue k -> permutation
    for idx, k in enumerate(residues[:5]):
        # Permutation: i -> (i * k) mod 23
        perm = [(i * k) % N for i in range(N)]
        Q_perm = Q[perm, :][:, perm]

        # Try diagonal fill strategy
        # For skew-symmetric Q (since 23≡3 mod 4), Q[i,i]=0, Q[i,j]=-Q[j,i]
        # Fill diagonal: alternating pattern
        M = Q_perm.copy()
        diag_vals = np.where(np.arange(N) % 2 == 0, 1, -1).astype(np.int8)
        np.fill_diagonal(M, diag_vals)

        results.append((M, f'paley_perm_k{k}_altdiag'))

    return results[:5]
''',
        "rationale": "Exploit GF(23) field automorphisms — permuting Paley core by quadratic residue multiplication creates non-equivalent matrices with the same algebraic pedigree",
        "priority": 5,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    },
    {
        "id": "auto_schur_border",
        "code": '''"""
Schur complement approach: Split 23×23 into a core submatrix
and borders. Use the Schur determinant formula to optimize.

det(M) = det(A) * det(D - C A^{-1} B)

Build A as a near-Hadamard submatrix, optimize borders.
"""
import numpy as np
from constructions import hadamard_24

def generate_matrices():
    N = 23
    H24 = hadamard_24()
    rng = np.random.RandomState(555)

    results = []

    for core_size in [12, 11, 15, 8, 18]:
        # Build A: core_size × core_size submatrix from H24
        A = H24[:core_size, :core_size].astype(np.int8)

        # Build borders B, C, D randomly but structured
        b_rows = core_size
        b_cols = N - core_size

        if b_cols <= 0:
            continue

        B = rng.choice([-1, 1], size=(b_rows, b_cols)).astype(np.int8)
        C = rng.choice([-1, 1], size=(b_cols, b_rows)).astype(np.int8)
        D = rng.choice([-1, 1], size=(b_cols, b_cols)).astype(np.int8)

        # Make D symmetric for better properties
        D = np.triu(D) + np.triu(D, 1).T
        np.fill_diagonal(D, rng.choice([-1, 1], size=b_cols))

        # Assemble
        M = np.zeros((N, N), dtype=np.int8)
        M[:core_size, :core_size] = A
        M[:core_size, core_size:] = B
        M[core_size:, :core_size] = C
        M[core_size:, core_size:] = D

        results.append((M, f'schur_core{core_size}'))

    return results[:5]
''',
        "rationale": "Schur complement block construction with varying core sizes — the core inherits Hadamard structure while borders are optimized separately",
        "priority": 4,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    },
    {
        "id": "auto_hadamard_product",
        "code": '''"""
Hadamard (elementwise) product of two structured matrices.
If A and B have complementary structures, A ⊙ B may inherit
beneficial properties from both.

Try: Paley core ⊙ circulant, Hadamard submatrix ⊙ Toeplitz, etc.
"""
import numpy as np
from constructions import hadamard_24, paley_core

def generate_matrices():
    N = 23
    rng = np.random.RandomState(333)

    results = []

    # Base matrix A: Best Hadamard submatrix
    H24 = hadamard_24()
    A = np.delete(np.delete(H24, 10, axis=0), 3, axis=1).astype(np.int8)

    # Matrix B1: Paley core with diagonal
    Q = paley_core(N).astype(np.int8)
    np.fill_diagonal(Q, 1)
    AB1 = A * Q
    results.append((AB1, 'hadprod_paley'))

    # Matrix B2: Circulant
    first_row = rng.choice([-1, 1], size=N).astype(np.int8)
    B2 = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        B2[i] = np.roll(first_row, i)
    AB2 = A * B2
    results.append((AB2, 'hadprod_circ'))

    # Matrix B3: Different Hadamard submatrix
    B3 = np.delete(np.delete(H24, 15, axis=0), 8, axis=1).astype(np.int8)
    AB3 = A * B3
    results.append((AB3, 'hadprod_hadam'))

    # Matrix B4: Random symmetric
    upper = rng.choice([-1, 1], size=(N, N)).astype(np.int8)
    B4 = np.triu(upper) + np.triu(upper, 1).T
    np.fill_diagonal(B4, 1)
    AB4 = A * B4
    results.append((AB4, 'hadprod_sym'))

    # Matrix B5: Alternating checkerboard
    B5 = np.fromfunction(lambda i, j: 1 - 2*((i+j)%2), (N, N), dtype=np.int8)
    AB5 = A * B5
    results.append((AB5, 'hadprod_check'))

    return results
''',
        "rationale": "Hadamard product combines structural properties — Paley algebraic structure with Hadamard submatrix optimality",
        "priority": 5,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None
    }
]

# Load existing queue, append new strategies
queue_path = Path('/home/marc/.hermes/hadamard-research/strategy_queue.json')
queue = json.loads(queue_path.read_text())

existing_ids = {s['id'] for s in queue}
added = 0
for s in NEW:
    if s['id'] not in existing_ids:
        queue.append(s)
        existing_ids.add(s['id'])
        added += 1

queue_path.write_text(json.dumps(queue, indent=2))
print(f'Injected {added} new strategies (total: {len(queue)})')
for s in NEW:
    print(f'  [{s["id"]}] priority={s["priority"]} — {s["rationale"]}')
