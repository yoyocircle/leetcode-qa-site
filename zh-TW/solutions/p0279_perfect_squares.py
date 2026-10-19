"""## Task

Express n as a sum of perfect squares using as few terms as possible.

## Hints

1. Use the final square to reduce to a smaller total.
2. Four squares always suffice; distinguish answers one, two, three, and four.

## Approach

### Bottom-up square-count table

Precompute square denominations and fill minimum term counts from zero upward, testing each
feasible final square.

### Square classification theorems

First test one square. Remove factors of four and test the 8b+7 obstruction to three
squares. Otherwise search for a two-square decomposition and return three if absent.

## Why it works

### Bottom-up square-count table

Every representation has a final square. Removing it reaches an already solved smaller
amount, and every finite predecessor extends to a valid representation.

### Square classification theorems

Lagrange guarantees at most four squares. Legendre characterizes numbers requiring four
after removing powers of four. Exact one- and two-square tests distinguish the remaining
possibilities.

## Walkthrough

For n=13, 4+9 uses two squares; for n=12, 4+4+4 uses three.

## Cost and pitfalls

Bottom-up square-count table: O(n*sqrt(n)) time; O(n) space.
Square classification theorems: O(sqrt(n)) time; O(1) space.

The number-theory variant relies on these classical theorems rather than the DP recurrence.
isqrt avoids floating-point rounding; arithmetic uses bounded problem-sized integers.
"""


class Solution:
    """Approach: Bottom-up square-count table
    Time: O(n*sqrt(n))
    Space: O(n)
    """

    def numSquares(self, n: int) -> int:
        from math import isqrt

        squares = [value * value for value in range(1, isqrt(n) + 1)]
        dp = [0] + [n + 1] * n
        for total in range(1, n + 1):
            for square in squares:
                if square > total:
                    break
                dp[total] = min(dp[total], dp[total - square] + 1)
        return dp[n]


class NumberTheorySolution:
    """Approach: Square classification theorems
    Time: O(sqrt(n))
    Space: O(1)
    """

    def numSquares(self, n: int) -> int:
        from math import isqrt

        if isqrt(n) ** 2 == n:
            return 1
        reduced = n
        while reduced % 4 == 0:
            reduced //= 4
        if reduced % 8 == 7:
            return 4
        for first in range(1, isqrt(n) + 1):
            remainder = n - first * first
            if isqrt(remainder) ** 2 == remainder:
                return 2
        return 3
