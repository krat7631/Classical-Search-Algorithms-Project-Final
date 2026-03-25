"""A* search with Manhattan heuristic on GridWorld."""

import heapq
import time
from itertools import count
from typing import Optional

from environment.grid_world import GridWorld, State, SearchResult, build_path
from .base import SearchConstraints


def astar(env: GridWorld, constraints: Optional[SearchConstraints] = None) -> SearchResult:
    """Run A* using GridWorld Manhattan distance as heuristic."""
    constraints = constraints or SearchConstraints()
    start_time = time.perf_counter()
    nodes_expanded = 0

    start = env.start
    goal = env.goal

    g_score: dict[State, float] = {start: 0.0}
    parent: dict[State, Optional[State]] = {start: None}

    tie = count()
    open_heap: list[tuple[float, int, State]] = []
    heapq.heappush(open_heap, (env.manhattan_distance(start), next(tie), start))

    closed: set[State] = set()
    failure_reason: Optional[str] = 'exhausted'

    while open_heap:
        if constraints.time_budget_seconds is not None:
            if time.perf_counter() - start_time > constraints.time_budget_seconds:
                failure_reason = 'time_budget'
                break

        if constraints.max_expansions is not None and nodes_expanded >= constraints.max_expansions:
            failure_reason = 'expansion_limit'
            break

        _, _, state = heapq.heappop(open_heap)
        if state in closed:
            continue

        depth = int(g_score[state])
        nodes_expanded += 1

        if state == goal:
            path = build_path(parent, state)
            path_cost = g_score[state]
            return SearchResult(
                solution_found=True,
                path=path,
                path_cost=float(path_cost),
                nodes_expanded=nodes_expanded,
                runtime_seconds=time.perf_counter() - start_time,
            )

        closed.add(state)

        if constraints.max_depth is not None and depth >= constraints.max_depth:
            continue

        for succ, step_cost in env.get_successors(state):
            tentative_g = g_score[state] + step_cost
            if succ in closed and tentative_g >= g_score.get(succ, float('inf')):
                continue
            if tentative_g < g_score.get(succ, float('inf')):
                parent[succ] = state
                g_score[succ] = tentative_g
                f_score = tentative_g + env.manhattan_distance(succ)
                heapq.heappush(open_heap, (f_score, next(tie), succ))

    runtime = time.perf_counter() - start_time
    if failure_reason == 'exhausted' and constraints.max_depth is not None:
        failure_reason = 'depth_limit'
    return SearchResult(
        solution_found=False,
        path=[],
        path_cost=0.0,
        nodes_expanded=nodes_expanded,
        runtime_seconds=runtime,
        failure_reason=failure_reason,
    )
