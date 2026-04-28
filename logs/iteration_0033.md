# Hadamard Max-Det Research — Iteration 0033

**Timestamp:** 2026-04-28 11:06:05
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `block5_part0` (strategy_hermod_bruteforce_small)
2. `block5_part1` (strategy_hermod_bruteforce_small)
3. `block5_part2` (strategy_hermod_bruteforce_small)
4. `block5_part3` (strategy_hermod_bruteforce_small)
5. `block5_part4` (strategy_hermod_bruteforce_small)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `block5_part0` | 0 | 0.0000% | strategy_hermod_bruteforce_small |
| 2 | `block5_part1` | 0 | 0.0000% | strategy_hermod_bruteforce_small |
| 3 | `block5_part2` | 0 | 0.0000% | strategy_hermod_bruteforce_small |
| 4 | `block5_part3` | 0 | 0.0000% | strategy_hermod_bruteforce_small |
| 5 | `block5_part4` | 0 | 0.0000% | strategy_hermod_bruteforce_small |

---

## Analysis

**Top determinant:** 0 (0.0000% of Barba)
  Construction: strategy_hermod_bruteforce_small
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_bruteforce_small: best=0 = (was 0)
  Spread: 0 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 33)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        165

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diagonal_paley: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diffset_construction: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_goethals_seidel: 1,521,681,143,169,024 (10 attempts)

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
  Iterations:        33
  Total tested:      165
