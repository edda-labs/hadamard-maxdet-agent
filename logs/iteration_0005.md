# Hadamard Max-Det Research — Iteration 0005

**Timestamp:** 2026-04-28 01:28:44
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r16_c4` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `symmetric_0` (symmetric)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r16_c4` | 1,521,681,143,169,035 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 203,074,836,627,456 | 5.1808% | conference_paley |
| 3 | `symmetric_0` | 8,298,019,422,208 | 0.2117% | symmetric |
| 4 | `pad_4` | 2,815,959,236,608 | 0.0718% | circulant_fallback |
| 5 | `circulant_0` | 2,096,896,147,456 | 0.0535% | circulant |

---

## Analysis

**Top determinant:** 1,521,681,143,169,035 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,035 = (was 1,521,681,143,169,035)
  conference_paley: best=203,074,836,627,456 ↓ (was 205,649,241,702,402)
  symmetric: best=8,298,019,422,208 ↑ (was 110,922,563,584)
  circulant_fallback: best=2,815,959,236,608 ↓ (was 87,469,429,096,448)
  circulant: best=2,096,896,147,456 ↓ (was 77,922,253,668,352)
  Spread: 1,519,584,247,021,579 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 5)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        25

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (5 attempts)
  conference_paley: 205,649,241,702,402 (5 attempts)
  circulant_fallback: 87,469,429,096,448 (2 attempts)
  circulant: 77,922,253,668,352 (5 attempts)
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
  Iterations:        5
  Total tested:      25
