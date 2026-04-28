# Hadamard Max-Det Research — Iteration 0052

**Timestamp:** 2026-04-28 14:20:59
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `sym_toeplitz_0` (strategy_seed_symmetric_toeplitz)
2. `sym_toeplitz_1` (strategy_seed_symmetric_toeplitz)
3. `sym_toeplitz_2` (strategy_seed_symmetric_toeplitz)
4. `sym_toeplitz_3` (strategy_seed_symmetric_toeplitz)
5. `sym_toeplitz_4` (strategy_seed_symmetric_toeplitz)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `sym_toeplitz_0` | 326,891,470,848 | 0.0083% | strategy_seed_symmetric_toeplitz |
| 2 | `sym_toeplitz_1` | 12,947,816,448 | 0.0003% | strategy_seed_symmetric_toeplitz |
| 3 | `sym_toeplitz_3` | 574,619,648 | 0.0000% | strategy_seed_symmetric_toeplitz |
| 4 | `sym_toeplitz_2` | 322,961,408 | 0.0000% | strategy_seed_symmetric_toeplitz |
| 5 | `sym_toeplitz_4` | 20,971,520 | 0.0000% | strategy_seed_symmetric_toeplitz |

---

## Analysis

**Top determinant:** 326,891,470,848 (0.0083% of Barba)
  Construction: strategy_seed_symmetric_toeplitz
  Improves record? No

**Method performance this iteration:**
  strategy_seed_symmetric_toeplitz: best=326,891,470,848 ↑ (was 0)
  Spread: 326,870,499,328 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 52)**
  Best determinant:    1,616,863,222,038,528
  vs. best known:      2,779,447,296,000,000 (58.17%)
  vs. Barba bound:     3,919,726,327,358,822 (41.2494%)
  Total tested:        260

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
  Iterations:        52
  Total tested:      260
