"""## Task

Split n into at least two positive integers and maximize their product.

## Hints

1. The first piece leaves a remainder that may be split or kept whole.
2. For large remainders, factors of three outperform longer pieces.

## Approach

### Best product by total

For each total, choose its first piece and either keep or optimally split the remainder. The
outer split always creates at least two pieces.

### Factors of three with a remainder adjustment

Use as many threes as possible, except replace a final 3+1 with 2+2. Handle two and three
separately because a split is required.

## Why it works

### Best product by total

Every partition has a first piece; its remainder is either a single piece or another
partition. Trying every first value covers every valid partition.

### Factors of three with a remainder adjustment

A piece at least five improves when replaced by 3 and its remainder. Ones reduce product,
and three twos improve to two threes. Only threes with at most two twos remain optimal.

## Walkthrough

For n=8, use 3+3+2 and obtain product 18.

## Cost and pitfalls

Best product by total: O(n^2) time; O(n) space.
Factors of three with a remainder adjustment: O(log n) arithmetic operations time; O(1)
integer objects space.

No inputs are mutated. Exponentiation uses growing integers; bit cost is additional to
arithmetic-operation counts. Returning n itself for n=2 or n=3 violates the required split.
"""


class Solution:
    """Approach: Best product by total
    Time: O(n^2)
    Space: O(n)
    """

    def integerBreak(self, n: int) -> int:
        dp = [0] * (n + 1)
        for total in range(2, n + 1):
            dp[total] = max(
                first * max(total - first, dp[total - first]) for first in range(1, total)
            )
        return dp[n]


class GreedySolution:
    """Approach: Factors of three with a remainder adjustment
    Time: O(log n) arithmetic operations
    Space: O(1) integer objects
    """

    def integerBreak(self, n: int) -> int:
        if n <= 3:
            return n - 1
        threes, remainder = divmod(n, 3)
        if remainder == 1:
            return 3 ** (threes - 1) * 4
        return 3**threes * (2 if remainder else 1)
