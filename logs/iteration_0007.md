# Hadamard Max-Det Research — Iteration 0007

**Timestamp:** 2026-04-28 02:30:02
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r22_c16` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `toeplitz_0` (toeplitz)
5. `skew_sym_0` (skew_symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r22_c16` | 1,521,681,143,169,013 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 163,450,919,583,744 | 4.1700% | conference_paley |
| 3 | `circulant_0` | 17,577,644,392,448 | 0.4484% | circulant |
| 4 | `skew_sym_0` | 4,690,079,121,408 | 0.1197% | skew_symmetric |
| 5 | `toeplitz_0` | 423,297,548,288 | 0.0108% | toeplitz |

---

## Analysis

**Top determinant:** 1,521,681,143,169,013 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,013 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=163,450,919,583,744 ↓ (was 205,649,241,702,402)
  circulant: best=17,577,644,392,448 ↓ (was 77,922,253,668,352)
  skew_symmetric: best=4,690,079,121,408 ↑ (was 2,137,752,862,720)
  toeplitz: best=423,297,548,288 ↑ (was 321,183,023,104)
  Spread: 1,521,257,845,620,725 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 7)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        35

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (7 attempts)
  conference_paley: 205,649,241,702,402 (7 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (7 attempts)
  negacyclic: 32,708,780,621,824 (1 attempts)

---

## Next Plan

**Strategy: BASELINE** — gathering initial data across methods
  Continue diverse exploration

**Next iteration candidate sources:**
  1. More row/col deletion pairs from H24 (576 total, only N tested so far)
  2. Try negating rows/cols of best deletion candidate

---

## State Summary

Best determinant found: 1,521,681,143,169,035
  vs. best known:   2,779,447,296,000,000
  Barba bound:      3,919,726,327,358,822 (38.82%)
  Construction:      hadamard_submatrix
  Iterations:        7
  Total tested:      35
