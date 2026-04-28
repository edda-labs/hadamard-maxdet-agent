# Hadamard Max-Det Research — Iteration 0042

**Timestamp:** 2026-04-28 12:42:19
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `coord_exchange_0` (strategy_hermod_coordinate_exchange)
2. `coord_exchange_1` (strategy_hermod_coordinate_exchange)
3. `coord_exchange_2` (strategy_hermod_coordinate_exchange)
4. `coord_exchange_3` (strategy_hermod_coordinate_exchange)
5. `coord_exchange_4` (strategy_hermod_coordinate_exchange)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `coord_exchange_0` | 1,521,681,143,169,046 | 38.8211% | strategy_hermod_coordinate_exchange |
| 2 | `coord_exchange_1` | 1,521,681,143,169,035 | 38.8211% | strategy_hermod_coordinate_exchange |
| 3 | `coord_exchange_2` | 1,521,681,143,169,035 | 38.8211% | strategy_hermod_coordinate_exchange |
| 4 | `coord_exchange_3` | 1,521,681,143,169,035 | 38.8211% | strategy_hermod_coordinate_exchange |
| 5 | `coord_exchange_4` | 1,521,681,143,169,035 | 38.8211% | strategy_hermod_coordinate_exchange |

---

## Analysis

**Top determinant:** 1,521,681,143,169,046 (38.8211% of Barba)
  Construction: strategy_hermod_coordinate_exchange
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_coordinate_exchange: best=1,521,681,143,169,046 ↑ (was 0)
  Spread: 11 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 42)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        210

**Method Rankings (by best determinant):**
  strategy_hermod_simulated_annealing: 1,616,863,222,038,528 (10 attempts)
  strategy_hermod_coordinate_exchange: 1,521,681,143,169,046 (5 attempts)
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diagonal_paley: 1,521,681,143,169,024 (10 attempts)

---

## Next Plan

**Strategy: BASELINE** — gathering initial data across methods
  Continue diverse exploration

**Next iteration candidate sources:**
  1. Continue current top method with perturbations
  2. Try unexplored methods: negacyclic, skew-symmetric

---

## State Summary

Best determinant found: 1,616,863,222,038,528
  vs. best known:   2,779,447,296,000,000
  Barba bound:      3,919,726,327,358,822 (41.25%)
  Construction:      strategy_hermod_simulated_annealing
  Iterations:        42
  Total tested:      210
