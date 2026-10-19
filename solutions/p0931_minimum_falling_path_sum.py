"""## Task

Find the minimum sum of a falling path through a square matrix, moving to the same or
adjacent column in the next row.

## Hints

1. A path ending in a cell comes from at most three preceding columns.
2. A suffix recurrence can instead choose among its three children.

## Approach

### Forward rolling row minima

Copy the first row as initial endpoint costs. For every later row, build a fresh row from
the minimum legal predecessor cost and add the cell value.

### Memoized suffix path costs

Memoize the cheapest path starting at each cell; invalid columns cost infinity and final-row
cells cost their own value. Choose the best top-row starting column.

## Why it works

### Forward rolling row minima

Every falling path has one predecessor among the three tested columns. Optimal prefixes can
replace nonoptimal ones without altering the final step, so the minimum recurrence is exact.

### Memoized suffix path costs

Each suffix must choose one valid child, so minimizing child optima gives the exact current
suffix cost. All start columns are allowed, making the outer minimum necessary.

## Walkthrough

For [[2,1,3],[6,5,4],[7,8,9]], a minimum path is 1,4,8 with total 13.

## Cost and pitfalls

Forward rolling row minima: O(n^2) time; O(n) space.
Memoized suffix path costs: O(n^2) time; O(n^2) space.

Both preserve matrix and support negative entries. The default first-row copy and matrix[1:]
reference slice each cost O(n) space; no nested input rows are modified. Memo depth is
bounded by side length<=100.
"""


class Solution:
    """Approach: Forward rolling row minima
    Time: O(n^2)
    Space: O(n)
    """

    def minFallingPathSum(self, matrix: list[list[int]]) -> int:
        previous = matrix[0].copy()
        for row in matrix[1:]:
            current = []
            for column, value in enumerate(row):
                best = previous[column]
                if column:
                    best = min(best, previous[column - 1])
                if column + 1 < len(row):
                    best = min(best, previous[column + 1])
                current.append(value + best)
            previous = current
        return min(previous)


class MemoSolution:
    """Approach: Memoized suffix path costs
    Time: O(n^2)
    Space: O(n^2)
    """

    def minFallingPathSum(self, matrix: list[list[int]]) -> int:
        from functools import cache

        @cache
        def suffix(row, column):
            if column < 0 or column >= len(matrix):
                return float("inf")
            if row == len(matrix) - 1:
                return matrix[row][column]
            return matrix[row][column] + min(
                suffix(row + 1, column + change) for change in (-1, 0, 1)
            )

        return min(suffix(0, column) for column in range(len(matrix)))
