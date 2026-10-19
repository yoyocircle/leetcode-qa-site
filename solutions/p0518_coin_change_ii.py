"""## Task

Count unordered combinations of unlimited positive coin denominations forming amount.

## Hints

1. A fixed denomination order avoids counting permutations.
2. A two-dimensional table separates skipping a denomination from taking it again.

## Approach

### Denomination-first rolling counts

Process denominations outside and totals ascending inside. Each update adds combinations
whose greatest processed denomination is the current coin.

### Coin-prefix and amount table

Store counts for every prefix of denominations. Add the previous row for excluding the coin
and the same row at a smaller amount for including one more copy.

## Why it works

### Denomination-first rolling counts

Combinations are classified by how many copies of the current denomination they use.
Ascending totals permit repeated copies; outer denomination order counts each multiset only
once.

### Coin-prefix and amount table

Excluding and including the newest coin are disjoint and exhaustive. The same-row transition
leaves that coin available, while excluding it moves to the preceding denomination set.

## Walkthrough

With coins [1,2] and amount 3, [1,1,1] and [1,2] give 2 combinations.

## Cost and pitfalls

Denomination-first rolling counts: O(C*A) time; O(A) space.
Coin-prefix and amount table: O(C*A) time; O(C*A+C+A) space.

C is coin count and A amount. Zero amount has one empty combination. Both preserve inputs;
amount-first loop order would count ordered sequences instead.
"""


class Solution:
    """Approach: Denomination-first rolling counts
    Time: O(C*A)
    Space: O(A)
    """

    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for total in range(coin, amount + 1):
                dp[total] += dp[total - coin]
        return dp[amount]


class TableSolution:
    """Approach: Coin-prefix and amount table
    Time: O(C*A)
    Space: O(C*A+C+A)
    """

    def change(self, amount: int, coins: list[int]) -> int:
        dp = [[0] * (amount + 1) for _ in range(len(coins) + 1)]
        dp[0][0] = 1
        for count, coin in enumerate(coins, 1):
            for total in range(amount + 1):
                dp[count][total] = dp[count - 1][total]
                if total >= coin:
                    dp[count][total] += dp[count][total - coin]
        return dp[-1][-1]
