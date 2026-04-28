"""
New strategies for Hadamard max-det research - ORDER 23.
Target: break the 24^11 plateau (1.52e15) to approach the record 2.78e15.

Key mathematical insight: All single-row/col deletions from any H24 give det = 24^11.
The Paley core + I also gives 24^11. To break through, we need matrices whose
Gram matrix is NOT of the form 24I - J (or simple variants).

Strategy 1: Diagonal-varied Paley - M = Q + D where D is non-constant diagonal.
  Gram matrix: G = 24I - J + (QD - DQ). The commutator adds structure.

Strategy 2: Hadamard equivalence orbit - Apply random equivalence transforms
  to H24 before deletion, then LOCAL FLIPS to break 24^11 invariance.

Strategy 3: Simulated annealing on best H24 submatrices.

Strategy 4: Symmetric Legendre-pattern matrices from multiplicative characters mod 23.

Strategy 5: Coordinate exchange (D-optimal design algorithm) on best starting points.
"""

SEED_STRATEGIES = [
    {
        "id": "hermod_diagonal_paley",
        "code": (
            '# Diagonal-varied Paley: M = Q + D where D diagonal has strategic +/-1\n'
            '# The Gram matrix is G = 24I - J + (QD - DQ) - commutator changes structure\n'
            'import numpy as np\n'
            'from constructions import paley_core\n'
            '\n'
            'def generate_matrices():\n'
            '    Q = paley_core(23).astype(np.int8)\n'
            '    results = []\n'
            '    \n'
            '    # Pattern 1: All +1 diagonal\n'
            '    M1 = Q.copy()\n'
            '    np.fill_diagonal(M1, 1)\n'
            '    results.append((M1, "paley_pos_diag"))\n'
            '    \n'
            '    # Pattern 2: All -1 diagonal (maximizes commutator)\n'
            '    M2 = Q.copy()\n'
            '    np.fill_diagonal(M2, -1)\n'
            '    results.append((M2, "paley_neg_diag"))\n'
            '    \n'
            '    # Pattern 3: Quadratic residue-based diagonal\n'
            '    residues = {pow(i, 2, 23) for i in range(1, 23)}\n'
            '    D3 = np.array([1 if i in residues else -1 for i in range(23)], dtype=np.int8)\n'
            '    M3 = Q.copy()\n'
            '    M3[np.arange(23), np.arange(23)] = D3\n'
            '    results.append((M3, "paley_qr_diag"))\n'
            '    \n'
            '    # Pattern 4: Alternating blocks of 4: +,+,-,-,...\n'
            '    D4 = np.tile(np.array([1,1,-1,-1], dtype=np.int8), 6)[:23]\n'
            '    M4 = Q.copy()\n'
            '    M4[np.arange(23), np.arange(23)] = D4\n'
            '    results.append((M4, "paley_alt4_diag"))\n'
            '    \n'
            '    # Pattern 5: First half +1, second half -1\n'
            '    D5 = np.ones(23, dtype=np.int8)\n'
            '    D5[11:] = -1\n'
            '    M5 = Q.copy()\n'
            '    M5[np.arange(23), np.arange(23)] = D5\n'
            '    results.append((M5, "paley_split_diag"))\n'
            '    \n'
            '    return results\n'
        ),
        "rationale": "Diagonal-varied Paley core - non-constant D adds commutator QD-DQ to Gram matrix, potentially exceeding 24^11",
        "priority": 9,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "hermod_equivalence_orbit",
        "code": (
            '# Apply Hadamard equivalence transformations to H24 BEFORE deleting row/col,\n'
            '# then apply local sign flips to break out of the 24^11 equivalence class.\n'
            '# Different equivalence transforms give structurally different 23x23 matrices.\n'
            'import numpy as np\n'
            'from constructions import hadamard_24\n'
            '\n'
            'def apply_equiv(H, row_signs, col_signs, row_perm, col_perm):\n'
            '    # Apply Hadamard equivalence: R * H * C\n'
            '    H2 = H.copy().astype(np.int8)\n'
            '    H2 = H2 * row_signs[:, np.newaxis]\n'
            '    H2 = H2 * col_signs[np.newaxis, :]\n'
            '    H2 = H2[row_perm, :]\n'
            '    H2 = H2[:, col_perm]\n'
            '    return H2\n'
            '\n'
            'def generate_matrices():\n'
            '    H24 = hadamard_24()\n'
            '    rng = np.random.RandomState(789)\n'
            '    results = []\n'
            '    \n'
            '    for variant in range(5):\n'
            '        # Random equivalence transformation\n'
            '        row_signs = rng.choice([-1, 1], size=24).astype(np.int8)\n'
            '        col_signs = rng.choice([-1, 1], size=24).astype(np.int8)\n'
            '        row_perm = rng.permutation(24)\n'
            '        col_perm = rng.permutation(24)\n'
            '        \n'
            '        H_transformed = apply_equiv(H24, row_signs, col_signs, row_perm, col_perm)\n'
            '        \n'
            '        # Delete row/col to get 23x23\n'
            '        r_del = variant * 4\n'
            '        c_del = (variant * 4 + 7) % 24\n'
            '        M = np.delete(np.delete(H_transformed, r_del, axis=0), c_del, axis=1).astype(np.int8)\n'
            '        \n'
            '        # CRITICAL: Apply strategic local flips to break det=24^11 invariant\n'
            '        M_perturbed = M.copy()\n'
            '        # Flip a 3x3 block in the upper left\n'
            '        M_perturbed[0:3, 0:3] *= -1\n'
            '        # Flip every 5th entry on the diagonal\n'
            '        for i in range(0, 23, 5):\n'
            '            M_perturbed[i, i] *= -1\n'
            '        \n'
            '        results.append((M_perturbed, f"equiv_perturb_v{variant}"))\n'
            '    \n'
            '    return results\n'
        ),
        "rationale": "Hadamard equivalence orbit search - different H24 transforms give structurally diverse 23x23 bases for perturbation",
        "priority": 8,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "hermod_simulated_annealing",
        "code": (
            '# Simulated annealing on best H24 submatrices.\n'
            '# Uses Metropolis criterion with det-based temperature.\n'
            '# Multiple starting points, multiple SA runs.\n'
            'import numpy as np\n'
            'from constructions import hadamard_24\n'
            '\n'
            'def generate_matrices():\n'
            '    N = 23\n'
            '    H24 = hadamard_24()\n'
            '    rng = np.random.RandomState(314159)\n'
            '    results = []\n'
            '    \n'
            '    # Starting points: best H24 deletions\n'
            '    start_pairs = [(10, 3), (16, 4), (13, 14), (18, 15), (9, 8)]\n'
            '    \n'
            '    for variant, (r_del, c_del) in enumerate(start_pairs):\n'
            '        M = np.delete(np.delete(H24, r_del, axis=0), c_del, axis=1).astype(np.int8)\n'
            '        \n'
            '        # Simulated annealing\n'
            '        T0 = 5e13  # Initial temperature\n'
            '        current_M = M.copy()\n'
            '        current_det = abs(int(round(np.linalg.det(current_M.astype(np.float64)))))\n'
            '        best_M = current_M.copy()\n'
            '        best_det = current_det\n'
            '        \n'
            '        for step in range(300):\n'
            '            T = T0 / (1 + np.log(1 + step))\n'
            '            \n'
            '            # Propose: flip a random entry\n'
            '            fi, fj = rng.randint(0, N, size=2)\n'
            '            current_M[fi, fj] *= -1\n'
            '            \n'
            '            new_det = abs(int(round(np.linalg.det(current_M.astype(np.float64)))))\n'
            '            delta = new_det - current_det\n'
            '            \n'
            '            if delta > 0 or (T > 1 and rng.random() < np.exp(delta / T)):\n'
            '                current_det = new_det\n'
            '                if current_det > best_det:\n'
            '                    best_det = current_det\n'
            '                    best_M = current_M.copy()\n'
            '            else:\n'
            '                current_M[fi, fj] *= -1  # Reject\n'
            '        \n'
            '        results.append((best_M, f"sa_best_v{variant}"))\n'
            '    \n'
            '    return results\n'
        ),
        "rationale": "Simulated annealing on top H24 submatrices - stochastic search to escape 24^11 plateau",
        "priority": 7,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "hermod_legendre_symmetric",
        "code": (
            '# Symmetric +/-1 matrices constructed from multiplicative characters mod 23.\n'
            '# Unlike the Paley core (skew-symmetric), these are SYMMETRIC with\n'
            '# carefully chosen sign patterns based on quadratic residues and cosets.\n'
            'import numpy as np\n'
            '\n'
            'def generate_matrices():\n'
            '    N = 23\n'
            '    MOD = 23\n'
            '    # Quadratic residues mod 23\n'
            '    qr = set()\n'
            '    for i in range(1, MOD):\n'
            '        qr.add(pow(i, 2, MOD))\n'
            '    \n'
            '    results = []\n'
            '    \n'
            '    for variant in range(5):\n'
            '        M = np.zeros((N, N), dtype=np.int8)\n'
            '        \n'
            '        for i in range(N):\n'
            '            for j in range(N):\n'
            '                if i == j:\n'
            '                    if variant == 0:\n'
            '                        M[i, j] = 1\n'
            '                    elif variant == 1:\n'
            '                        M[i, j] = 1 if i in qr else -1\n'
            '                    elif variant == 2:\n'
            '                        M[i, j] = 1 if i % 2 == 0 else -1\n'
            '                    elif variant == 3:\n'
            '                        M[i, j] = 1 if i < 12 else -1\n'
            '                    else:\n'
            '                        # Based on multiplicative order mod 23\n'
            '                        # Primitive root is 5; entries with order dividing (p-1)/2\n'
            '                        M[i, j] = 1 if pow(5, i, 23) < 12 else -1\n'
            '                else:\n'
            '                    d = (i - j) % MOD\n'
            '                    if variant == 0:\n'
            '                        # Pure QR pattern (symmetric, unlike Paley)\n'
            '                        M[i, j] = 1 if d in qr else -1\n'
            '                    elif variant == 1:\n'
            '                        # Product of Legendre symbols\n'
            '                        li = 1 if (i == 0 or i in qr) else -1\n'
            '                        lj = 1 if (j == 0 or j in qr) else -1\n'
            '                        M[i, j] = li * lj * (1 if d in qr else -1)\n'
            '                    elif variant == 2:\n'
            '                        # Sum index pattern: (i+j) mod 23\n'
            '                        s = (i + j) % MOD\n'
            '                        M[i, j] = 1 if (s == 0 or s in qr) else -1\n'
            '                    elif variant == 3:\n'
            '                        # Sum-of-squares pattern\n'
            '                        s = (i*i + j*j) % MOD\n'
            '                        M[i, j] = 1 if (s == 0 or s in qr) else -1\n'
            '                    else:\n'
            '                        # Product index pattern: (i*j) mod 23\n'
            '                        p = (i * j) % MOD\n'
            '                        M[i, j] = 1 if (p == 0 or p in qr) else -1\n'
            '        \n'
            '        results.append((M, f"legendre_sym_v{variant}"))\n'
            '    \n'
            '    return results\n'
        ),
        "rationale": "Symmetric matrices from multiplicative characters mod 23 - structurally different from Paley, may yield higher det",
        "priority": 7,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
    {
        "id": "hermod_coordinate_exchange",
        "code": (
            '# Coordinate exchange algorithm for D-optimal design.\n'
            '# Greedy: for each entry, try flipping; if det improves, keep it.\n'
            '# Multiple passes until convergence or max iterations.\n'
            '# Start from best matrices, not random.\n'
            'import numpy as np\n'
            'from constructions import hadamard_24, paley_core\n'
            '\n'
            'def generate_matrices():\n'
            '    N = 23\n'
            '    H24 = hadamard_24()\n'
            '    Q = paley_core(23)\n'
            '    results = []\n'
            '    \n'
            '    # Best starting points from state\n'
            '    starts = []\n'
            '    starts.append(np.delete(np.delete(H24, 10, axis=0), 3, axis=1).astype(np.int8))\n'
            '    starts.append(np.delete(np.delete(H24, 16, axis=0), 4, axis=1).astype(np.int8))\n'
            '    starts.append(np.delete(np.delete(H24, 13, axis=0), 14, axis=1).astype(np.int8))\n'
            '    \n'
            '    # Paley + diagonal variants\n'
            '    for diag_fill in [1, -1]:\n'
            '        M = Q.copy().astype(np.int8)\n'
            '        np.fill_diagonal(M, diag_fill)\n'
            '        starts.append(M)\n'
            '    \n'
            '    for idx, start_M in enumerate(starts[:5]):\n'
            '        M = start_M.copy()\n'
            '        best_M = M.copy()\n'
            '        best_det = abs(int(round(np.linalg.det(M.astype(np.float64)))))\n'
            '        \n'
            '        N_entries = N * N\n'
            '        for iteration in range(5):  # Multiple passes\n'
            '            improved = False\n'
            '            order = np.random.permutation(N_entries)\n'
            '            for pos in order:\n'
            '                i, j = divmod(pos, N)\n'
            '                M[i, j] *= -1\n'
            '                new_det = abs(int(round(np.linalg.det(M.astype(np.float64)))))\n'
            '                if new_det > best_det:\n'
            '                    best_det = new_det\n'
            '                    best_M = M.copy()\n'
            '                    improved = True\n'
            '                else:\n'
            '                    M[i, j] *= -1  # Revert\n'
            '            if not improved:\n'
            '                break\n'
            '        \n'
            '        results.append((best_M, f"coord_exchange_{idx}"))\n'
            '    \n'
            '    return results\n'
        ),
        "rationale": "Coordinate exchange (D-optimal design) - greedy entry-by-entry optimization from best starting points",
        "priority": 6,
        "created_by": "hermod",
        "attempts": 0,
        "best_det": 0,
        "best_name": None,
    },
]
