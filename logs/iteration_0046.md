# Hadamard Max-Det Research — Iteration 0046

**Timestamp:** 2026-04-28 13:24:36
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `paley_perm_k1_altdiag` (strategy_auto_paley_permutations)
2. `paley_perm_k2_altdiag` (strategy_auto_paley_permutations)
3. `paley_perm_k3_altdiag` (strategy_auto_paley_permutations)
4. `paley_perm_k4_altdiag` (strategy_auto_paley_permutations)
5. `paley_perm_k6_altdiag` (strategy_auto_paley_permutations)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `paley_perm_k1_altdiag` | 44,435,266,076,672 | 1.1336% | strategy_auto_paley_permutations |
| 2 | `paley_perm_k2_altdiag` | 44,435,266,076,672 | 1.1336% | strategy_auto_paley_permutations |
| 3 | `paley_perm_k3_altdiag` | 44,435,266,076,672 | 1.1336% | strategy_auto_paley_permutations |
| 4 | `paley_perm_k4_altdiag` | 44,435,266,076,672 | 1.1336% | strategy_auto_paley_permutations |
| 5 | `paley_perm_k6_altdiag` | 44,435,266,076,672 | 1.1336% | strategy_auto_paley_permutations |

---

## Analysis

**Top determinant:** 44,435,266,076,672 (1.1336% of Barba)
  Construction: strategy_auto_paley_permutations
  Improves record? No

**Method performance this iteration:**
  strategy_auto_paley_permutations: best=44,435,266,076,672 ↑ (was 0)
  Spread: 0 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 46)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        230

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
  Iterations:        46
  Total tested:      230
