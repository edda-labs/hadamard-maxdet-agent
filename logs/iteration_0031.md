# Hadamard Max-Det Research — Iteration 0031

**Timestamp:** 2026-04-28 10:45:01
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `bordered_neg_v0` (strategy_hermod_paley_bordered)
2. `bordered_neg_v1` (strategy_hermod_paley_bordered)
3. `bordered_neg_v2` (strategy_hermod_paley_bordered)
4. `bordered_neg_v3` (strategy_hermod_paley_bordered)
5. `bordered_neg_v4` (strategy_hermod_paley_bordered)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `bordered_neg_v0` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_paley_bordered |
| 2 | `bordered_neg_v2` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_paley_bordered |
| 3 | `bordered_neg_v3` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_paley_bordered |
| 4 | `bordered_neg_v1` | 1,521,681,143,169,013 | 38.8211% | strategy_hermod_paley_bordered |
| 5 | `bordered_neg_v4` | 1,521,681,143,169,013 | 38.8211% | strategy_hermod_paley_bordered |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: strategy_hermod_paley_bordered
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_paley_bordered: best=1,521,681,143,169,024 = (was 1,521,681,143,169,024)
  Spread: 11 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 31)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        155

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
  Iterations:        31
  Total tested:      155
