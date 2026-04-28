# Hadamard Max-Det Research — Iteration 0003

**Timestamp:** 2026-04-28 00:27:47
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r10_c3` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `negacyclic_0` (negacyclic)
5. `random_0` (random)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r10_c3` | 1,521,681,143,169,035 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 205,649,241,702,402 | 5.2465% | conference_paley |
| 3 | `negacyclic_0` | 32,708,780,621,824 | 0.8345% | negacyclic |
| 4 | `circulant_0` | 691,686,866,944 | 0.0176% | circulant |
| 5 | `random_0` | 22,385,000,448 | 0.0006% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,035 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,035 ↑ (was 1,521,681,143,169,024)
  conference_paley: best=205,649,241,702,402 ↑ (was 154,122,519,052,288)
  negacyclic: best=32,708,780,621,824 ↑ (was 0)
  circulant: best=691,686,866,944 ↓ (was 54,557,279,256,576)
  random: best=22,385,000,448 ↓ (was 23,957,864,448)
  Spread: 1,521,658,758,168,587 (max-min)
  Improvement over session best: +0.0000%

---

## Self-Assessment

**Overall Progress (Iteration 3)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        15

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (3 attempts)
  conference_paley: 205,649,241,702,402 (3 attempts)
  circulant_fallback: 87,469,429,096,448 (1 attempts)
  circulant: 54,557,279,256,576 (3 attempts)
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
  Iterations:        3
  Total tested:      15
