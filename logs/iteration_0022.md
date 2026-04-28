# Hadamard Max-Det Research — Iteration 0022

**Timestamp:** 2026-04-28 08:57:30
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `negacyclic_v0` (strategy_seed_negacyclic_family)
2. `negacyclic_v1` (strategy_seed_negacyclic_family)
3. `negacyclic_v2` (strategy_seed_negacyclic_family)
4. `negacyclic_v3` (strategy_seed_negacyclic_family)
5. `negacyclic_v4` (strategy_seed_negacyclic_family)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `negacyclic_v3` | 16,019,661,783,040 | 0.4087% | strategy_seed_negacyclic_family |
| 2 | `negacyclic_v4` | 37,748,736 | 0.0000% | strategy_seed_negacyclic_family |
| 3 | `negacyclic_v1` | 4,194,304 | 0.0000% | strategy_seed_negacyclic_family |
| 4 | `negacyclic_v2` | 4,194,304 | 0.0000% | strategy_seed_negacyclic_family |
| 5 | `negacyclic_v0` | 0 | 0.0000% | strategy_seed_negacyclic_family |

---

## Analysis

**Top determinant:** 16,019,661,783,040 (0.4087% of Barba)
  Construction: strategy_seed_negacyclic_family
  Improves record? No

**Method performance this iteration:**
  strategy_seed_negacyclic_family: best=16,019,661,783,040 ↑ (was 0)
  Spread: 16,019,661,783,040 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 22)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        110

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_seed_local_flip: 1,178,833,231,282,172 (10 attempts)
  conference_paley: 226,224,085,401,601 (17 attempts)
  circulant_fallback: 87,469,429,096,448 (6 attempts)

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
  Iterations:        22
  Total tested:      110
