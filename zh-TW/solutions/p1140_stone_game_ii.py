"""## Task

In Stone Game II, players take 1 through 2M leading piles, update M to max(M,taken), and
maximize their eventual stones.

## Hints

1. The current player receives all remaining stones except what the opponent can force.
2. The state is the remaining index and current M, regardless of player name.

## Approach

### Bottom-up suffix-total minimax

Precompute suffix totals and fill states with starting indices descending. If all remaining
piles can be taken, take them; otherwise subtract the opponent optimum after each legal
move.

### Memoized score-difference game tree

Memoize the best current-player minus opponent score, accumulating taken stones as move
length grows. Convert the initial difference and total into the first player score.

## Why it works

### Bottom-up suffix-total minimax

The game is zero-sum over the fixed remaining suffix. Every legal first move hands the
opponent a solved later-index state, so maximizing total minus opponent score gives optimal
play.

### Memoized score-difference game tree

After a move, roles swap, so subtracting the child score difference gives the current
advantage. The maximum chooses optimal play, and total=first+second with
difference=first-second determines the result.

## Walkthrough

For [2,3], the first player may take both piles immediately and obtain 5.

## Cost and pitfalls

Bottom-up suffix-total minimax: O(n^3) time; O(n^2) space.
Memoized score-difference game tree: O(n^3) time; O(n^2) space.

Inputs are unchanged. Memo depth is at most n=100, within Python limits. The two state
values differ: one is stones won, the other score advantage; their transitions must not be
mixed.
"""


class Solution:
    """Approach: Bottom-up suffix-total minimax
    Time: O(n^3)
    Space: O(n^2)
    """

    def stoneGameII(self, piles: list[int]) -> int:
        n = len(piles)
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for m in range(1, n + 1):
                dp[i][m] = (
                    suffix[i]
                    if i + 2 * m >= n
                    else max(suffix[i] - dp[i + x][max(m, x)] for x in range(1, 2 * m + 1))
                )
        return dp[0][1]


class MemoSolution:
    """Approach: Memoized score-difference game tree
    Time: O(n^3)
    Space: O(n^2)
    """

    def stoneGameII(self, piles: list[int]) -> int:
        from functools import cache

        @cache
        def difference(index, m):
            if index == len(piles):
                return 0
            taken = 0
            best = -float("inf")
            for count in range(1, min(2 * m, len(piles) - index) + 1):
                taken += piles[index + count - 1]
                best = max(best, taken - difference(index + count, max(m, count)))
            return best

        return (sum(piles) + difference(0, 1)) // 2
