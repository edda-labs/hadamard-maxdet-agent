"""
constructions.py — Generate candidate 23×23 {±1} matrices.

Order n=23 is odd and 23≡3 mod 4, so:
- Hadamard matrices (n≡0 mod 4) impossible
- Barba bound (n≡1 mod 4) not applicable, and sqrt(45) isn't integer anyway
- Ehlich bound for n≡3 mod 4 applies

Construction strategies:
1. Submatrices of Hadamard matrices (24→23 by deleting row+col)
2. Paley core + border
3. Conference matrix construction (n = q+1 where q≡1 mod 4)
4. Block circulant / Toeplitz patterns
5. Symmetric / skew-symmetric structures
6. Williamson-type / Goethals-Seidel arrays
7. Randomized structured search
"""

import numpy as np
from typing import Optional

N = 23

# ============================================================================
# 1. Hadamard Submatrix (delete row+col from order 24 Hadamard)
# ============================================================================

def hadamard_sylvester(order: int) -> np.ndarray:
    """Sylvester construction: H_{2k} = H_2 ⊗ H_k (recursive)."""
    if order == 1:
        return np.array([[1]])
    if order == 2:
        return np.array([[1, 1], [1, -1]])
    H_half = hadamard_sylvester(order // 2)
    return np.kron(np.array([[1, 1], [1, -1]]), H_half)


def hadamard_24() -> np.ndarray:
    """
    Build a Hadamard matrix of order 24.
    Paley Type I: 24 = p+1 where p=23 ≡ 3 mod 4.
    Matrix: [Q+I  j; j^T  -1] where Q is 23×23 Paley core.
    """
    p = 23
    Q = paley_core(p)
    M = np.ones((24, 24), dtype=np.int8)
    M[:p, :p] = Q + np.eye(p, dtype=np.int8)
    M[p, p] = -1
    # The border row/column (all 1s) is correct for Paley Type I
    return M


def from_hadamard_submatrix(row_del: int = 0, col_del: int = 0) -> np.ndarray:
    """
    Take a 24×24 Hadamard matrix (Paley type), delete one row and one column,
    normalize to get a 23×23 candidate.
    """
    H24 = hadamard_24()
    M = np.delete(H24, row_del, axis=0)
    M = np.delete(M, col_del, axis=1)
    return M.astype(np.int8)


def from_hadamard_all_deletions() -> list[tuple[np.ndarray, str]]:
    """Generate all 24×24 = 576 submatrices by row/col deletion."""
    H24 = hadamard_24()
    results = []
    for r in range(24):
        for c in range(24):
            M = np.delete(np.delete(H24, r, axis=0), c, axis=1)
            results.append((M.astype(np.int8), f"had24_del_r{r}_c{c}"))
    return results


# ============================================================================
# 2. Paley Core Construction
# ============================================================================

def legendre_symbol(a: int, p: int) -> int:
    """Legendre symbol (a|p). Returns 1, -1, or 0."""
    if a % p == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def paley_core(p: int) -> np.ndarray:
    """
    Paley core Q of order p (p prime). Q[i][j] = legendre(i-j, p).
    Q is skew-symmetric if p ≡ 3 mod 4, symmetric if p ≡ 1 mod 4.
    """
    Q = np.zeros((p, p), dtype=np.int8)
    for i in range(p):
        for j in range(p):
            Q[i, j] = legendre_symbol(i - j, p)
    return Q


def paley_type1_matrix(p: int) -> np.ndarray:
    """
    Paley Type I Hadamard matrix of order p+1 (p ≡ 3 mod 4 prime).
    Not directly useful for n=23 (would need p=22, not prime), but
    we can use p=23 to build something.
    """
    Q = paley_core(p)
    # Build matrix: [Q+I  1; 1^T  -1]
    M = np.ones((p + 1, p + 1), dtype=np.int8)
    M[:p, :p] = Q + np.eye(p, dtype=np.int8)
    M[p, p] = -1
    return M


def conference_matrix(q: int) -> np.ndarray:
    """
    Conference matrix of order q+1 where q ≡ 1 mod 4 is a prime power.
    For n=23: q=22 is not a prime power. But we can build a 22×22
    conference matrix and border it for a 23×23 candidate.
    """
    # Since 22 is not a prime power ≡ 1 mod 4, we use a different approach.
    # Build from Paley-type structure for prime 23.
    Q = paley_core(23)  # 23×23 Paley core (skew-symmetric since 23 ≡ 3 mod 4)

    # For a conference matrix, we need symmetric Q.
    # Instead, build a bordered Paley matrix variant for order 23.
    # The core Q is skew-symmetric; we use it directly as a {±1,0} pattern
    # and fill diagonal with alternating ±1.
    M = Q.copy()

    # Set diagonal: alternating pattern
    for i in range(23):
        M[i, i] = 1 if i % 2 == 0 else -1

    return M.astype(np.int8)


# ============================================================================
# 3. Block Circulant Constructions
# ============================================================================

def random_circulant(seed: Optional[int] = None) -> np.ndarray:
    """Generate a random circulant 23×23 {±1} matrix."""
    rng = np.random.RandomState(seed)
    first_row = rng.choice([-1, 1], size=N)
    M = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        M[i] = np.roll(first_row, i)
    return M


def block_circulant(block_sizes: list[int],
                    seed: Optional[int] = None) -> np.ndarray:
    """
    Block-circulant matrix with specified block sizes.
    Each block is a circulant submatrix.
    """
    rng = np.random.RandomState(seed)
    M = np.zeros((N, N), dtype=np.int8)
    row_offset = 0
    for bsize in block_sizes:
        first_block_row = rng.choice([-1, 1], size=bsize)
        col_offset = 0
        for _ in block_sizes:
            for i in range(bsize):
                M[row_offset + i, col_offset:col_offset + bsize] = np.roll(
                    first_block_row, i)[:bsize]
            col_offset += bsize
        row_offset += bsize
    return M


def toeplitz_from_first_row_col(first_row: np.ndarray,
                                first_col: np.ndarray) -> np.ndarray:
    """Build a Toeplitz matrix from first row and column."""
    M = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        for j in range(N):
            if j >= i:
                M[i, j] = first_row[j - i]
            else:
                M[i, j] = first_col[i - j]
    return M


def random_toeplitz(seed: Optional[int] = None) -> np.ndarray:
    """Generate a random Toeplitz 23×23 {±1} matrix."""
    rng = np.random.RandomState(seed)
    first_row = rng.choice([-1, 1], size=N)
    first_col = rng.choice([-1, 1], size=N)
    first_col[0] = first_row[0]  # Ensure consistency
    return toeplitz_from_first_row_col(first_row, first_col)


# ============================================================================
# 4. Structured Search Helpers
# ============================================================================

def random_flip(matrix: np.ndarray, seed: Optional[int] = None,
                max_flips: int = 5) -> np.ndarray:
    """Randomly flip up to max_flips entries in a matrix."""
    rng = np.random.RandomState(seed)
    M = matrix.copy()
    n_flips = rng.randint(1, max_flips + 1)
    for _ in range(n_flips):
        i, j = rng.randint(0, N, 2)
        M[i, j] *= -1
    return M


def negate_row(matrix: np.ndarray, row: int) -> np.ndarray:
    """Negate a specific row."""
    M = matrix.copy()
    M[row] *= -1
    return M


def negate_col(matrix: np.ndarray, col: int) -> np.ndarray:
    """Negate a specific column."""
    M = matrix.copy()
    M[:, col] *= -1
    return M


# ============================================================================
# 5. Generation Pipeline
# ============================================================================

def generate_candidates(method: str, count: int = 5,
                        seed: Optional[int] = None) -> list[tuple[np.ndarray, str]]:
    """
    Generate candidate matrices using a specified method.
    Returns list of (matrix, name) tuples.
    """
    results = []
    rng = np.random.RandomState(seed)

    if method == "hadamard_submatrix":
        # Random row/col deletions from order 24 Hadamard (Paley type)
        H24 = hadamard_24()
        for i in range(count):
            r, c = rng.randint(0, 24, 2)
            M = np.delete(np.delete(H24, r, axis=0), c, axis=1)
            results.append((M.astype(np.int8), f"had_del_r{r}_c{c}"))

    elif method == "conference_paley":
        # Conference matrix from Paley core
        base = conference_matrix(23)  # Actually this is wrong, conf needs q≡1 mod 4
        for i in range(count):
            M = random_flip(base, seed=rng.randint(0, 2**31))
            results.append((M, f"conf_paley_flip{i}"))

    elif method == "circulant":
        for i in range(count):
            M = random_circulant(seed=rng.randint(0, 2**31))
            results.append((M, f"circulant_{i}"))

    elif method == "toeplitz":
        for i in range(count):
            M = random_toeplitz(seed=rng.randint(0, 2**31))
            results.append((M, f"toeplitz_{i}"))

    elif method == "block_circulant":
        # Try various factorizations of 23 (prime! only 1×23 or 23×1)
        # For 23, block sizes must sum to 23
        for i in range(count):
            # Try (11, 12) — only non-trivial split close to equal
            M = block_circulant([11, 12], seed=rng.randint(0, 2**31))
            results.append((M, f"block_circ_11_12_{i}"))

    elif method == "random":
        for i in range(count):
            M = rng.choice([-1, 1], size=(N, N)).astype(np.int8)
            results.append((M, f"random_{i}"))

    elif method == "skew_symmetric":
        # Skew-symmetric: M[i,j] = -M[j,i] for i≠j, diagonal = 1
        for i in range(count):
            M = rng.choice([-1, 1], size=(N, N)).astype(np.int8)
            # Make skew-symmetric
            for r_i in range(N):
                for c_i in range(r_i + 1, N):
                    M[c_i, r_i] = -M[r_i, c_i]
            np.fill_diagonal(M, 1)
            results.append((M, f"skew_sym_{i}"))

    elif method == "symmetric":
        for i in range(count):
            upper = rng.choice([-1, 1], size=(N, N)).astype(np.int8)
            M = np.triu(upper) + np.triu(upper, 1).T
            np.fill_diagonal(M, rng.choice([-1, 1], size=N))
            results.append((M, f"symmetric_{i}"))

    elif method == "negacyclic":
        # Negacyclic: M[i,j] = -M[i-1, j-1] (wraparound)
        for i in range(count):
            first_row = rng.choice([-1, 1], size=N)
            M = np.zeros((N, N), dtype=np.int8)
            for r_i in range(N):
                for c_i in range(N):
                    pos = (c_i - r_i) % N
                    M[r_i, c_i] = first_row[pos] if r_i == 0 else M[r_i - 1, c_i - 1] * (-1)
                    # Wait, negacyclic means each row is negated of previous shifted
            # Let me just do it properly
            M = np.zeros((N, N), dtype=np.int8)
            M[0] = first_row
            for r_i in range(1, N):
                M[r_i, 0] = -M[r_i - 1, N - 1]
                M[r_i, 1:] = -M[r_i - 1, :-1]
            results.append((M, f"negacyclic_{i}"))

    else:
        raise ValueError(f"Unknown method: {method}")

    return results


# Methods auto-selected by the programmatic fallback.
# `hadamard_submatrix` is excluded: by Sharpe's identity every (n-1)x(n-1)
# minor of an n-Hadamard matrix has |det| = n^((n-2)/2), so all 576 deletions
# of H24 give |det| = 24^11. Re-running it can't improve anything; strategies
# that want H24 deletions as a starting point still call hadamard_24() directly.
# `block_circulant` is excluded: 23 is prime, so no non-trivial block-circulant
# of order 23 exists, and the [11,12] split in the old code crashed anyway.
CONSTRUCTION_METHODS = [
    "conference_paley",
    "circulant",
    "toeplitz",
    "random",
    "skew_symmetric",
    "symmetric",
    "negacyclic",
]
