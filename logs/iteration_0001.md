# Hadamard Max-Det Research — Iteration 0001

**Timestamp:** 2026-04-28 00:27:12
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r18_c15` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `symmetric_0` (symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r18_c15` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 103,575,808,114,688 | 2.6424% | conference_paley |
| 3 | `circulant_0` | 54,557,279,256,576 | 1.3919% | circulant |
| 4 | `symmetric_0` | 110,922,563,584 | 0.0028% | symmetric |
| 5 | `random_0` | 2,290,089,984 | 0.0001% | random |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↑ (was 0)
  conference_paley: best=103,575,808,114,688 ↑ (was 0)
  circulant: best=54,557,279,256,576 ↑ (was 0)
  symmetric: best=110,922,563,584 ↑ (was 0)
  random: best=2,290,089,984 ↑ (was 0)
  Spread: 1,521,678,853,079,040 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 1)**
  Best determinant:    0
  vs. best known:      2,779,447,296,000,000 (0.00%)
  vs. Barba bound:     3,919,726,327,358,822 (0.0000%)
  Total tested:        0

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
  Iterations:        1
  Total tested:      5
