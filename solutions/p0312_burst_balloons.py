"""## Task

Burst every balloon to maximize total coins. Bursting one gives its value
times its current left and right neighbors' values. A missing neighbor has
value one, and bursting removes the balloon.

## Hints

1. Choosing the first balloon changes both neighboring subproblems.
2. Choose the last balloon inside an interval; its two boundary neighbors survive.

## Approach

### Bottom-up last-burst intervals

Copy the values between two virtual boundary balloons of value one. Define
dp[left][right] as the optimum for bursting all balloons strictly between
those boundaries while leaving them intact. Empty intervals cost zero.
Process intervals by increasing boundary distance. Try each interior index
as the last balloon: combine the two smaller interval optima with the
product of the left boundary, that balloon, and the right boundary.

### Memoized last-burst intervals

Memoize intervals on demand instead of filling them by width. Each call selects the final
interior balloon and combines the two independent boundary-preserving subintervals.

## Why it works

### Bottom-up last-burst intervals

If index k is last in an interval, its final neighbors are exactly the
fixed boundaries. Earlier bursts on its left and right do not interact
because k separates them. Their independent optima plus the final product
therefore give the best order ending at k. Every burst order has a last
index, so maximizing over all of them covers every possible order.

### Memoized last-burst intervals

Fixing the last balloon keeps its boundary neighbors alive. Left and right burst orders then
contribute independently, so testing every last index covers every possible order and
memoization reuses equal intervals.

## Walkthrough

For [2,3], bursting 2 first earns 1*2*3=6, then 3 earns 3, totaling 9.
Bursting 3 first earns 6, then 2 earns 2, totaling 8. The full interval
chooses 3 as its last balloon and returns 9.

## Cost and pitfalls

For the default Bottom-up last-burst intervals approach:

O(n^3) time and O(n^2) space, including an O(n) padded copy; input is
unchanged. Boundaries are excluded from their interval. Local greedy choices
miss how each removal changes future neighbor products.

Bottom-up last-burst intervals: O(n^3) time; O(n^2) space.
Memoized last-burst intervals: O(n^3) time; O(n^2) space.
Both allocate a padded O(n) copy and leave nums unchanged. Memo recursion depth is at most
n+1 with n at most 300; it does not scale to unbounded input depths.
"""


class Solution:
    """Approach: Bottom-up last-burst intervals
    Time: O(n^3)
    Space: O(n^2)
    """

    def maxCoins(self, nums: list[int]) -> int:
        values = [1, *nums, 1]
        size = len(values)
        dp = [[0] * size for _ in range(size)]
        for distance in range(2, size):
            for left in range(size - distance):
                right = left + distance
                dp[left][right] = max(
                    dp[left][last] + values[left] * values[last] * values[right] + dp[last][right]
                    for last in range(left + 1, right)
                )
        return dp[0][-1]


class MemoSolution:
    """Approach: Memoized last-burst intervals
    Time: O(n^3)
    Space: O(n^2)
    """

    def maxCoins(self, nums: list[int]) -> int:
        from functools import cache

        values = [1, *nums, 1]

        @cache
        def solve(left, right):
            if right - left <= 1:
                return 0
            return max(
                solve(left, last) + values[left] * values[last] * values[right] + solve(last, right)
                for last in range(left + 1, right)
            )

        return solve(0, len(values) - 1)
