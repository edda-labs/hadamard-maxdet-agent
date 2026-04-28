# Hadamard Max-Det Research — Iteration 0013

**Timestamp:** 2026-04-28 05:34:03
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r15_c18` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `symmetric_0` (symmetric)
5. `pad_4` (circulant_fallback)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r15_c18` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 226,224,085,401,601 | 5.7714% | conference_paley |
| 3 | `pad_4` | 2,245,802,328,064 | 0.0573% | circulant_fallback |
| 4 | `circulant_0` | 1,784,101,732,352 | 0.0455% | circulant |
| 5 | `symmetric_0` | 64,223,182,848 | 0.0016% | symmetric |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=226,224,085,401,601 ↑ (was 205,649,241,702,402)
  circulant_fallback: best=2,245,802,328,064 ↓ (was 87,469,429,096,448)
  circulant: best=1,784,101,732,352 ↓ (was 77,922,253,668,352)
  symmetric: best=64,223,182,848 ↓ (was 8,298,019,422,208)
  Spread: 1,521,616,919,986,176 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 13)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        65

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (13 attempts)
  conference_paley: 226,224,085,401,601 (13 attempts)
  circulant_fallback: 87,469,429,096,448 (4 attempts)
  circulant: 77,922,253,668,352 (13 attempts)
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
  Iterations:        13
  Total tested:      65
