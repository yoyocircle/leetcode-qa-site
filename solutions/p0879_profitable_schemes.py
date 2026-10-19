"""## Task

Count subsets of crimes using at most n people and earning at least minProfit, modulo
1,000,000,007; every crime may be selected once.

## Hints

1. Profits above the target can be capped at the target.
2. Dense arrays and sparse maps can store the same people/profit frontier differently.

## Approach

### Dense capped-profit knapsack

Track exact people used and profit capped at the goal. Visit used people backward for each
crime, adding take choices while existing counts represent skip choices.

### Sparse copied state frontier

Store only reachable (people used, capped profit) states in a dictionary. Copy the skip
frontier, then add every feasible take transition from the old frontier.

## Why it works

### Dense capped-profit knapsack

All profits at or above the goal have identical future relevance and may merge. Backward
people iteration reads only pre-crime source states because every crime uses at least one
person, so each crime is counted at most once.

### Sparse copied state frontier

Take and skip subsets are disjoint, so their counts add. Reading the old dictionary prevents
repeated use of the current crime; merging equal states preserves all multiplicities while
discarding irrelevant history.

## Walkthrough

For n=5, minProfit=3, group=[2,2], profit=[2,3], choose the second crime alone or both,
giving 2.

## Cost and pitfalls

Dense capped-profit knapsack: O(C*n*P) time; O(n*P) space.
Sparse copied state frontier: O(C*n*P) expected time; O(n*P) space.

C is crime count and P=minProfit+1, so the zero-target case is included in the bounds.
Inputs remain unchanged. Dense storage has lower per-state overhead; sparse storage can skip
unreachable combinations but copies its frontier each round. The empty subset is valid when
minProfit=0.
"""


class Solution:
    """Approach: Dense capped-profit knapsack
    Time: O(C*n*P)
    Space: O(n*P)
    """

    def profitableSchemes(self, n: int, minProfit: int, group: list[int], profit: list[int]) -> int:
        modulus = 1_000_000_007
        dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for people, gain in zip(group, profit, strict=True):
            for used in range(n - people, -1, -1):
                for earned in range(minProfit, -1, -1):
                    following = min(minProfit, earned + gain)
                    dp[used + people][following] = (
                        dp[used + people][following] + dp[used][earned]
                    ) % modulus
        return sum(row[minProfit] for row in dp) % modulus


class SparseSolution:
    """Approach: Sparse copied state frontier
    Time: O(C*n*P) expected
    Space: O(n*P)
    """

    def profitableSchemes(self, n: int, minProfit: int, group: list[int], profit: list[int]) -> int:
        modulus = 1_000_000_007
        counts = {(0, 0): 1}
        for people, gain in zip(group, profit, strict=True):
            following = counts.copy()
            for (used, earned), count in counts.items():
                if used + people <= n:
                    state = (used + people, min(minProfit, earned + gain))
                    following[state] = (following.get(state, 0) + count) % modulus
            counts = following
        return sum(count for (_, earned), count in counts.items() if earned == minProfit) % modulus
