# Hadamard Max-Det Research — Iteration 0014

**Timestamp:** 2026-04-28 06:04:41
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r1_c13` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `random_0` (random)
5. `symmetric_0` (symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r1_c13` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 127,766,032,809,984 | 3.2596% | conference_paley |
| 3 | `random_0` | 48,737,812,480 | 0.0012% | random |
| 4 | `circulant_0` | 13,895,729,152 | 0.0004% | circulant |
| 5 | `symmetric_0` | 11,211,374,592 | 0.0003% | symmetric |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=127,766,032,809,984 ↓ (was 226,224,085,401,601)
  random: best=48,737,812,480 ↓ (was 72,209,137,664)
  circulant: best=13,895,729,152 ↓ (was 77,922,253,668,352)
  symmetric: best=11,211,374,592 ↓ (was 8,298,019,422,208)
  Spread: 1,521,669,931,794,432 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 14)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        70

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (14 attempts)
  conference_paley: 226,224,085,401,601 (14 attempts)
  circulant_fallback: 87,469,429,096,448 (4 attempts)
  circulant: 77,922,253,668,352 (14 attempts)
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
  Iterations:        14
  Total tested:      70
