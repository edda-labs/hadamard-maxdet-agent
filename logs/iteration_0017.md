# Hadamard Max-Det Research — Iteration 0017

**Timestamp:** 2026-04-28 07:37:14
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `had_del_r18_c3` (hadamard_submatrix)
2. `conf_paley_flip0` (conference_paley)
3. `circulant_0` (circulant)
4. `symmetric_0` (symmetric)
5. `skew_sym_0` (skew_symmetric)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `had_del_r18_c3` | 1,521,681,143,169,024 | 38.8211% | hadamard_submatrix |
| 2 | `conf_paley_flip0` | 108,379,297,021,952 | 2.7650% | conference_paley |
| 3 | `circulant_0` | 11,820,551,110,656 | 0.3016% | circulant |
| 4 | `skew_sym_0` | 8,349,869,408,256 | 0.2130% | skew_symmetric |
| 5 | `symmetric_0` | 56,925,093,888 | 0.0015% | symmetric |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: hadamard_submatrix
  Improves record? No

**Method performance this iteration:**
  hadamard_submatrix: best=1,521,681,143,169,024 ↓ (was 1,521,681,143,169,035)
  conference_paley: best=108,379,297,021,952 ↓ (was 226,224,085,401,601)
  circulant: best=11,820,551,110,656 ↓ (was 77,922,253,668,352)
  skew_symmetric: best=8,349,869,408,256 ↑ (was 5,396,458,635,264)
  symmetric: best=56,925,093,888 ↓ (was 8,298,019,422,208)
  Spread: 1,521,624,218,075,136 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 17)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        85

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  conference_paley: 226,224,085,401,601 (17 attempts)
  circulant_fallback: 87,469,429,096,448 (6 attempts)
  circulant: 77,922,253,668,352 (17 attempts)
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
  Iterations:        17
  Total tested:      85
