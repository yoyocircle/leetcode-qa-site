"""## Task

A binary grid contains exactly two orthogonally connected islands. Return the minimum number of
water cells to change into land to connect them.

## Hints

1. Treat every cell of the first island as a distance-zero source.
2. Without obstacles, a closest pair of island cells also gives a Manhattan-distance baseline.

## Approach

### Island discovery and multi-source BFS

Iteratively mark one whole island, then expand a BFS through water from all its cells. Touching
unmarked land reaches the second island; the current distance is the flip count.

### All-pairs island Manhattan distance

Discover both island cell lists and minimize Manhattan distance minus one over their Cartesian
product. This educational baseline avoids BFS but compares many pairs.

## Why it works

### Island discovery and multi-source BFS

The source frontier permits any departure point on the first island. BFS explores water by
minimum number of flips, so its first contact with the second island is optimal.

### All-pairs island Manhattan distance

Any bridge path between endpoint cells needs at least their Manhattan distance minus one water
positions. A shortest coordinate path for a closest pair attains that minimum; encountering
island land earlier would only provide a closer endpoint pair.

## Walkthrough

For [[1,0,0],[0,0,1],[0,0,1]], a closest pair of island cells has Manhattan distance 3, so two
water flips suffice.

## Cost and pitfalls

Island discovery and multi-source BFS: O(R*C) time; O(R*C) space.
All-pairs island Manhattan distance: O(R*C+A*B); may time out time; O(R*C) space.
The grid is unchanged. A and B are island sizes; the pairwise baseline may time out for large
islands. Mark the entire first island before expansion, and do not count its existing land as
flipped water.
"""

from collections import deque


class Solution:
    """Approach: Island discovery and multi-source BFS
    Time: O(R*C)
    Space: O(R*C)
    """

    def shortestBridge(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c])
        seen = {start}
        stack = [start]
        while stack:
            row, col = stack.pop()
            for r, c in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] and (r, c) not in seen:
                    seen.add((r, c))
                    stack.append((r, c))
        queue = deque((r, c, 0) for r, c in seen)
        while queue:
            row, col, distance = queue.popleft()
            for r, c in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if 0 <= r < rows and 0 <= c < cols and (r, c) not in seen:
                    if grid[r][c]:
                        return distance
                    seen.add((r, c))
                    queue.append((r, c, distance + 1))
        raise AssertionError("The input contains exactly two islands")


class PairDistanceSolution:
    """Approach: All-pairs island Manhattan distance
    Time: O(R*C+A*B); may time out
    Space: O(R*C)
    """

    def shortestBridge(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        seen, islands = set(), []
        for row in range(rows):
            for col in range(cols):
                if not grid[row][col] or (row, col) in seen:
                    continue
                island = []
                stack = [(row, col)]
                seen.add((row, col))
                while stack:
                    r, c = stack.pop()
                    island.append((r, c))
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and grid[nr][nc]
                            and (nr, nc) not in seen
                        ):
                            seen.add((nr, nc))
                            stack.append((nr, nc))
                islands.append(island)
        return min(abs(a - c) + abs(b - d) - 1 for a, b in islands[0] for c, d in islands[1])
