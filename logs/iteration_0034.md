# Hadamard Max-Det Research — Iteration 0034

**Timestamp:** 2026-04-28 11:16:50
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `equiv_perturb_v0` (strategy_hermod_equivalence_orbit)
2. `equiv_perturb_v1` (strategy_hermod_equivalence_orbit)
3. `equiv_perturb_v2` (strategy_hermod_equivalence_orbit)
4. `equiv_perturb_v3` (strategy_hermod_equivalence_orbit)
5. `equiv_perturb_v4` (strategy_hermod_equivalence_orbit)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `equiv_perturb_v1` | 731,737,202,098,179 | 18.6681% | strategy_hermod_equivalence_orbit |
| 2 | `equiv_perturb_v2` | 485,831,668,137,988 | 12.3945% | strategy_hermod_equivalence_orbit |
| 3 | `equiv_perturb_v4` | 451,227,250,851,841 | 11.5117% | strategy_hermod_equivalence_orbit |
| 4 | `equiv_perturb_v0` | 245,753,331,056,639 | 6.2697% | strategy_hermod_equivalence_orbit |
| 5 | `equiv_perturb_v3` | 137,917,573,890,048 | 3.5186% | strategy_hermod_equivalence_orbit |

---

## Analysis

**Top determinant:** 731,737,202,098,179 (18.6681% of Barba)
  Construction: strategy_hermod_equivalence_orbit
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_equivalence_orbit: best=731,737,202,098,179 ↑ (was 0)
  Spread: 593,819,628,208,131 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 34)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        170

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
  Iterations:        34
  Total tested:      170
