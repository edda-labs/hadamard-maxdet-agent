# Hadamard Max-Det Research Agent

**Edda Labs** — *Research for the benefit of the people.*

Autonomous AI agent for attacking the **Hadamard Maximal Determinant Problem** — open since 1893, built on a Raspberry Pi 5.

---

## The Problem

> What is the largest possible determinant of an n×n matrix with entries in {+1, −1}?

For **order n=23**, the value remains **unknown** — the smallest open case in a problem connected to error-correcting codes, quantum information, and combinatorial design.

| Bound | Value |
|---|---|
| **World record** (Orrick et al., 2003) | 2,779,447,296,000,000 |
| **Ehlich bound** (n≡3 mod 4) | 3,341,958,861,191,168 |
| **Barba bound** (n≡1 mod 4, upper) | 3,919,726,327,358,822 |

The problem is **computationally intractable**: there are 2^529 ≈ 10^159 different matrices of order 23. Exhaustive search is impossible. Structured search and mathematical insight are required.

---

## Architecture

A closed-loop multi-agent system for autonomous mathematical research:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLOSED-LOOP RESEARCH CYCLE                    │
│                                                                  │
│   STRATEGY QUEUE ──► GENERATE ──► TEST ──► ANALYZE ──► INJECT   │
│         ▲                                              │        │
│         │              PENALTY SYSTEM                  │        │
│         └── STALE/KILL ◄── CRASH ◄── FEEDBACK ◄───────┘        │
│                                                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│   │ Strategy     │  │ Lab Agent    │  │ Research     │         │
│   │ Queue (JSON) │  │ (Python)     │  │ Director     │         │
│   │              │  │ Runs tests   │  │ (LLM)        │         │
│   │ Priority-sel │  │ Tracks best  │  │ Analyzes     │         │
│   │ Penalty-decay│  │ Records det  │  │ Injects new  │         │
│   │ Auto-kill    │  │ Phase 1-6    │  │ strategies   │         │
│   └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

- **`agent.py`** — Main research loop with 6 construction phases (Hadamard submatrix, Paley core, circulant, Toeplitz, block-circulant, random) + LLM strategy execution
- **`constructions.py`** — Matrix construction methods (Sylvester, Paley core/type I, conference matrices, circulant, Toeplitz, negacyclic)
- **`strategy_queue.py`** — Strategy queue management with priority selection, staleness penalty, crash-penalty, and auto-kill
- **`autonomous_wrapper.py`** — Orchestrates one full research cycle, handles strategy pick/execute/record with penalty feedback loop

### Strategy Queue

Strategies are Python code objects in a JSON queue, each with:
- **Priority** (1-10, higher = picked first)
- **Penalty system**: Stale strategies (no improvement for 3+ attempts) get priority decay. Crashed strategies get crash-streak tracking. Dead strategies (stale ≥ 5 or crash_streak ≥ 5) get killed and excluded.
- **Auto-inject**: When fewer than 5 healthy strategies remain, the LLM Research Director autonomously proposes and injects new strategies.

### Penalty System

| Condition | Action |
|---|---|
| No improvement for 1 run | `stale_rounds += 1`, priority −1 |
| No improvement for 3 runs | Priority −4 |
| No improvement for 5 runs | **Auto-kill**, strategy removed |
| 3+ consecutive crashes | Priority −6 (severe demotion) |
| 5+ consecutive crashes | **Dead**, excluded from queue |
| Successful run | Reset `crash_streak`, keep stale count |

---

## Results (318 runs, 1,590 matrices, 40+ strategies)

### Best Determinants Found
### Best Determinants Found

| Rank | det | % WR | % Barba | Strategy | Note |
|------|-----|------|---------|----------|------|
| &#x1f947; | 2,779,447,296,000,000 | 100.0% | 70.9% | `hermod_orrick_perturb` | Orrick world record confirmed |
| &#x1f948; | 2,385,859,554,836,488 | 85.8% | 60.9% | `auto_dft_circulant_descent` | DFT island, independent |
| &#x1f949; | 2,355,757,055,999,990 | 84.8% | 60.1% | `hermod_orrick_perturb` | Double-flip on Orrick matrix |
| 4 | 2,338,054,471,680,024 | 84.1% | 59.6% | `hermod_orrick_perturb` | Double-flip variant |
| 5 | 2,231,107,584,000,011 | 80.3% | 56.9% | `hermod_orrick_perturb` | Double-flip variant |
| 6 | 1,745,879,438,458,882 | 62.8% | 44.5% | `auto_dft_circulant_descent` | DFT v3 iteration |
| 7 | 1,616,863,222,038,528 | 58.2% | 41.2% | `hermod_simulated_annealing` | Plateau champion |
| 8 | 1,597,260,756,418,553 | 57.5% | 40.7% | `auto_block_exhaustive` | Block exhaustive |


