# Hadamard Max-Det Research — Iteration 0048

**Timestamp:** 2026-04-28 13:45:41
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `hadprod_paley` (strategy_auto_hadamard_product)
2. `hadprod_circ` (strategy_auto_hadamard_product)
3. `hadprod_hadam` (strategy_auto_hadamard_product)
4. `hadprod_sym` (strategy_auto_hadamard_product)
5. `hadprod_check` (strategy_auto_hadamard_product)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `hadprod_check` | 1,521,681,143,169,035 | 38.8211% | strategy_auto_hadamard_product |
| 2 | `hadprod_circ` | 238,668,480,512 | 0.0061% | strategy_auto_hadamard_product |
| 3 | `hadprod_sym` | 90,529,857,536 | 0.0023% | strategy_auto_hadamard_product |
| 4 | `hadprod_paley` | 0 | 0.0000% | strategy_auto_hadamard_product |
| 5 | `hadprod_hadam` | 0 | 0.0000% | strategy_auto_hadamard_product |

---

## Analysis

**Top determinant:** 1,521,681,143,169,035 (38.8211% of Barba)
  Construction: strategy_auto_hadamard_product
  Improves record? No

**Method performance this iteration:**
  strategy_auto_hadamard_product: best=1,521,681,143,169,035 ↑ (was 0)
  Spread: 1,521,681,143,169,035 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 48)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        240

**Method Rankings (by best determinant):**
  strategy_hermod_simulated_annealing: 1,616,863,222,038,528 (10 attempts)
  strategy_hermod_coordinate_exchange: 1,521,681,143,169,046 (10 attempts)
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_auto_hadamard_product: 1,521,681,143,169,035 (5 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)

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
  Iterations:        48
  Total tested:      240
