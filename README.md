# Classical Search Algorithms Project

This repository implements and evaluates classical search algorithms on a deterministic grid-world pathfinding problem under shared resource constraints.

The current codebase includes:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening DFS (IDDFS)
- A* (with Manhattan heuristic)

All algorithms run in the same environment and support the same constraint interface, which allows consistent comparison.

---

## 1) What Has Been Implemented So Far

### Environment and Core Data Model
- `GridWorld` domain with:
  - 2D grid (`0 = free`, `1 = obstacle`)
  - start state and goal state
  - 4-neighbor successor function (up/down/left/right)
  - unit step cost (`1.0`)
- Shared result structure:
  - `solution_found`
  - `path`, `path_cost`
  - `nodes_expanded`
  - `runtime_seconds`
  - `failure_reason` (`time_budget`, `expansion_limit`, `depth_limit`, `exhausted`)

### Algorithms
- `bfs.py`: optimal on unit-cost grids
- `dfs.py`: depth-first traversal (not guaranteed optimal)
- `iddfs.py`: iterative deepening with DFS depth limits (optimal on unit-cost grids)
- `astar.py`: best-first using `f(n)=g(n)+h(n)` with Manhattan distance

### Shared Constraint Framework
`SearchConstraints` supports:
- `max_depth`
- `max_expansions`
- `time_budget_seconds`

The same constraint object is passed to every algorithm for fair comparison.

### Experiment/Evaluation Layer
- `evaluation/runner.py` provides:
  - single algorithm runs
  - multi-algorithm runs on same environment
  - sweeps over:
    - grid sizes
    - obstacle densities
    - constraint configurations

### CLI Runner
- `main.py` provides:
  - baseline run
  - custom constrained run
  - predefined multi-config run (`--all`)
  - systematic sweeps (`--sweep`, optional `--quick`, JSON output)

### Test Coverage
- `tests/test_algorithms.py` verifies:
  - all algorithms solve simple solvable grids
  - path validity and expected path costs on controlled maps
  - constraints are respected
  - start-equals-goal edge case

---

## 2) Repository Structure

```text
Main Project/
├── algorithms/
│   ├── base.py           # shared SearchConstraints
│   ├── bfs.py            # Breadth-First Search
│   ├── dfs.py            # Depth-First Search
│   ├── iddfs.py          # Iterative Deepening DFS
│   ├── astar.py          # A* (Manhattan heuristic)
│   └── __init__.py
├── environment/
│   ├── grid_world.py     # GridWorld, State, SearchResult, generator utilities
│   └── __init__.py
├── evaluation/
│   ├── runner.py         # experiment and sweep orchestration
│   └── __init__.py
├── tests/
│   ├── test_algorithms.py
│   └── __init__.py
├── main.py               # CLI entry point
├── run_tests.py          # unittest runner
├── requirements.txt
└── README.md
```

---

## 3) Setup and Execution

### Prerequisites
- Python 3.10+ recommended

### Install dependencies
From project root:

```bash
cd "/Users/devanshnayak/Desktop/Main Project"
pip3 install -r requirements.txt
```

Note: tests run with built-in `unittest`; `pytest` is listed but not required for `run_tests.py`.

---

## 4) How to Run the Project

All commands below assume you are in:

```bash
cd "/Users/devanshnayak/Desktop/Main Project"
```

### A) Baseline run (all algorithms, default 5x5 grid)

```bash
python3 main.py
```

### B) Run with one constraint

```bash
python3 main.py --max-depth 5
python3 main.py --max-expansions 100
python3 main.py --time-budget 0.01
```

### C) Run predefined baseline + constrained configurations

```bash
python3 main.py --all
```

### D) Run a sweep (for larger comparative experiments)

```bash
python3 main.py --sweep
python3 main.py --sweep --quick
python3 main.py --sweep --format json
```

Optional filters:

```bash
python3 main.py --sweep --max-size 10
python3 main.py --sweep --algorithms bfs astar --format json
```

### E) Run tests

```bash
python3 run_tests.py
```

---

## 5) Understanding the Constraint Behavior