1. **Orrick world record confirmed**: The agent loaded the 2003 record matrix and verified |det| = 2,779,447,296,000,000.

2. **DFT Island at 85.8%**: The DFT-circulant-descent strategy independently reached 2.386e15 without any Orrick seeding — a structurally different construction achieving 86% of the record.

3. **The Plateau**: Most strategies converge on the 24^11 plateau (~1.52e15, 55% WR) — the Hadamard-submatrix ceiling. At least 8 distinct strategies hit this same value, confirming it as a deep attractor in the search space.

4. **Perturbation sensitivity**: Single and double sign-flips on the Orrick matrix consistently *decrease* the determinant (to 80-85%), confirming the record sits on a steep, narrow peak.

5. **Strategy diversity**: 40+ strategies explored across Paley variations, DFT descent, simulated annealing, Gram optimization, Goethals-Seidel arrays, Williamson constructions, spectral majorization, and alternating projections.

---

## Setup

### Requirements

- Python 3.10+
- NumPy
- (Optional) LLM provider credentials for Research Director strategy injection

### Installation

```bash
# Clone the repository
git clone https://github.com/edda-labs/hadamard-maxdet-agent.git
cd hadamard-maxdet-agent

# Install dependencies
pip install numpy
```

### Running

```bash
# Single research iteration (5 matrices)
python3 agent.py --iterations 1

# Multiple iterations with verbose output
python3 agent.py --iterations 10

# Autonomous wrapper (full cycle: strategy pick → execute → record → penalty)
python3 autonomous_wrapper.py
```

### Autonomous Mode (Cron)

The agent is designed to run as a cron job with an autonomous wrapper:

```bash
# Every 5 minutes (add to your crontab)
*/5 * * * * cd /path/to/hadamard-maxdet-agent && python3 autonomous_wrapper.py >> /tmp/hadamard.log 2>&1
```

The `autonomous_wrapper.py` handles:
1. Fetching the next best strategy (considering priority + penalty)
2. Executing the strategy code via `exec()` in a sandboxed namespace
3. Recording results and updating staleness/crash metrics
4. Auto-killing dead strategies
5. Creating `INJECT_NEEDED.txt` when strategy pool drops below 3

### Adding Custom Strategies

Edit `strategy_queue.json` to inject your own strategies:

```json
{
  "id": "my_strategy",
  "code": "import numpy as np\ndef generate_matrices():\n    # Return list of (matrix, name) tuples\n    M = np.ones((23, 23), dtype=np.int8)\n    return [(M, 'my_matrix')]",
  "rationale": "Description of the mathematical approach",
  "priority": 5,
  "created_by": "your_name",
  "attempts": 0,
  "best_det": 0,
  "best_name": null
}
```

Available imports in strategy execution context:
- `numpy` as `np`
- `PROJECT_DIR` — absolute path to project directory
- `paley_core(n)` — build Paley core matrix
- `hadamard_24()` — build Hadamard matrix of order 24
- Full Python stdlib

### Project Structure

```
hadamard-maxdet-agent/
├── agent.py                 # Main research loop (6-phase)
├── autonomous_wrapper.py    # Autonomous cycle orchestrator
├── constructions.py         # Matrix construction methods
├── strategy_queue.py        # Strategy management with penalty system
├── strategy_queue.json      # Strategy queue (JSON, editable)
├── state.json               # Research state + best matrices (runtime, gitignored)
├── README.md                # This file
└── .gitignore               # Excludes state, logs, secrets
```

---

## Background

The Hadamard maximal determinant problem asks: for a given order n, what is the largest possible determinant of an n×n matrix with entries ±1? For orders where Hadamard matrices exist (n=1,2 or n≡0 mod 4), the answer is known. For other orders, the value remains open.

Order 23 is the **smallest unresolved case** (n≡3 mod 4). The Ehlich bound for n≡3 mod 4 gives the theoretical maximum, but no construction achieving it is known. The best known value comes from Orrick, Solomon, Dowdeswell, and Smith (2003), *arXiv:math/0304410*.

---

## License

MIT

---

*Built on a Raspberry Pi 5 by Edda Labs. 318 iterations, 1,590 matrices, 40+ strategies explored.*
