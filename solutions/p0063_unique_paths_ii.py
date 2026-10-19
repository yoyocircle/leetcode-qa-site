"""## Task

Count right/down paths in a grid whose cells marked one are blocked.

## Hints

1. A blocked cell contributes zero paths.
2. Keep obstacle decisions in the recurrence rather than modifying the grid.

## Approach

### Rolling obstacle-aware row

Seed a virtual path into the start. Scan rows left to right, clearing blocked cells and
adding the above and current-left counts for open cells.

### Padded full path table

Keep all cell counts in a table padded with a zero top row and left column. One virtual
predecessor supplies the starting path.

## Why it works

### Rolling obstacle-aware row

Every path to an open cell ends above or left; these groups are disjoint. Clearing a blocked
cell prevents paths from crossing it, including a blocked start.

### Padded full path table

Padding gives zero contribution from nonexistent predecessors. The virtual seed enters only
the starting cell, while every later nonblocked cell sums its two legal predecessor counts.

## Walkthrough

For [[0,0],[1,0]], only right then down reaches the destination.

## Cost and pitfalls

Rolling obstacle-aware row: O(R*C) time; O(C) space.
Padded full path table: O(R*C) time; O(R*C) space.

Both preserve the grid. The table makes every intermediate count inspectable; the rolling
row saves memory. Do not retain an above contribution when the current cell is blocked.
"""


class Solution:
    """Approach: Rolling obstacle-aware row
    Time: O(R*C)
    Space: O(C)
    """

    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        dp = [0] * len(obstacleGrid[0])
        dp[0] = 1
        for row in obstacleGrid:
            for column, blocked in enumerate(row):
                if blocked:
                    dp[column] = 0
                elif column:
                    dp[column] += dp[column - 1]
        return dp[-1]


class TableSolution:
    """Approach: Padded full path table
    Time: O(R*C)
    Space: O(R*C)
    """

    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        rows, columns = len(obstacleGrid), len(obstacleGrid[0])
        table = [[0] * (columns + 1) for _ in range(rows + 1)]
        table[0][1] = 1
        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                if not obstacleGrid[row - 1][column - 1]:
                    table[row][column] = table[row - 1][column] + table[row][column - 1]
        return table[-1][-1]
