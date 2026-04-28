# Hadamard Max-Det Research — Iteration 0009

**Timestamp:** 2026-04-28 03:31:16
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r10_c7` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `skew_sym_0` (skew_symmetric)
5. `toeplitz_0` (toeplitz)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r10_c7` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 90,617,220,694,017 | 2.3118% | conference_paley |
| 3 | `circulant_0` | 44,603,424,112,640 | 1.1379% | circulant |
| 4 | `skew_sym_0` | 5,396,458,635,264 | 0.1377% | skew_symmetric |
| 5 | `toeplitz_0` | 700,562,014,208 | 0.0179% | toeplitz |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=90,617,220,694,017 ↓ (was 205,649,241,702,402)
  circulant: best=44,603,424,112,640 ↓ (was 77,922,253,668,352)
  skew_symmetric: best=5,396,458,635,264 ↑ (was 4,690,079,121,408)
  toeplitz: best=700,562,014,208 ↑ (was 423,297,548,288)
  Spread: 1,520,980,581,154,816 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 9)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        45

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (9 attempts)
  conference_paley: 205,649,241,702,402 (9 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (9 attempts)
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
  Iterations:        9
  Total tested:      45
