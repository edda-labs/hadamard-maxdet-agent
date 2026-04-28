# Hadamard Max-Det Research — Iteration 0018

**Timestamp:** 2026-04-28 07:39:22
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `local_search_corners_r0_c0` (strategy_seed_local_flip)
2. `local_search_corners_r5_c7` (strategy_seed_local_flip)
3. `local_search_corners_r11_c13` (strategy_seed_local_flip)
4. `local_search_corners_r17_c19` (strategy_seed_local_flip)
5. `local_search_corners_r23_c1` (strategy_seed_local_flip)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `local_search_corners_r11_c13` | 1,178,833,231,282,172 | 30.0744% | strategy_seed_local_flip |
| 2 | `local_search_corners_r17_c19` | 1,046,938,543,718,400 | 26.7095% | strategy_seed_local_flip |
| 3 | `local_search_corners_r23_c1` | 1,017,585,126,604,801 | 25.9606% | strategy_seed_local_flip |
| 4 | `local_search_corners_r5_c7` | 999,973,076,336,636 | 25.5113% | strategy_seed_local_flip |
| 5 | `local_search_corners_r0_c0` | 489,223,618,560,002 | 12.4811% | strategy_seed_local_flip |

---

## Analysis

**Top determinant:** 1,178,833,231,282,172 (30.0744% of Barba)
  Construction: strategy_seed_local_flip
  Improves record? No

**Method performance this iteration:**
  strategy_seed_local_flip: best=1,178,833,231,282,172 ↑ (was 0)
  Spread: 689,609,612,722,170 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 18)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        90

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_local_flip: 1,178,833,231,282,172 (5 attempts)
  conference_paley: 226,224,085,401,601 (17 attempts)
  circulant_fallback: 87,469,429,096,448 (6 attempts)
  circulant: 77,922,253,668,352 (17 attempts)

---

## Next Plan

**Strategy: BASELINE** — gathering initial data across methods
  Continue diverse exploration

**Next iteration candidate sources:**
  1. Continue current top method with perturbations
  2. Try unexplored methods: negacyclic, skew-symmetric

---

## State Summary

Best determinant found: 1,521,681,143,169,035
  vs. best known:   2,779,447,296,000,000
  Barba bound:      3,919,726,327,358,822 (38.82%)
  Construction:      hadamard_submatrix
  Iterations:        18
  Total tested:      90
