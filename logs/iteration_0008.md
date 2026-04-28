# Hadamard Max-Det Research — Iteration 0008

**Timestamp:** 2026-04-28 03:00:33
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r13_c15` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `toeplitz_0` (toeplitz)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r13_c15` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 100,665,007,276,032 | 2.5682% | conference_paley |
| 3 | `toeplitz_0` | 257,844,838,400 | 0.0066% | toeplitz |
| 4 | `circulant_0` | 212,437,303,296 | 0.0054% | circulant |
| 5 | `random_0` | 72,209,137,664 | 0.0018% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=100,665,007,276,032 ↓ (was 205,649,241,702,402)
  toeplitz: best=257,844,838,400 ↓ (was 423,297,548,288)
  circulant: best=212,437,303,296 ↓ (was 77,922,253,668,352)
  random: best=72,209,137,664 ↑ (was 23,957,864,448)
  Spread: 1,521,608,934,031,360 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 8)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        40

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (8 attempts)
  conference_paley: 205,649,241,702,402 (8 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (8 attempts)
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
  Iterations:        8
  Total tested:      40
