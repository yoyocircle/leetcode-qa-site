"""## Task

Return the number of cells in a shortest zero-valued path from the top-left to bottom-right of a
square binary grid. Movement may use any of eight neighboring cells; return -1 if blocked.

## Hints

1. Each legal move costs one, so BFS gives the shortest route.
2. Chebyshev distance is a lower bound when diagonal moves are allowed.

## Approach

### Eight-direction BFS

Start an open first cell at path length one, mark cells when queued, and explore every open
eight-neighbor cell. Return on reaching the destination.

### A-star with Chebyshev heuristic

Use a heap ordered by traveled length plus max(remaining rows,remaining columns). Store best
known traveled lengths and skip stale heap entries.

## Why it works

### Eight-direction BFS

BFS layers count equal-cost moves. The first destination visit has the fewest moves, and adding
the initial cell yields the required cell-count length.

### A-star with Chebyshev heuristic

Each move can reduce Chebyshev distance by at most one, making the heuristic admissible and
consistent. A destination popped from the best-first heap therefore has optimal traveled length.

## Walkthrough

For [[0,1],[1,0]], one diagonal move reaches the endpoint, giving path length 2. A blocked first
or last cell gives -1.

## Cost and pitfalls

Eight-direction BFS: O(n^2) time; O(n^2) space.
A-star with Chebyshev heuristic: O(n^2 log(n+1)) time; O(n^2) space.
The grid is unchanged. The single open cell case returns 1. Diagonal moves do not require
adjacent side cells to be open. Store distances separately rather than changing grid values.
"""

from collections import deque
from heapq import heappop, heappush


class Solution:
    """Approach: Eight-direction BFS
    Time: O(n^2)
    Space: O(n^2)
    """

    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        if grid[0][0] or grid[-1][-1]:
            return -1
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            row, col, distance = queue.popleft()
            if row == col == n - 1:
                return distance
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    r, c = row + dr, col + dc
                    if (
                        (dr or dc)
                        and 0 <= r < n
                        and 0 <= c < n
                        and not grid[r][c]
                        and (r, c) not in seen
                    ):
                        seen.add((r, c))
                        queue.append((r, c, distance + 1))
        return -1


class AStarSolution:
    """Approach: A-star with Chebyshev heuristic
    Time: O(n^2 log(n+1))
    Space: O(n^2)
    """

    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        if grid[0][0] or grid[-1][-1]:
            return -1
        best = {(0, 0): 1}
        heap = [(n, 1, 0, 0)]
        while heap:
            _, distance, row, col = heappop(heap)
            if distance != best[row, col]:
                continue
            if row == col == n - 1:
                return distance
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    r, c = row + dr, col + dc
                    if not (dr or dc) or not (0 <= r < n and 0 <= c < n) or grid[r][c]:
                        continue
                    candidate = distance + 1
                    if candidate < best.get((r, c), float("inf")):
                        best[r, c] = candidate
                        estimate = candidate + max(n - 1 - r, n - 1 - c)
                        heappush(heap, (estimate, candidate, r, c))
        return -1
