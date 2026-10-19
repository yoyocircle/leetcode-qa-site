"""## Task

Find the earliest water level allowing travel across a square elevation grid, with each
visited elevation at most that level.

## Hints

1. A route costs its greatest visited elevation.
2. Reachability is monotone as the water level rises.

## Approach

### Minimax elevation Dijkstra

Heap-expand the smallest achievable maximum elevation and relax neighbors by taking the
maximum with their elevation.

### Binary-search water level and flood-fill

Binary-search levels between the endpoint minimum requirement and n²-1, testing each with an
iterative flood-fill restricted to submerged cells.

## Why it works

### Minimax elevation Dijkstra

Path costs never decrease on extension, so the smallest pending bottleneck finalizes just as
in Dijkstra. The popped goal has the least possible water requirement.

### Binary-search water level and flood-fill

Increasing level only adds traversable cells, so feasibility is monotone. Flood-fill exactly
decides a level, and binary search isolates its first feasible value.

## Walkthrough

For [[0,2],[1,3]], the destination forces water level at least 3, which suffices.

## Cost and pitfalls

Minimax elevation Dijkstra: O(n^2 log n) time; O(n^2) space.
Binary-search water level and flood-fill: O(n^2 log n) time; O(n^2) space.

Both preserve the grid and avoid recursion. n is side length; elevations are a permutation
of 0 through n²-1. Water cost is maximum cell height, unlike maximum adjacent difference in
problem 1631.
"""


class Solution:
    """Approach: Minimax elevation Dijkstra
    Time: O(n^2 log n)
    Space: O(n^2)
    """

    def swimInWater(self, grid: list[list[int]]) -> int:
        from heapq import heappop, heappush

        n = len(grid)
        best = {(0, 0): grid[0][0]}
        heap = [(grid[0][0], 0, 0)]
        while heap:
            level, r, c = heappop(heap)
            if level != best[(r, c)]:
                continue
            if (r, c) == (n - 1, n - 1):
                return level
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < n and 0 <= nc < n:
                    candidate = max(level, grid[nr][nc])
                    if candidate < best.get((nr, nc), float("inf")):
                        best[(nr, nc)] = candidate
                        heappush(heap, (candidate, nr, nc))
        return -1


class BinarySearchSolution:
    """Approach: Binary-search water level and flood-fill
    Time: O(n^2 log n)
    Space: O(n^2)
    """

    def swimInWater(self, grid: list[list[int]]) -> int:
        n = len(grid)

        def reachable(level):
            seen, stack = {(0, 0)}, [(0, 0)]
            while stack:
                r, c = stack.pop()
                if (r, c) == (n - 1, n - 1):
                    return True
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if (
                        0 <= nr < n
                        and 0 <= nc < n
                        and grid[nr][nc] <= level
                        and (nr, nc) not in seen
                    ):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return False

        low = max(grid[0][0], grid[-1][-1]) - 1
        high = n * n - 1
        while low + 1 < high:
            middle = (low + high) // 2
            if reachable(middle):
                high = middle
            else:
                low = middle
        return high
