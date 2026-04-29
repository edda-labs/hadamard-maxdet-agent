"""
agent.py — Hadamard Max-Det Research Agent

Autonomous research loop for finding maximal-determinant 23×23 {±1} matrices.
Target: Order 23 is the smallest open case in the Hadamard Maximal Determinant Problem.

Loop (per iteration):
  1. GENERATE — LLM proposes 5 candidate constructions with rationale
  2. TEST — Compute determinants, rank results
  3. ANALYZE — Identify patterns in top matrices, failure modes
  4. SELF-ASSESS — Evaluate progress toward Barba bound, compare to prior iterations
  5. NEXT PLAN — Propose search strategy for next iteration
  6. REPORT — Write iteration_NNNN.md + update LATEST.md

Usage: python3 agent.py --iterations 1
"""

import numpy as np
import json
import time
import sys
import os
from datetime import datetime
from pathlib import Path

from matrix_tester import (
    N, BEST_KNOWN_G, BARBA_BOUND, HADAMARD_BOUND,
    verify_matrix, verify_batch, load_state, save_state, update_state,
    summarize_progress, TestResult
)
from constructions import (
    generate_candidates, CONSTRUCTION_METHODS,
    hadamard_24, from_hadamard_all_deletions,
    random_circulant, random_toeplitz, random_flip
)
from strategy_queue import load_strategies, get_next_strategy, record_attempt, record_error, init_seed_strategies

PROJECT_DIR = Path(__file__).parent

# ============================================================================
# 1. GENERATE — LLM-driven candidate generation
# ============================================================================

def generate_candidates_phase(state: dict, iteration: int) -> tuple[list[tuple[np.ndarray, str, str]], str | None]:
    """
    Generate 5 candidate matrices.
    Priority: Strategy queue → programmatic exploration.

    Returns (candidates, active_strategy_id). The strategy_id is None for the
    programmatic fallback path; otherwise it's the id of the strategy whose
    code produced the candidates. The caller is responsible for calling
    record_attempt exactly once per invocation after testing — recording
    per-matrix here would inflate `attempts` 5x and bump `stale_rounds` past
    the auto-kill threshold after a single successful run.
    """

    # ---- STRATEGY QUEUE ----
    strategy = get_next_strategy(state.get("best_determinant") or 0)
    if strategy:
        print(f"  [STRATEGY] Executing: {strategy['rationale']} (attempt {strategy['attempts']+1})")
        try:
            namespace = {"np": np, "__builtins__": __builtins__,
                         "PROJECT_DIR": str(PROJECT_DIR),
                         "__file__": str(PROJECT_DIR / "strategy_exec.py")}
            sys.path.insert(0, str(PROJECT_DIR))
            from constructions import paley_core, hadamard_24
            namespace["paley_core"] = paley_core
            namespace["hadamard_24"] = hadamard_24

            exec(strategy["code"], namespace)

            if "generate_matrices" in namespace:
                matrices = namespace["generate_matrices"]()
                candidates = []
                for matrix, name in matrices[:5]:
                    method = f"strategy_{strategy['id']}"
                    candidates.append((matrix, name, method))
                return candidates, strategy["id"]
        except Exception as e:
            print(f"  [STRATEGY ERROR] {e}")
            import traceback
            traceback.print_exc()
            record_error(strategy["id"], str(e))

    # ---- PROGRAMMATIC FALLBACK ----
    return _programmatic_generate(state, iteration, count=5), None


