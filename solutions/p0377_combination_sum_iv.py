"""## Task

Count ordered sequences of positive distinct numbers summing to target; numbers may be reused.

## Hints

1. Choose the final number rather than a sorted combination.
2. Path counts in the increasing-sum DAG also count ordered sequences.

## Approach

### Final-element amount DP

Visit totals ascending and sum counts from every possible final value. The empty sequence
seeds total zero.

### Forward path propagation

Keep a sparse dictionary of reachable sums and propagate each solved count along all
one-number append edges.

## Why it works

### Final-element amount DP

Every nonempty sequence has one unique final value. Removing it leaves a sequence at a
smaller total, so summing predecessor counts counts each ordered sequence once.

### Forward path propagation

Positive values give a topological increasing-sum order. Every path to a total represents
exactly one ordered sequence, and distributing its count along each outgoing edge counts all
extensions.

## Walkthrough

For nums=[1,2] and target=3, sequences [1,1,1], [1,2], and [2,1] give 3.

## Cost and pitfalls

Final-element amount DP: O(n*T) time; O(T) space.
Forward path propagation: O(n*T) time; O(T) space.

T is target. Inputs are unchanged. Reversing the loops into denomination-first iteration
counts unordered combinations instead. Python count arithmetic has additional cost when
intermediate counts grow.
"""


class Solution:
    """Approach: Final-element amount DP
    Time: O(n*T)
    Space: O(T)
    """

    def combinationSum4(self, nums: list[int], target: int) -> int:
        dp = [0] * (target + 1)
        dp[0] = 1
        for total in range(1, target + 1):
            dp[total] = sum(dp[total - value] for value in nums if value <= total)
        return dp[target]


class ForwardSolution:
    """Approach: Forward path propagation
    Time: O(n*T)
    Space: O(T)
    """

    def combinationSum4(self, nums: list[int], target: int) -> int:
        ways = {0: 1}
        for total in range(target + 1):
            count = ways.get(total, 0)
            if not count:
                continue
            for value in nums:
                following = total + value
                if following <= target:
                    ways[following] = ways.get(following, 0) + count
        return ways.get(target, 0)
