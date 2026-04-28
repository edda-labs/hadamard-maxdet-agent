# Hadamard Max-Det Research — Iteration 0051

**Timestamp:** 2026-04-28 14:17:27
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `block_11_12_s0` (strategy_seed_kronecker_product)
2. `block_11_12_s1` (strategy_seed_kronecker_product)
3. `block_11_12_s2` (strategy_seed_kronecker_product)
4. `block_11_12_s3` (strategy_seed_kronecker_product)
5. `block_11_12_s4` (strategy_seed_kronecker_product)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `block_11_12_s2` | 23,731,372,032 | 0.0006% | strategy_seed_kronecker_product |
| 2 | `block_11_12_s4` | 22,422,749,184 | 0.0006% | strategy_seed_kronecker_product |
| 3 | `block_11_12_s3` | 19,604,176,896 | 0.0005% | strategy_seed_kronecker_product |
| 4 | `block_11_12_s1` | 6,849,298,432 | 0.0002% | strategy_seed_kronecker_product |
| 5 | `block_11_12_s0` | 3,460,300,800 | 0.0001% | strategy_seed_kronecker_product |

---

## Analysis

**Top determinant:** 23,731,372,032 (0.0006% of Barba)
  Construction: strategy_seed_kronecker_product
  Improves record? No

**Method performance this iteration:**
  strategy_seed_kronecker_product: best=23,731,372,032 = (was 23,731,372,032)
  Spread: 20,271,071,232 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 51)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        255

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
  Iterations:        51
  Total tested:      255
