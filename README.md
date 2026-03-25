# Main Project

This project implements and evaluates classical search algorithms on a grid-world pathfinding problem.

## Current Scope

Implemented algorithms:
- BFS
- DFS
- IDDFS
- A* (Manhattan heuristic)

Shared constraints available for all algorithms:
- `max_depth`
- `max_expansions`
- `time_budget_seconds`

## Project Structure

```
Main Project/
├── algorithms/
│   ├── base.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── iddfs.py
│   ├── astar.py
│   └── __init__.py
├── environment/
│   ├── grid_world.py
│   └── __init__.py
├── evaluation/
│   ├── runner.py
│   └── __init__.py
├── tests/
│   ├── test_algorithms.py
│   └── __init__.py
├── main.py
├── run_tests.py
├── requirements.txt
└── README.md
```

## How to Run

Run from inside this folder:

```bash
cd "Main Project"
```

Baseline run:

```bash
python3 main.py
```

Run with constraints:

```bash
python3 main.py --max-depth 5
python3 main.py --max-expansions 100
python3 main.py --time-budget 0.1
```

Run predefined baseline + constrained configurations:

```bash
python3 main.py --all
```

Run sweeps over grid sizes, obstacle densities, and constraints:

```bash
python3 main.py --sweep
python3 main.py --sweep --quick
python3 main.py --sweep --format json
```

Run tests:

```bash
python3 run_tests.py
```

## Notes

- The code is intentionally focused on core algorithm implementation and evaluation.
- Advanced theory-specific modules and export utilities are not part of this submission snapshot.
