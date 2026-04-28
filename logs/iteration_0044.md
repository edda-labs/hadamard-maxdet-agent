# Hadamard Max-Det Research — Iteration 0044

**Timestamp:** 2026-04-28 13:03:28
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `genetic_had_bestxpaley_all1_s6` (strategy_auto_genetic_crossover)
2. `genetic_negaxpaley_all1_s7` (strategy_auto_genetic_crossover)
3. `genetic_negaxpaley_alt_s6` (strategy_auto_genetic_crossover)
4. `genetic_paley_all1xhad_best_s12` (strategy_auto_genetic_crossover)
5. `genetic_paley_all1xhad_best_s8` (strategy_auto_genetic_crossover)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `genetic_paley_all1xhad_best_s12` | 132,090,377,011,200 | 3.3699% | strategy_auto_genetic_crossover |
| 2 | `genetic_had_bestxpaley_all1_s6` | 80,232,673,443,840 | 2.0469% | strategy_auto_genetic_crossover |
| 3 | `genetic_paley_all1xhad_best_s8` | 27,690,056,810,496 | 0.7064% | strategy_auto_genetic_crossover |
| 4 | `genetic_negaxpaley_all1_s7` | 86,973,087,744 | 0.0022% | strategy_auto_genetic_crossover |
| 5 | `genetic_negaxpaley_alt_s6` | 22,196,256,768 | 0.0006% | strategy_auto_genetic_crossover |

---

## Analysis

**Top determinant:** 132,090,377,011,200 (3.3699% of Barba)
  Construction: strategy_auto_genetic_crossover
  Improves record? No

**Method performance this iteration:**
  strategy_auto_genetic_crossover: best=132,090,377,011,200 ↑ (was 0)
  Spread: 132,068,180,754,432 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 44)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        220

**Method Rankings (by best determinant):**
  strategy_hermod_simulated_annealing: 1,616,863,222,038,528 (10 attempts)
  strategy_hermod_coordinate_exchange: 1,521,681,143,169,046 (10 attempts)
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
  Iterations:        44
  Total tested:      220
