# Hadamard Max-Det Research — Iteration 0004

**Timestamp:** 2026-04-28 00:58:14
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r1_c18` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `toeplitz_0` (toeplitz)
5. `skew_sym_0` (skew_symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r1_c18` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 123,164,235,399,168 | 3.1422% | conference_paley |
| 3 | `circulant_0` | 77,922,253,668,352 | 1.9880% | circulant |
| 4 | `skew_sym_0` | 2,137,752,862,720 | 0.0545% | skew_symmetric |
| 5 | `toeplitz_0` | 321,183,023,104 | 0.0082% | toeplitz |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=123,164,235,399,168 ↓ (was 205,649,241,702,402)
  circulant: best=77,922,253,668,352 ↑ (was 54,557,279,256,576)
  skew_symmetric: best=2,137,752,862,720 ↑ (was 0)
  toeplitz: best=321,183,023,104 ↑ (was 0)
  Spread: 1,521,359,960,145,920 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 4)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        20

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (4 attempts)
  conference_paley: 205,649,241,702,402 (4 attempts)
  circulant_fallback: 87,469,429,096,448 (1 attempts)
  circulant: 77,922,253,668,352 (4 attempts)
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
  Iterations:        4
  Total tested:      20
