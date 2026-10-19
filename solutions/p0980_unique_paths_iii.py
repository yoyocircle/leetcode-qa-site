"""## Task

Count orthogonal walks from the start cell to the end cell that visit every non-obstacle grid
cell exactly once.

## Hints

1. The grid has at most twenty traversable cells.
2. A visited mask and current position completely describe the remaining problem.

## Approach

### Memoized position and visited mask

Index traversable cells and cache the count for (position,visited-mask). Reaching the end
succeeds only when every traversable bit is set.

### Path-local backtracking

Keep a path-local used-cell set, recursively try unused neighbors, and undo on return. Count
reaching the endpoint only after all traversable cells are used.

## Why it works

### Memoized position and visited mask

Future legal moves depend only on current position and used cells, so cached states are
equivalent. The terminal condition admits precisely Hamiltonian start-to-end grid walks.

### Path-local backtracking

Each recursive branch adds one distinct legal neighboring cell. Every accepted branch is a
complete walk, and every legal complete walk follows one explored branch sequence.

## Walkthrough

For [[1,0,2]], the only valid route crosses the middle cell and gives 1. Reaching the endpoint
while another open cell remains does not count.

## Cost and pitfalls

Memoized position and visited mask: O(V*2^V) time; O(V*2^V) space.
Path-local backtracking: O(4^V) loose bound time; O(V) space.
The grid is unchanged. V<=20 bounds recursion depth. Memoization can consume exponential memory
but avoids repeated suffix computations. Do not walk through the endpoint and leave it again.
"""

from functools import cache


class Solution:
    """Approach: Memoized position and visited mask
    Time: O(V*2^V)
    Space: O(V*2^V)
    """

    def uniquePathsIII(self, grid: list[list[int]]) -> int:
        cells = [(r, c) for r, row in enumerate(grid) for c, value in enumerate(row) if value != -1]
        indices = {cell: index for index, cell in enumerate(cells)}
        adjacency = [[] for _ in cells]
        start = end = 0
        for index, (row, col) in enumerate(cells):
            if grid[row][col] == 1:
                start = index
            elif grid[row][col] == 2:
                end = index
            for neighbor in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if neighbor in indices:
                    adjacency[index].append(indices[neighbor])
        full = (1 << len(cells)) - 1

        @cache
        def visit(position, mask):
            if position == end:
                return int(mask == full)
            return sum(
                visit(neighbor, mask | (1 << neighbor))
                for neighbor in adjacency[position]
                if not mask & (1 << neighbor)
            )

        return visit(start, 1 << start)


class PathSetSolution:
    """Approach: Path-local backtracking
    Time: O(4^V) loose bound
    Space: O(V)
    """

    def uniquePathsIII(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        count = sum(value != -1 for row in grid for value in row)
        start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1)
        used = set()

        def visit(row, col):
            if grid[row][col] == 2:
                return int(len(used) + 1 == count)
            used.add((row, col))
            total = sum(
                visit(r, c)
                for r, c in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1))
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] != -1 and (r, c) not in used
            )
            used.remove((row, col))
            return total

        return visit(*start)
