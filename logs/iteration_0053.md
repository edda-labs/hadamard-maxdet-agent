# Hadamard Max-Det Research — Iteration 0053

**Timestamp:** 2026-04-28 14:35:27
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `gram_relax_v0` (strategy_auto_gram_relax)
2. `gram_relax_v1` (strategy_auto_gram_relax)
3. `gram_relax_v2` (strategy_auto_gram_relax)
4. `gram_relax_v3` (strategy_auto_gram_relax)
5. `gram_relax_v4` (strategy_auto_gram_relax)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `gram_relax_v0` | 0 | 0.0000% | strategy_auto_gram_relax |
| 2 | `gram_relax_v1` | 0 | 0.0000% | strategy_auto_gram_relax |
| 3 | `gram_relax_v2` | 0 | 0.0000% | strategy_auto_gram_relax |
| 4 | `gram_relax_v3` | 0 | 0.0000% | strategy_auto_gram_relax |
| 5 | `gram_relax_v4` | 0 | 0.0000% | strategy_auto_gram_relax |

---

## Analysis

**Top determinant:** 0 (0.0000% of Barba)
  Construction: strategy_auto_gram_relax
  Improves record? No

**Method performance this iteration:**
  strategy_auto_gram_relax: best=0 = (was 0)
  Spread: 0 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 53)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        265

**Method Rankings (by best determinant):**
  strategy_hermod_simulated_annealing: 1,616,863,222,038,528 (10 attempts)
  strategy_hermod_coordinate_exchange: 1,521,681,143,169,046 (10 attempts)
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_auto_hadamard_product: 1,521,681,143,169,035 (10 attempts)
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
  Iterations:        53
  Total tested:      265
