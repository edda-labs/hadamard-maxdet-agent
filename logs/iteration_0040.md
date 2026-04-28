# Hadamard Max-Det Research — Iteration 0040

**Timestamp:** 2026-04-28 12:20:37
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `gram_cluster_del0` (strategy_auto_gram_target)
2. `gram_cluster_del6` (strategy_auto_gram_target)
3. `gram_cluster_del12` (strategy_auto_gram_target)
4. `gram_cluster_del18` (strategy_auto_gram_target)
5. `gram_cluster_del23` (strategy_auto_gram_target)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `gram_cluster_del6` | 1,521,681,143,169,024 | 38.8211% | strategy_auto_gram_target |
| 2 | `gram_cluster_del12` | 1,521,681,143,169,024 | 38.8211% | strategy_auto_gram_target |
| 3 | `gram_cluster_del18` | 1,521,681,143,169,024 | 38.8211% | strategy_auto_gram_target |
| 4 | `gram_cluster_del23` | 1,521,681,143,169,024 | 38.8211% | strategy_auto_gram_target |
| 5 | `gram_cluster_del0` | 1,521,681,143,169,013 | 38.8211% | strategy_auto_gram_target |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: strategy_auto_gram_target
  Improves record? No

**Method performance this iteration:**
  strategy_auto_gram_target: best=1,521,681,143,169,024 ↑ (was 0)
  Spread: 11 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 40)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        200

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
  Iterations:        40
  Total tested:      200
