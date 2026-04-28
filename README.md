# Hadamard Max-Det Research Agent

Autonomous AI agent for attacking the **Hadamard Maximal Determinant Problem** — open since 1893.

## The Problem

> What is the largest possible determinant of an n×n matrix with entries in {+1, −1}?

For **order n=23**, the value remains **unknown** — the smallest open case in a problem connected to error-correcting codes, quantum information, and combinatorial design.

## Architecture

A closed-loop two-agent system running autonomous mathematical research:

```
STRATEGY QUEUE → GENERATE → TEST → ANALYZE → STRATEGY INJECTION
      ↑                                              |
      └──────────── FEEDBACK LOOP ───────────────────┘
```

- **Lab Agent** (cron, every 10 min): runs test iterations, computes determinants, tracks convergence
- **Research Director Agent** (LLM): analyzes state, performs long-chain reasoning, autonomously injects novel mathematical constructions

## Results (53 iterations, 265 matrices)

| Metric | Value |
|---|---|
| Best |det| | 1,616,863,222,038,528 |
| % Barba bound | 41.25% |
| % known record | 58.17% |
| Strategies explored | 22 |
| Autonomous injections | 3 |

### Breakthrough

Simulated annealing — autonomously identified and executed by the Research Director Agent — escaped a 38.82% Barba plateau to reach 41.25%:

| Method | Best |det| |
|---|---|---|
| Simulated annealing (autonomous) | 1,616,863,222,038,528 |
| Coordinate exchange | 1,521,681,143,169,046 |
| Hadamard submatrix | 1,521,681,143,169,035 |

### Autonomous Strategy Injections

The agent independently proposed and implemented:

1. **Gram Relaxation** — build Ehlich-optimal Gram matrix in spectral domain, Cholesky factor, round to ±1
2. **SVD-Gradient Optimization** — use M⁻ᵀ as exact gradient of log|det| for principled entry flips
3. **Quasi-Williamson Array** — Goethals-Seidel construction from 4 circulant blocks (24 binary DOF)

## Quick Start

```bash
# Install dependencies
pip install numpy

# Run one research iteration
python agent.py --iterations 1

# Check latest results
cat logs/LATEST.md
```

## Project Structure

```
hadamard-research/
├── agent.py              # Main research loop (6-phase)
├── constructions.py      # Matrix construction methods
├── matrix_tester.py      # Determinant verification
├── strategy_queue.py     # Autonomous strategy management
├── strategy_queue.json   # Strategy queue (LLM-editable)
├── state.json            # Research state + best matrices
└── logs/                 # Iteration reports
```

## License

MIT
