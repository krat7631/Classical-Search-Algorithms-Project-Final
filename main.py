"""CLI entry point for running search experiments."""

import argparse
import json
import sys

sys.path.insert(0, ".")

from environment.grid_world import GridWorld
from algorithms.base import SearchConstraints
from evaluation.runner import run_experiment, run_sweep, TIME_BUDGET_STRESS


DEFAULT_GRID = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
]
DEFAULT_START = (0, 0)
DEFAULT_GOAL = (4, 4)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run search algorithm experiments")
    parser.add_argument("--max-depth", type=int, default=None, help="Max search depth")
    parser.add_argument("--max-expansions", type=int, default=None, help="Max node expansions")
    parser.add_argument("--time-budget", type=float, default=None, help="Time budget in seconds")
    parser.add_argument("--all", action="store_true", help="Run baseline + constrained runs")
    parser.add_argument("--sweep", action="store_true", help="Run grid/density sweep")
    parser.add_argument("--quick", action="store_true", help="Run a smaller sweep")
    parser.add_argument("--max-size", type=int, default=None, help="Upper bound for sweep grid size")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=["bfs", "dfs", "iddfs", "astar"],
        help="Algorithms to run",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.sweep:
        constraint_configs = [
            ("baseline", None),
            ("max_depth_5", SearchConstraints(max_depth=5)),
            ("max_expansions_50", SearchConstraints(max_expansions=50)),
        ] + [
            (f"time_{t}s", SearchConstraints(time_budget_seconds=t))
            for t in TIME_BUDGET_STRESS
        ]

        if args.quick:
            grid_sizes = [(5, 5)]
            obstacle_densities = [0.0, 0.1]
            constraint_configs = constraint_configs[:5]
        else:
            grid_sizes = [(5, 5), (10, 10), (15, 15)]
            if args.max_size is not None:
                grid_sizes = [(r, c) for r, c in grid_sizes if r <= args.max_size and c <= args.max_size]
            obstacle_densities = [0.0, 0.1, 0.2]

        all_results = run_sweep(
            grid_sizes=grid_sizes,
            obstacle_densities=obstacle_densities,
            algorithms=args.algorithms,
            constraint_configs=constraint_configs,
            seed=42,
            verbose=True,
        )
        if args.format == "json":
            print(json.dumps(all_results, indent=2))
        else:
            for r in all_results:
                fail = f", fail={r.get('failure_reason', '-')}" if not r["solution_found"] else ""
                print(
                    f"[{r['grid_size']} d={r['obstacle_density']}] {r.get('config_label', '?')} "
                    f"{r['algorithm']}: found={r['solution_found']}, nodes={r['nodes_expanded']}{fail}"
                )
        return

    env = GridWorld(DEFAULT_GRID, DEFAULT_START, DEFAULT_GOAL)

    if args.all:
        configs = [
            ("Baseline (no constraints)", None),
            ("max_depth=3", SearchConstraints(max_depth=3)),
            ("max_depth=5", SearchConstraints(max_depth=5)),
            ("max_expansions=50", SearchConstraints(max_expansions=50)),
            ("max_expansions=100", SearchConstraints(max_expansions=100)),
            ("time_budget=0.01s", SearchConstraints(time_budget_seconds=0.01)),
            ("time_budget=0.1s", SearchConstraints(time_budget_seconds=0.1)),
        ]
    else:
        constraints = SearchConstraints(
            max_depth=args.max_depth,
            max_expansions=args.max_expansions,
            time_budget_seconds=args.time_budget,
        )
        if args.max_depth is None and args.max_expansions is None and args.time_budget is None:
            configs = [("Baseline (no constraints)", None)]
        else:
            configs = [("Constrained", constraints)]

    all_results = []
    for label, constraints in configs:
        all_results.extend(
            run_experiment(env, algorithms=args.algorithms, constraints=constraints, config_label=label)
        )

    if args.format == "json":
        print(json.dumps(all_results, indent=2))
    else:
        for r in all_results:
            print(
                f"[{r['config_label']}] {r['algorithm']}: found={r['solution_found']}, "
                f"path_cost={r['path_cost']}, nodes={r['nodes_expanded']}, "
                f"time={r['runtime_seconds']:.6f}s"
            )


if __name__ == "__main__":
    main()
