# Hadamard Max-Det Research — Iteration 0015

**Timestamp:** 2026-04-28 06:35:13
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r3_c19` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `toeplitz_0` (toeplitz)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r3_c19` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 117,171,720,028,160 | 2.9893% | conference_paley |
| 3 | `pad_4` | 24,079,830,614,016 | 0.6143% | circulant_fallback |
| 4 | `circulant_0` | 11,311,379,382,272 | 0.2886% | circulant |
| 5 | `toeplitz_0` | 1,163,806,113,792 | 0.0297% | toeplitz |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=117,171,720,028,160 ↓ (was 226,224,085,401,601)
  circulant_fallback: best=24,079,830,614,016 ↓ (was 87,469,429,096,448)
  circulant: best=11,311,379,382,272 ↓ (was 77,922,253,668,352)
  toeplitz: best=1,163,806,113,792 ↑ (was 700,562,014,208)
  Spread: 1,520,517,337,055,232 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 15)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        75

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (15 attempts)
  conference_paley: 226,224,085,401,601 (15 attempts)
  circulant_fallback: 87,469,429,096,448 (5 attempts)
  circulant: 77,922,253,668,352 (15 attempts)
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
  Iterations:        15
  Total tested:      75
