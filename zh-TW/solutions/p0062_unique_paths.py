"""## Task

Count paths from the top-left cell to the bottom-right cell of an m by n
grid. Each move goes one cell right or one cell down; there are no obstacles.

## Hints

1. A path into an interior cell ends at either its upper or its left neighbor.
2. Keep the preceding row, then reuse each entry when computing the next row.

## Approach

### Compressed row counts

Choose the smaller grid dimension as the row width to minimize memory.
Initialize every entry to one: the first row has exactly one path to each
cell. For each remaining row, update columns from left to right using
dp[column] += dp[column-1]. The old entry counts paths from above; the
updated left entry counts paths from the left. The first column stays one.

### Choose the down-step positions

Every route contains m-1 down moves and n-1 right moves. Choose which m-1 positions in the
fixed-length move sequence contain down moves using an exact binomial coefficient.
Accumulate that coefficient multiplicatively, dividing exactly after each factor.

## Why it works

### Compressed row counts

The last move uniquely partitions paths into two disjoint groups: paths
from above and paths from the left. Their sum therefore counts every path
exactly once. Boundary cells have only one possible route. Induction over
rows and columns proves every updated entry is the correct path count.
Transposing the dimensions preserves the right/down path count.

### Choose the down-step positions

There is a bijection between paths and subsets of down-step positions: reading a subset
produces one route, and recording a route produces that subset. Counting subsets therefore
counts paths exactly.

## Walkthrough

For a 3 by 3 grid, begin with [1,1,1]. The second row becomes [1,2,3].
The third becomes [1,3,6], so six paths reach the destination.

## Cost and pitfalls

For the default Compressed row counts approach:

O(m*n) time and O(min(m,n)) auxiliary space; dimensions are unchanged.
Update left to right so the left contribution belongs to the current row.
A single row or column naturally yields one path. Counting shortest paths
does not require BFS because every legal right/down path has the same length.

Compressed row counts: O(m*n) time; O(min(m,n)) space.
Choose the down-step positions: O(min(m,n)) arithmetic operations; O(1) integer objects.
The combinatorial variant avoids a grid table. Its exact product/division updates use
arbitrary-precision arithmetic, so bit cost and integer storage grow with the result.
"""


class Solution:
    """Approach: Compressed row counts
    Time: O(m*n)
    Space: O(min(m,n))
    """

    def uniquePaths(self, m: int, n: int) -> int:
        width, height = min(m, n), max(m, n)
        dp = [1] * width
        for _ in range(1, height):
            for column in range(1, width):
                dp[column] += dp[column - 1]
        return dp[-1]


class CombinatorialSolution:
    """Approach: Choose the down-step positions
    Time: O(min(m,n)) arithmetic operations
    Space: O(1) integer objects
    """

    def uniquePaths(self, m: int, n: int) -> int:
        steps = m + n - 2
        chosen = min(m - 1, n - 1)
        result = 1
        for count in range(1, chosen + 1):
            result = result * (steps - count + 1) // count
        return result
