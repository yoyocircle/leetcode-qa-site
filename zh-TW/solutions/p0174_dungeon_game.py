"""## Task

Find the minimum starting health needed to cross a dungeon right/down, staying strictly
positive after every cell.

## Hints

1. The least required health is easier to compute backward from the goal.
2. For a proposed initial health, only the greatest surviving health at each cell matters.

## Approach

### Backward required-health row

Work backward, storing the minimum health needed before entering each cell. Choose the
cheaper successor requirement, subtract the cell effect, and clamp to one.

### Binary-search feasible initial health

For a trial initial health, propagate the largest positive remaining health through a
rolling frontier; dead paths use -1. Binary-search between zero and one plus all negative
losses.

## Why it works

### Backward required-health row

A path survives exactly when its health after this cell meets one successor requirement.
Choosing the smaller successor and requiring at least one before entry gives the exact
optimal requirement.

### Binary-search feasible initial health

More initial health never hurts feasibility. At a fixed cell, greater health dominates
smaller health for every future path, so one maximum suffices for the feasibility test. The
upper bound survives every possible loss.

## Walkthrough

For [[-2,-3],[5,-4]], starting with 3 survives by moving down then right.

## Cost and pitfalls

Backward required-health row: O(R*C) time; O(C) space.
Binary-search feasible initial health: O(R*C*log B) time; O(C) space.

B is one plus the sum of negative magnitudes. Inputs are unchanged. Minimizing total path
sum does not control the lowest intermediate health; the strict positive-health rule
matters.
"""


class Solution:
    """Approach: Backward required-health row
    Time: O(R*C)
    Space: O(C)
    """

    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:
        rows, columns = len(dungeon), len(dungeon[0])
        dp = [float("inf")] * (columns + 1)
        dp[columns - 1] = 1
        for row in range(rows - 1, -1, -1):
            for column in range(columns - 1, -1, -1):
                dp[column] = max(1, min(dp[column], dp[column + 1]) - dungeon[row][column])
        return dp[0]


class BinarySearchSolution:
    """Approach: Binary-search feasible initial health
    Time: O(R*C*log B)
    Space: O(C)
    """

    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:
        def feasible(initial):
            dp = [-1] * len(dungeon[0])
            for r, row in enumerate(dungeon):
                for c, value in enumerate(row):
                    incoming = initial if r == c == 0 else max(dp[c], dp[c - 1] if c else -1)
                    dp[c] = incoming + value if incoming > 0 and incoming + value > 0 else -1
            return dp[-1] > 0

        low = 0
        high = 1 + sum(-value for row in dungeon for value in row if value < 0)
        while low + 1 < high:
            middle = (low + high) // 2
            if feasible(middle):
                high = middle
            else:
                low = middle
        return high
