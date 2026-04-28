# Hadamard Max-Det Research — Iteration 0020

**Timestamp:** 2026-04-28 08:10:25
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `paley_diag_0` (strategy_seed_conference_border)
2. `paley_diag_1` (strategy_seed_conference_border)
3. `paley_diag_2` (strategy_seed_conference_border)
4. `paley_diag_3` (strategy_seed_conference_border)
5. `paley_diag_4` (strategy_seed_conference_border)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `paley_diag_0` | 1,521,681,143,169,024 | 38.8211% | strategy_seed_conference_border |
| 2 | `paley_diag_1` | 1,521,681,143,169,024 | 38.8211% | strategy_seed_conference_border |
| 3 | `paley_diag_4` | 1,521,681,143,169,024 | 38.8211% | strategy_seed_conference_border |
| 4 | `paley_diag_3` | 282,604,553,109,504 | 7.2098% | strategy_seed_conference_border |
| 5 | `paley_diag_2` | 44,435,266,076,672 | 1.1336% | strategy_seed_conference_border |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: strategy_seed_conference_border
  Improves record? No

**Method performance this iteration:**
  strategy_seed_conference_border: best=1,521,681,143,169,024 ↑ (was 0)
  Spread: 1,477,245,877,092,352 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 20)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        100

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (5 attempts)
  strategy_seed_local_flip: 1,178,833,231,282,172 (10 attempts)
  conference_paley: 226,224,085,401,601 (17 attempts)
  circulant_fallback: 87,469,429,096,448 (6 attempts)

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
  Iterations:        20
  Total tested:      100