`failure_reason` appears only when a run does not find a solution:
- `time_budget`: wall-clock budget exceeded
- `expansion_limit`: max expanded nodes reached
- `depth_limit`: exploration stopped due to depth cap
- `exhausted`: no path found after fully exploring allowed space

Important note on `time_budget`:
- On small/easy grids, a budget like `0.001` or `0.01` seconds may still succeed because search finishes very quickly.
- To force time-budget failures, use tighter budgets and/or larger/harder grids via `--sweep`.

---

## 6) Implementation Walkthrough (How It Works Internally)

### Step 1: Build an environment
`GridWorld` validates:
- non-empty grid
- start and goal in bounds
- start/goal not obstacles

`get_successors(state)` returns valid adjacent cells with unit cost.

### Step 2: Pass shared constraints
Create `SearchConstraints` once and pass to any algorithm:

```python
from algorithms.base import SearchConstraints
constraints = SearchConstraints(max_depth=5, max_expansions=100, time_budget_seconds=0.01)
```

### Step 3: Run algorithm and collect `SearchResult`
Each algorithm returns a `SearchResult` with comparable metrics.

### Step 4: Compare algorithms via `evaluation/runner.py`
Use `run_experiment(...)` for same grid + same constraints, or `run_sweep(...)` for many settings.

---

## 7) Planned Extension Roadmap (For Final Report Phase)

The items in this section are planned next steps, not completed features. They are included to make the implementation plan explicit and reproducible.

### A) Add a new algorithm (planned)
1. Create `algorithms/<new_algo>.py` with signature:
   - `def new_algo(env: GridWorld, constraints: Optional[SearchConstraints] = None) -> SearchResult`
2. Apply constraints in the same style/order as existing algorithms.
3. Return full `SearchResult` fields.
4. Export from `algorithms/__init__.py`.
5. Register in `evaluation/runner.py` `ALGORITHMS` map.
6. Add tests in `tests/test_algorithms.py`.

### B) Add a new heuristic for A* (planned)
1. Add heuristic function in `GridWorld` (or a dedicated heuristic module).
2. Add CLI parameter in `main.py` (for heuristic selection).
3. Pass selected heuristic to A* implementation.
4. Add tests for admissibility/behavior as needed.

### C) Add CSV export for experiments (planned)
1. Keep `run_sweep(...)` output as list of dictionaries.
2. In `main.py`, when `--format json` is selected, optionally also write to file.
3. Add `--output` argument for export path.
4. Serialize rows with `csv.DictWriter`.

### D) Add reproducible experiment plans (planned)
1. Fix random seed in sweeps.
2. Define explicit configuration matrix (sizes, densities, budgets).
3. Save results + command metadata together.
4. Generate summary tables from saved JSON/CSV.

---

## 8) Recommended Development Workflow (Used in This Project)

1. **Implement in small increments**
   - Modify one component at a time (environment, one algorithm, or runner).
2. **Run focused sanity checks early**
   - `python3 main.py --algorithms bfs dfs astar`
3. **Validate constrained behavior**
   - `python3 main.py --all`
4. **Run full tests before commit**
   - `python3 run_tests.py`
5. **Run quick experiment snapshot when relevant**
   - `python3 main.py --sweep --quick --format json`
6. **Commit clear, scoped changes**
   - One logical change per commit with an explicit message.

---

## 9) Git and Submission Hygiene

Recommended `.gitignore` entries:

```gitignore
__pycache__/
*.py[cod]
```

Optional ignores for generated outputs (if you do not want to version them):

```gitignore
results*.json
results*.txt
```

Practical submission rules followed in this repository:
- Do not commit `__pycache__` or `*.pyc` files.
- Keep generated outputs out of commits unless required by grading.
- Keep source, tests, and documentation synchronized (if behavior changes, update tests and README in the same commit).
- Prefer direct reproducible commands in README over informal instructions.

---

## 10) Current Status and Next Steps

Completed:
- GridWorld environment
- BFS / DFS / IDDFS / A*
- Shared constraints
- Unified experiment runner
- CLI for direct runs and sweeps
- Baseline unit tests

Good next improvements:
- richer A* heuristic options (zero/weighted Manhattan)
- CSV export and plotting-ready summaries
- expanded test coverage for corner cases and stress limits
- theory-oriented metrics reports
