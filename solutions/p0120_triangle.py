"""## Task

Find the smallest sum along a top-to-bottom triangle path, moving to either adjacent entry
in the next row.

## Hints

1. Every cell has two possible children.
2. Top-down reachability and bottom-up suffix costs need different boundaries.

## Approach

### Bottom-up suffix costs

Copy the last row, then replace its entries with the best cost from each parent through
either child. Scan columns left to right.

### Top-down prefix frontier

Build fresh prefix-cost rows. A cell receives a path from its upper-left or upper-right
parent when that parent exists.

## Why it works

### Bottom-up suffix costs

Before overwriting a parent, its two child costs are still available. Every downward path
chooses one child, so the smaller optimal child suffix gives the optimal parent suffix.

### Top-down prefix frontier

Every top-down path to a cell ends at one existing parent, so minimizing their prefix costs
is exact. The minimum last-row entry selects the cheapest possible endpoint.

## Walkthrough

For [[2],[3,4],[6,1,5]], choose 2,3,1 for sum 6.

## Cost and pitfalls

Bottom-up suffix costs: O(N) time; O(h) space.
Top-down prefix frontier: O(N) time; O(h) space.

N is total entries and h triangle height. Both preserve the nested lists; the first
explicitly copies the last row. Negative values are valid because the dependency graph is
acyclic.
"""


class Solution:
    """Approach: Bottom-up suffix costs
    Time: O(N)
    Space: O(h)
    """

    def minimumTotal(self, triangle: list[list[int]]) -> int:
        dp = triangle[-1].copy()
        for row in range(len(triangle) - 2, -1, -1):
            for column, value in enumerate(triangle[row]):
                dp[column] = value + min(dp[column], dp[column + 1])
        return dp[0]


class ForwardSolution:
    """Approach: Top-down prefix frontier
    Time: O(N)
    Space: O(h)
    """

    def minimumTotal(self, triangle: list[list[int]]) -> int:
        previous = [0]
        for row in triangle:
            current = [float("inf")] * len(row)
            for column, value in enumerate(row):
                if column < len(previous):
                    current[column] = min(current[column], previous[column] + value)
                if column:
                    current[column] = min(current[column], previous[column - 1] + value)
            previous = current
        return min(previous)
