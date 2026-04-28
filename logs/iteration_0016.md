# Hadamard Max-Det Research — Iteration 0016

**Timestamp:** 2026-04-28 07:05:54
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r22_c13` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `symmetric_0` (symmetric)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r22_c13` | 1,521,681,143,169,013 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 52,149,882,978,304 | 1.3304% | conference_paley |
| 3 | `pad_4` | 17,053,624,827,904 | 0.4351% | circulant_fallback |
| 4 | `circulant_0` | 7,377,969,479,680 | 0.1882% | circulant |
| 5 | `symmetric_0` | 140,614,041,600 | 0.0036% | symmetric |

---

## Analysis

**Top determinant:** 1,521,681,143,169,013 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,013 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=52,149,882,978,304 ↓ (was 226,224,085,401,601)
  circulant_fallback: best=17,053,624,827,904 ↓ (was 87,469,429,096,448)
  circulant: best=7,377,969,479,680 ↓ (was 77,922,253,668,352)
  symmetric: best=140,614,041,600 ↓ (was 8,298,019,422,208)
  Spread: 1,521,540,529,127,413 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 16)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        80

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (16 attempts)
  conference_paley: 226,224,085,401,601 (16 attempts)
  circulant_fallback: 87,469,429,096,448 (6 attempts)
  circulant: 77,922,253,668,352 (16 attempts)
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
  Iterations:        16
  Total tested:      80
