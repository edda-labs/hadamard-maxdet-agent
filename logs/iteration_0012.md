# Hadamard Max-Det Research — Iteration 0012

**Timestamp:** 2026-04-28 05:03:30
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r13_c14` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `symmetric_0` (symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r13_c14` | 1,521,681,143,169,035 | 38.8211% | hadamard_submatrix |
| 2 | `circulant_0` | 62,521,574,686,720 | 1.5950% | circulant |
| 3 | `conf_paley_flip0` | 6,655,970,377,728 | 0.1698% | conference_paley |
| 4 | `symmetric_0` | 192,250,118,144 | 0.0049% | symmetric |
| 5 | `random_0` | 19,285,409,792 | 0.0005% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,035 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,035 = (was 1,521,681,143,169,035)
  circulant: best=62,521,574,686,720 ↓ (was 77,922,253,668,352)
  conference_paley: best=6,655,970,377,728 ↓ (was 205,649,241,702,402)
  symmetric: best=192,250,118,144 ↓ (was 8,298,019,422,208)
  random: best=19,285,409,792 ↓ (was 72,209,137,664)
  Spread: 1,521,661,857,759,243 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 12)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        60

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (12 attempts)
  conference_paley: 205,649,241,702,402 (12 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (12 attempts)
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
  Iterations:        12
  Total tested:      60
