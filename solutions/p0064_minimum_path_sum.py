"""## Task

Find the minimum sum along a path from the top-left to the bottom-right
of a nonempty rectangular grid. Moves go right or down, and both endpoint
values contribute to the sum.

## Hints

1. The last step into a cell comes from above or from the left.
2. The best path cost only needs the preceding row and current row's left cell.

## Approach

### Compressed minimum-cost row

Use one cost entry per column. Set entries to infinity, then set dp[0]
to zero as a virtual predecessor of the starting cell. Process rows from
top to bottom and columns from left to right. For each cell, take the
smaller of the old entry from above and the updated entry to its left,
then add the cell value. At column zero the left cost is infinity.

### Shortest path on weighted grid

View right/down moves as weighted directed edges that charge the destination cell. Seed the
heap with the starting cell value, relax improvements, and stop when the target is removed
with its best cost.

## Why it works

### Compressed minimum-cost row

Every path reaching a cell uses one of its legal predecessors. An optimal
path must use an optimal path to that predecessor: otherwise replacing
the prefix reduces its total. The minimum of the two predecessor optima
plus the cell value is therefore optimal. Infinity removes nonexistent
predecessors; the virtual zero seeds exactly the starting cell.

### Shortest path on weighted grid

All cell values are nonnegative, so Dijkstra finalizes a popped minimum distance. Charging
the start once and each destination once gives exactly the required path sum.

## Walkthrough

For [[2,5],[1,3]], the first row gives costs [2,7]. On the second row,
column zero becomes 3 and column one becomes min(7,3)+3=6. Return 6.

## Cost and pitfalls

For the default Compressed minimum-cost row approach:

O(rows*columns) time and O(columns) space; input is unchanged. Left-to-right
updates are essential to use the current row's left cost. Mutating the
grid is unnecessary, and choosing the cheaper immediate neighbor greedily
does not account for expensive cells later in the path.

Compressed minimum-cost row: O(R*C) time; O(C) space.
Shortest path on weighted grid: O(R*C log(R*C)) time; O(R*C) space.
Dijkstra demonstrates the graph formulation but is slower and larger than exploiting the
grid DAG. Both leave the grid unchanged.
"""


class Solution:
    """Approach: Compressed minimum-cost row
    Time: O(R*C)
    Space: O(C)
    """

    def minPathSum(self, grid: list[list[int]]) -> int:
        dp = [float("inf")] * len(grid[0])
        dp[0] = 0
        for row in grid:
            for column, value in enumerate(row):
                left = dp[column - 1] if column else float("inf")
                dp[column] = min(dp[column], left) + value
        return dp[-1]


class DijkstraSolution:
    """Approach: Shortest path on weighted grid
    Time: O(R*C log(R*C))
    Space: O(R*C)
    """

    def minPathSum(self, grid: list[list[int]]) -> int:
        from heapq import heappop, heappush

        rows, columns = len(grid), len(grid[0])
        best = {(0, 0): grid[0][0]}
        heap = [(grid[0][0], 0, 0)]
        while heap:
            cost, row, column = heappop(heap)
            if best[(row, column)] != cost:
                continue
            if (row, column) == (rows - 1, columns - 1):
                return cost
            for nr, nc in ((row + 1, column), (row, column + 1)):
                if nr < rows and nc < columns:
                    following = cost + grid[nr][nc]
                    if following < best.get((nr, nc), float("inf")):
                        best[(nr, nc)] = following
                        heappush(heap, (following, nr, nc))
        return 0
