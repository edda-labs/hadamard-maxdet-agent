# Hadamard Max-Det Research — Iteration 0002

**Timestamp:** 2026-04-28 00:27:43
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r12_c5` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r12_c5` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 154,122,519,052,288 | 3.9320% | conference_paley |
| 3 | `pad_4` | 87,469,429,096,448 | 2.2315% | circulant_fallback |
| 4 | `circulant_0` | 491,450,793,984 | 0.0125% | circulant |
| 5 | `random_0` | 23,957,864,448 | 0.0006% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 = (was 1,521,681,143,169,024)
  conference_paley: best=154,122,519,052,288 ↑ (was 103,575,808,114,688)
  circulant_fallback: best=87,469,429,096,448 ↑ (was 0)
  circulant: best=491,450,793,984 ↓ (was 54,557,279,256,576)
  random: best=23,957,864,448 ↑ (was 2,290,089,984)
  Spread: 1,521,657,185,304,576 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 2)**
  Best determinant:    1,521,681,143,169,024
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        10

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,024 (2 attempts)
  conference_paley: 154,122,519,052,288 (2 attempts)
  circulant_fallback: 87,469,429,096,448 (1 attempts)
  circulant: 54,557,279,256,576 (2 attempts)
  symmetric: 110,922,563,584 (1 attempts)

---

## Next Plan

**Strategy: BASELINE** — gathering initial data across methods
  Continue diverse exploration

**Next iteration candidate sources:**
  1. More row/col deletion pairs from H24 (576 total, only N tested so far)
  2. Try negating rows/cols of best deletion candidate

---

## State Summary

Best determinant found: 1,521,681,143,169,024
  vs. best known:   2,779,447,296,000,000
  Barba bound:      3,919,726,327,358,822 (38.82%)
  Construction:      hadamard_submatrix
  Iterations:        2
  Total tested:      10
