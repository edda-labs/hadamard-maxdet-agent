# Hadamard Max-Det Research — Iteration 0027

**Timestamp:** 2026-04-28 10:02:51
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `diffset_shift0` (strategy_hermod_diffset_construction)
2. `diffset_shift1` (strategy_hermod_diffset_construction)
3. `diffset_shift2` (strategy_hermod_diffset_construction)
4. `diffset_shift3` (strategy_hermod_diffset_construction)
5. `diffset_shift4` (strategy_hermod_diffset_construction)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `diffset_shift0` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_diffset_construction |
| 2 | `diffset_shift1` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_diffset_construction |
| 3 | `diffset_shift3` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_diffset_construction |
| 4 | `diffset_shift2` | 214,189,721,255,937 | 5.4644% | strategy_hermod_diffset_construction |
| 5 | `diffset_shift4` | 214,189,721,255,937 | 5.4644% | strategy_hermod_diffset_construction |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: strategy_hermod_diffset_construction
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_diffset_construction: best=1,521,681,143,169,024 = (was 1,521,681,143,169,024)
  Spread: 1,307,491,421,913,087 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 27)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        135

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diagonal_paley: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diffset_construction: 1,521,681,143,169,024 (10 attempts)
  strategy_seed_local_flip: 1,178,833,231,282,172 (10 attempts)

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
  Iterations:        27
  Total tested:      135
