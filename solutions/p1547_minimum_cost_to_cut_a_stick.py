"""## Task

Cut a stick of length n at all requested positions in any order, minimizing the sum of
lengths of the pieces when each cut is made.

## Hints

1. The first cut of a remaining interval splits it into independent subproblems.
2. Add endpoints zero and n so each interval cost is a boundary difference.

## Approach

### Bottom-up first-cut interval table

Sort a copied cut list between stick endpoints. An interval with no interior requested cut
costs zero; otherwise try every first cut and add the interval length once.

### Memoized endpoint-index cutting costs

Solve only requested boundary intervals on demand, caching each pair of endpoint indices.
Try each possible first cut with its two remaining cached intervals.

## Why it works

### Bottom-up first-cut interval table

Every valid cutting order has one first interior cut. It charges the full current interval,
then leaves independent left/right tasks; minimizing all such choices is necessary and
sufficient.

### Memoized endpoint-index cutting costs

The first-cut decomposition is exhaustive and subinterval costs depend only on fixed
endpoints, not earlier cuts outside them. Memoization therefore reuses identical tasks
without changing the optimum.

## Walkthrough

For n=7 and cuts [1,3,4,5], choosing 3 first permits a minimum total cost of 16.

## Cost and pitfalls

Bottom-up first-cut interval table: O(c^3) time; O(c^2) space.
Memoized endpoint-index cutting costs: O(c^3) time; O(c^2) space.

c is requested cut count plus two; sorting O(c log c) and the O(c) position copy are
included in the larger bounds. Both preserve cuts. Memo depth is at most 101 for the
official 100-cut limit. Greedily choosing a cheap immediate cut ignores how it changes
future piece lengths.
"""


class Solution:
    """Approach: Bottom-up first-cut interval table
    Time: O(c^3)
    Space: O(c^2)
    """

    def minCost(self, n: int, cuts: list[int]) -> int:
        positions = [0, *sorted(cuts), n]
        size = len(positions)
        dp = [[0] * size for _ in range(size)]
        for distance in range(2, size):
            for left in range(size - distance):
                right = left + distance
                dp[left][right] = (
                    positions[right]
                    - positions[left]
                    + min(dp[left][cut] + dp[cut][right] for cut in range(left + 1, right))
                )
        return dp[0][-1]


class MemoSolution:
    """Approach: Memoized endpoint-index cutting costs
    Time: O(c^3)
    Space: O(c^2)
    """

    def minCost(self, n: int, cuts: list[int]) -> int:
        from functools import cache

        positions = [0, *sorted(cuts), n]

        @cache
        def cost(left, right):
            if right - left <= 1:
                return 0
            return (
                positions[right]
                - positions[left]
                + min(cost(left, cut) + cost(cut, right) for cut in range(left + 1, right))
            )

        return cost(0, len(positions) - 1)
