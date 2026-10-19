"""## Task

Find the fewest coins needed to form a target amount, using positive coin
denominations as often as desired. Return -1 if no combination forms it.

## Hints

1. Choose the final coin and ask for the best way to make the remaining amount.
2. Smaller amounts come first, and an impossible amount needs a distinct state.

## Approach

### Bottom-up amount table

Let dp[x] be the minimum coin count for amount x. Set dp[0]=0. Initialize
other entries to amount+1, a sentinel larger than any possible answer because
every denomination is at least one. Visit totals in ascending order. For
each coin no larger than the total, consider dp[total-coin]+1. Return -1
when the target still has the sentinel value.

### Breadth-first sums

Treat totals 0 through A as vertices and adding one coin as an edge. BFS starts at zero,
marks sums when enqueued, and returns the first target distance. C is the number of
denominations.

## Why it works

### Bottom-up amount table

Every nonempty combination has a final coin. Removing it leaves a smaller
total whose optimum is already known. Trying every possible final coin
therefore finds a combination no worse than any valid one. Every finite
candidate extends an achievable smaller amount, so it also represents a
valid combination. Induction establishes every table entry's optimum.

### Breadth-first sums

Every edge uses exactly one coin, so BFS layers equal coin counts. Every valid combination
defines a path. First arrival is therefore the minimum count; exhaustion proves
impossibility.

## Walkthrough

With coins [2,5] and amount 7, totals 2 and 5 each need one coin. At 7,
using 2 after 5 or 5 after 2 needs two coins. Amount 3 stays impossible.

## Cost and pitfalls

For the default Bottom-up amount table approach:

O(amount * number_of_coins) time and O(amount) space; inputs are unchanged.
Ascending totals permit repeated use of the same coin. Greedily selecting
the largest denomination fails for sets such as [1,3,4] and target 6.

Bottom-up amount table: O(A*C) time; O(A) space.
Breadth-first sums: O(A*C) time; O(A) space.
BFS can stop before solving all sums, but stores a queue and visited set. Positive coin
values make the bounded state graph sufficient.
"""


class Solution:
    """Approach: Bottom-up amount table
    Time: O(A*C)
    Space: O(A)
    """

    def coinChange(self, coins: list[int], amount: int) -> int:
        impossible = amount + 1
        dp = [impossible] * (amount + 1)
        dp[0] = 0
        for total in range(1, amount + 1):
            for coin in coins:
                if coin <= total:
                    dp[total] = min(dp[total], dp[total - coin] + 1)
        return -1 if dp[amount] == impossible else dp[amount]


class BFSSolution:
    """Approach: Breadth-first sums
    Time: O(A*C)
    Space: O(A)
    """

    def coinChange(self, coins: list[int], amount: int) -> int:
        from collections import deque

        queue = deque([(0, 0)])
        seen = {0}
        while queue:
            total, count = queue.popleft()
            if total == amount:
                return count
            for coin in coins:
                following = total + coin
                if following <= amount and following not in seen:
                    seen.add(following)
                    queue.append((following, count + 1))
        return -1
