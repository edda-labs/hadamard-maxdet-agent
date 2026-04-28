# Hadamard Max-Det Research — Iteration 0024

**Timestamp:** 2026-04-28 09:12:06
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** 2,779,447,296,000,000
**Barba Bound:** 3,919,726,327,358,822

---

## Generated Candidates

1. `paley_pos_diag` (strategy_hermod_diagonal_paley)
2. `paley_neg_diag` (strategy_hermod_diagonal_paley)
3. `paley_qr_diag` (strategy_hermod_diagonal_paley)
4. `paley_alt4_diag` (strategy_hermod_diagonal_paley)
5. `paley_split_diag` (strategy_hermod_diagonal_paley)

---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
| 1 | `paley_pos_diag` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_diagonal_paley |
| 2 | `paley_neg_diag` | 1,521,681,143,169,024 | 38.8211% | strategy_hermod_diagonal_paley |
| 3 | `paley_alt4_diag` | 44,435,266,076,672 | 1.1336% | strategy_hermod_diagonal_paley |
| 4 | `paley_split_diag` | 44,435,266,076,672 | 1.1336% | strategy_hermod_diagonal_paley |
| 5 | `paley_qr_diag` | 0 | 0.0000% | strategy_hermod_diagonal_paley |

---

## Analysis

**Top determinant:** 1,521,681,143,169,024 (38.8211% of Barba)
  Construction: strategy_hermod_diagonal_paley
  Improves record? No

**Method performance this iteration:**
  strategy_hermod_diagonal_paley: best=1,521,681,143,169,024 ↑ (was 0)
  Spread: 1,521,681,143,169,024 (max-min)

---

## Self-Assessment

**Overall Progress (Iteration 24)**
  Best determinant:    1,521,681,143,169,035
  vs. best known:      2,779,447,296,000,000 (54.75%)
  vs. Barba bound:     3,919,726,327,358,822 (38.8211%)
  Total tested:        120

**Method Rankings (by best determinant):**
  hadamard_submatrix: 1,521,681,143,169,035 (17 attempts)
  strategy_seed_conference_border: 1,521,681,143,169,024 (10 attempts)
  strategy_hermod_diagonal_paley: 1,521,681,143,169,024 (5 attempts)
  strategy_seed_local_flip: 1,178,833,231,282,172 (10 attempts)
  conference_paley: 226,224,085,401,601 (17 attempts)

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
  Iterations:        24
  Total tested:      120
