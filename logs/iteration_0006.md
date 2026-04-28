# Hadamard Max-Det Research — Iteration 0006

**Timestamp:** 2026-04-28 01:59:24
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r9_c8` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r9_c8` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 198,349,638,598,656 | 5.0603% | conference_paley |
| 3 | `circulant_0` | 1,123,482,075,136 | 0.0287% | circulant |
| 4 | `pad_4` | 38,247,858,176 | 0.0010% | circulant_fallback |
| 5 | `random_0` | 7,583,301,632 | 0.0002% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=198,349,638,598,656 ↓ (was 205,649,241,702,402)
  circulant: best=1,123,482,075,136 ↓ (was 77,922,253,668,352)
  circulant_fallback: best=38,247,858,176 ↓ (was 87,469,429,096,448)
  random: best=7,583,301,632 ↓ (was 23,957,864,448)
  Spread: 1,521,673,559,867,392 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 6)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        30

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (6 attempts)
  conference_paley: 205,649,241,702,402 (6 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (6 attempts)
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
  Iterations:        6
  Total tested:      30
