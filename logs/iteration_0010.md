# Hadamard Max-Det Research — Iteration 0010

**Timestamp:** 2026-04-28 04:02:08
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r17_c12` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `toeplitz_0` (toeplitz)
5. `skew_sym_0` (skew_symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r17_c12` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 14,045,549,690,880 | 0.3583% | conference_paley |
| 3 | `skew_sym_0` | 3,243,044,241,408 | 0.0827% | skew_symmetric |
| 4 | `circulant_0` | 2,270,305,452,032 | 0.0579% | circulant |
| 5 | `toeplitz_0` | 429,270,237,184 | 0.0110% | toeplitz |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=14,045,549,690,880 ↓ (was 205,649,241,702,402)
  skew_symmetric: best=3,243,044,241,408 ↓ (was 5,396,458,635,264)
  circulant: best=2,270,305,452,032 ↓ (was 77,922,253,668,352)
  toeplitz: best=429,270,237,184 ↓ (was 700,562,014,208)
  Spread: 1,521,251,872,931,840 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 10)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        50

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (10 attempts)
  conference_paley: 205,649,241,702,402 (10 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (10 attempts)
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
  Iterations:        10
  Total tested:      50