def _programmatic_generate(state: dict, iteration: int, count: int = 5) -> list[tuple[np.ndarray, str, str]]:
    """Programmatic candidate generation as fallback."""
    construction_stats = state.get("construction_stats", {})
    scores = {}
    for method in CONSTRUCTION_METHODS:
        if method in construction_stats:
            best = construction_stats[method].get("best_det", 0)
            cnt = construction_stats[method].get("count", 0)
            # Score: best_det * (1 + 1/sqrt(count)) to balance exploitation/exploration
            scores[method] = best * (1 + 1.0 / max(1, np.sqrt(cnt)))
        else:
            scores[method] = 0  # Unexplored methods get a shot

    # Rank methods, prioritize top scorers but include some exploration
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    candidates = []
    methods_used = []

    # Use top 3 methods + 2 random unexplored/low-scoring methods
    for method, _ in ranked[:3]:
        if method not in methods_used:
            methods_used.append(method)

    # Add 2 exploration methods from the bottom half
    bottom_half = [m for m, _ in ranked[len(ranked)//2:] if m not in methods_used]
    import random as rand
    methods_used.extend(rand.sample(bottom_half, min(2, len(bottom_half))))

    # Ensure we have exactly 5 methods
    while len(methods_used) < 5:
        unused = [m for m in CONSTRUCTION_METHODS if m not in methods_used]
        if unused:
            methods_used.append(rand.choice(unused))
        else:
            break
    methods_used = methods_used[:5]

    # Generate one candidate per method
    for method in methods_used:
        try:
            gen_results = generate_candidates(method, count=1,
                                             seed=hash(f"iter{iteration}_{method}") % 2**31)
            for matrix, name in gen_results:
                candidates.append((matrix, name, method))
        except Exception as e:
            print(f"  [GEN ERROR] {method}: {e}")

    # Pad if needed
    while len(candidates) < 5:
        matrix, name = random_circulant(seed=hash(f"pad_{len(candidates)}") % 2**31), f"pad_{len(candidates)}"
        candidates.append((matrix, name, "circulant_fallback"))

    return candidates


# ============================================================================
# 2. TEST — Compute determinants
# ============================================================================

def test_phase(candidates: list[tuple[np.ndarray, str, str]]) -> list[TestResult]:
    """Test each candidate and return ranked results."""
    prepared = [(m, n, c) for m, n, c in candidates]
    results = verify_batch(prepared)
    results.sort(key=lambda r: r.det_abs, reverse=True)
    return results


# ============================================================================
# 3. ANALYZE — Pattern analysis
# ============================================================================

def analyze_phase(results: list[TestResult], state: dict,
                  construction_stats: dict) -> str:
    """Analyze results and generate insights."""
    if not results:
        return "No results to analyze."

    best = results[0]
    worst = results[-1]

    lines = []
    lines.append(f"**Top determinant:** {best.det_abs:,} ({best.pct_of_barba:.4f}% of Barba)")
    lines.append(f"  Construction: {best.construction_method}")
    lines.append(f"  Improves record? {'YES 🏆' if best.improves_record else 'No'}")

    # Per-method performance
    lines.append("")
    lines.append("**Method performance this iteration:**")
    method_results = {}
    for r in results:
        m = r.construction_method
        if m not in method_results:
            method_results[m] = []
        method_results[m].append(r.det_abs)

    for method, dets in sorted(method_results.items(),
                                key=lambda x: max(x[1]), reverse=True):
        best_det = max(dets)
        # Compare to historical best for this method
        hist_best = state.get("construction_stats", {}).get(method, {}).get("best_det", 0)
        improved = "↑" if best_det > hist_best else "=" if best_det == hist_best else "↓"
        lines.append(f"  {method}: best={best_det:,} {improved} (was {hist_best:,})")

    # Spread analysis
    dets_values = [r.det_abs for r in results]
    if len(dets_values) >= 3:
        spread = max(dets_values) - min(dets_values)
        lines.append(f"  Spread: {spread:,} (max-min)")

    # Compare against previous baseline
    prev_best = state.get("best_determinant", 0)
    if prev_best and best.det_abs > prev_best:
        improvement = ((best.det_abs - prev_best) / prev_best) * 100
        lines.append(f"  Improvement over session best: +{improvement:.4f}%")

    return "\n".join(lines)


# ============================================================================
# 4. SELF-ASSESS — Progress evaluation
# ============================================================================

def self_assess_phase(state: dict, iteration: int) -> str:
    """Evaluate whether the search is making meaningful progress."""
    lines = []

    # Progress toward Barba bound
    best_det = state.get("best_determinant") or 0
    pct_barba = (best_det / BARBA_BOUND) * 100 if best_det else 0
    pct_known = (best_det / BEST_KNOWN_G) * 100 if best_det else 0

    lines.append(f"**Overall Progress (Iteration {iteration})**")
    lines.append(f"  Best determinant:    {best_det:,}")
    lines.append(f"  vs. best known:      {BEST_KNOWN_G:,} ({pct_known:.2f}%)")
    lines.append(f"  vs. Barba bound:     {BARBA_BOUND:,} ({pct_barba:.4f}%)")
    lines.append(f"  Total tested:        {state.get('total_matrices_tested', 0):,}")

    # Convergence assessment
    history = state.get("history", [])
    if len(history) >= 2:
        prev_best = history[-2].get("best_det", 0)
        if best_det > prev_best:
            improvement = ((best_det - prev_best) / prev_best) * 100
            lines.append(f"  Converging?          ↑ +{improvement:.4f}% since last iteration")
        elif best_det == prev_best:
            lines.append(f"  Converging?          → stagnant (maybe stuck in local optimum)")
        else:
            lines.append(f"  Converging?          ↓ Regression (unusual, check state integrity)")

    # Ranking of construction methods
    stats = state.get("construction_stats", {})
    if stats:
        lines.append("")
        lines.append("**Method Rankings (by best determinant):**")
        ranked_methods = sorted(stats.items(),
                               key=lambda x: x[1].get("best_det", 0),
                               reverse=True)
        for method, mstats in ranked_methods[:5]:
            lines.append(f"  {method}: {mstats['best_det']:,} ({mstats['count']} attempts)")

    return "\n".join(lines)


# ============================================================================
# 5. NEXT PLAN — Strategy for next iteration
# ============================================================================

def next_plan_phase(state: dict, results: list[TestResult]) -> str:
    """Plan the next iteration's search strategy."""
    lines = []

    best_method = results[0].construction_method if results else "unknown"
    best_det = results[0].det_abs if results else 0

    # Determine if we should exploit or explore
    history = state.get("history", [])
    if len(history) >= 3:
        recent_bests = [h.get("best_det", 0) for h in history[-3:]]
        if len(set(recent_bests)) == 1 and recent_bests[0] > 0:
            lines.append("**Strategy: EXPLORE** — stalled for 3+ iterations, shift to new methods")
            lines.append(f"  Try: perturbations of top matrix, new block structures, negacyclic variants")
        else:
            lines.append(f"**Strategy: EXPLOIT** — making progress with {best_method}")
            lines.append(f"  Focus: generate more {best_method}-family candidates, small perturbations")
    else:
        lines.append("**Strategy: BASELINE** — gathering initial data across methods")
        lines.append("  Continue diverse exploration")

    # Specific next steps
    lines.append("")
    lines.append("**Next iteration candidate sources:**")
    if best_method == "hadamard_submatrix":
        lines.append("  1. More row/col deletion pairs from H24 (576 total, only N tested so far)")
        lines.append("  2. Try negating rows/cols of best deletion candidate")
    elif best_method in ["circulant", "toeplitz"]:
        lines.append(f"  1. Perturb best {best_method} with 1-3 sign flips")
        lines.append(f"  2. Try related {best_method} variants")
    else:
        lines.append("  1. Continue current top method with perturbations")
        lines.append("  2. Try unexplored methods: negacyclic, skew-symmetric")

    return "\n".join(lines)


# ============================================================================
# 6. REPORT — Write iteration log
# ============================================================================

def report_phase(iteration: int, candidates: list, results: list[TestResult],
                 analysis: str, assessment: str, plan: str, state: dict) -> str:
    """Write iteration report to logs/ and update LATEST.md."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build iteration report
    report = f"""# Hadamard Max-Det Research — Iteration {iteration:04d}

**Timestamp:** {timestamp}
**Target:** Order 23 ±1 matrix, max determinant
**Best Known:** {BEST_KNOWN_G:,}
**Barba Bound:** {BARBA_BOUND:,}

---

## Generated Candidates

"""
    for i, (matrix, name, method) in enumerate(candidates):
        report += f"{i+1}. `{name}` ({method})\n"

    report += f"""
---

## Test Results

| # | Name | |det| | % Barba | Method |
|---|------|--------|---------|--------|
"""
    for r in results:
        report += f"| {results.index(r)+1} | `{r.name}` | {r.det_abs:,} | {r.pct_of_barba:.4f}% | {r.construction_method} |\n"

    report += f"""
---

## Analysis

{analysis}

---

## Self-Assessment

{assessment}

---

## Next Plan

{plan}

---

## State Summary

{summarize_progress(state)}
"""

    # Write iteration log
    log_path = PROJECT_DIR / "logs" / f"iteration_{iteration:04d}.md"
    with open(log_path, "w") as f:
        f.write(report)

    # Update LATEST.md
    latest_path = PROJECT_DIR / "logs" / "LATEST.md"
    with open(latest_path, "w") as f:
        f.write(report)

    return str(log_path)


# ============================================================================
# MAIN LOOP
# ============================================================================

def run_iteration(iteration: int, state_path: str = "state.json") -> dict:
    """Execute one full iteration of the research loop."""
    print(f"\n{'='*60}")
    print(f"  ITERATION {iteration:04d}")
    print(f"{'='*60}")

    state = load_state(state_path)

    # Phase 1: Generate
    print("\n[1/6] GENERATE — creating 5 candidate matrices...")
    t0 = time.time()
    candidates, active_strategy_id = generate_candidates_phase(state, iteration)
    print(f"  Generated {len(candidates)} candidates in {time.time()-t0:.1f}s")
    for _, name, method in candidates:
        print(f"    • {name} ({method})")

    # Phase 2: Test
    print("\n[2/6] TEST — computing determinants...")
    t0 = time.time()
    results = test_phase(candidates)
    print(f"  Tested {len(results)} matrices in {time.time()-t0:.1f}s")
    for r in results:
        flag = " 🏆" if r.improves_record else ""
        print(f"    • {r.name}: |det|={r.det_abs:,} ({r.pct_of_barba:.4f}% Barba){flag}")

    # Aggregate strategy outcome: one record_attempt per invocation, using the
    # max integer-det across the 5 candidates. Per-matrix recording (the old
    # behavior) bumped `attempts` to 5 and `stale_rounds` to 4 after a single
    # successful run, killing strategies after 2 invocations.
    if active_strategy_id is not None:
        tag = f"strategy_{active_strategy_id}"
        sresults = [r for r in results if r.construction_method == tag]
        if sresults:
            best_r = max(sresults, key=lambda r: r.det_abs)
            record_attempt(active_strategy_id, best_r.det_abs, best_r.name)
        else:
            record_attempt(active_strategy_id, 0, "no_valid_matrices")

    # Phase 3: Analyze
    print("\n[3/6] ANALYZE — finding patterns...")
    analysis = analyze_phase(results, state, state.get("construction_stats", {}))

    # Update state BEFORE self-assess so it has fresh data
    state = update_state(state, results, iteration, state_path)
    print(analysis)

    # Phase 4: Self-Assess
    print("\n[4/6] SELF-ASSESS — evaluating progress...")
    assessment = self_assess_phase(state, iteration)
    print(assessment)

    # Phase 5: Next Plan
    print("\n[5/6] NEXT PLAN — strategy for iteration {}...".format(iteration + 1))
    plan = next_plan_phase(state, results)
    print(plan)

    # Phase 6: Report
    print("\n[6/6] REPORT — writing logs...")
    report_path = report_phase(iteration, candidates, results, analysis, assessment, plan, state)
    print(f"  Report: {report_path}")

    print(f"\n{'='*60}")
    print(f"  ITERATION {iteration:04d} COMPLETE")
    print(f"{'='*60}")

    return state


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hadamard Max-Det Research Agent")
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations to run")
    parser.add_argument("--state", type=str, default="state.json", help="State file path")
    args = parser.parse_args()

    state = load_state(args.state)

    for i in range(1, args.iterations + 1):
        iteration_num = state.get("iterations_completed", 0) + 1
        try:
            state = run_iteration(iteration_num, args.state)
        except Exception as e:
            print(f"\n[ERROR] Iteration {iteration_num} failed: {e}")
            import traceback
            traceback.print_exc()
            break

    print(f"\n{'='*60}")
    print(f"  RESEARCH SESSION COMPLETE")
    print(f"{'='*60}")
    print(summarize_progress(state))
