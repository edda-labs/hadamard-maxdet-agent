# Hadamard Max-Det Research — Iteration 0037

**Timestamp:** 2026-04-28 11:48:50
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `sa_best_v0` (strategy_hermod_simulated_annealing)
2. `sa_best_v1` (strategy_hermod_simulated_annealing)
3. `sa_best_v2` (strategy_hermod_simulated_annealing)
4. `sa_best_v3` (strategy_hermod_simulated_annealing)
5. `sa_best_v4` (strategy_hermod_simulated_annealing)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `sa_best_v4` | 1,616,863,222,038,528 | 41.2494% | strategy_hermod_simulated_annealing |
| 2 | `sa_best_v2` | 1,615,675,495,809,035 | 41.2191% | strategy_hermod_simulated_annealing |
| 3 | `sa_best_v1` | 1,584,203,921,620,988 | 40.4162% | strategy_hermod_simulated_annealing |
| 4 | `sa_best_v3` | 1,574,876,057,960,444 | 40.1782% | strategy_hermod_simulated_annealing |
| 5 | `sa_best_v0` | 1,525,334,012,854,275 | 38.9143% | strategy_hermod_simulated_annealing |

---

## Analysis

**Top determinant:** 1,616,863,222,038,528 (41.2494% of Barba)
  Construction: strategy_hermod_simulated_annealing
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_simulated_annealing: best=1,616,863,222,038,528 = (was 1,616,863,222,038,528)
  Spread: 91,529,209,184,253 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 37)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        185

**Method Rankings (by best determinant):**
  strategy_hermod_simulated_annealing: 1,616,863,222,038,528 (10 attempts)
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diagonal_paley: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diffset_construction: 1,521,681,143,169,024 (10 attempts)

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
  Iterations:        37
  Total tested:      185
