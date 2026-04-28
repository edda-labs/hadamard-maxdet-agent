# Hadamard Max-Det Research — Iteration 0011

**Timestamp:** 2026-04-28 04:32:52
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r15_c19` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `toeplitz_0` (toeplitz)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r15_c19` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 167,841,449,902,081 | 4.2820% | conference_paley |
| 3 | `circulant_0` | 38,804,857,552,896 | 0.9900% | circulant |
| 4 | `toeplitz_0` | 164,316,053,504 | 0.0042% | toeplitz |
| 5 | `random_0` | 20,338,180,096 | 0.0005% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=167,841,449,902,081 ↓ (was 205,649,241,702,402)
  circulant: best=38,804,857,552,896 ↓ (was 77,922,253,668,352)
  toeplitz: best=164,316,053,504 ↓ (was 700,562,014,208)
  random: best=20,338,180,096 ↓ (was 72,209,137,664)
  Spread: 1,521,660,804,988,928 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 11)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        55

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (11 attempts)
  conference_paley: 205,649,241,702,402 (11 attempts)
  circulant_fallback: 87,469,429,096,448 (3 attempts)
  circulant: 77,922,253,668,352 (11 attempts)
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
  Iterations:        11
  Total tested:      55
