"""## Task

Assign a plus or minus sign to every number and count assignments producing target.

## Hints

1. Equal signed totals can merge by adding their counts.
2. Transform a negative-sign subset into a subset-sum target.

## Approach

### Signed-sum frequency frontier

For each input position, build a new frequency map by adding its value with either sign.
Counts merge when different assignments reach the same total.

### Negative-subset count DP

If negative-signed entries sum to N, total-2N=target. Count position subsets summing to
(total-target)/2 with descending updates.

## Why it works

### Signed-sum frequency frontier

The two sign choices partition assignments by their final sign. Summing predecessor
multiplicities preserves each assignment exactly once, including two distinct choices for
zero.

### Negative-subset count DP

Choosing the negative positions is a bijection with sign assignments. Descending iteration
uses each position once; a zero doubles each count, correctly accounting for its two
possible signs.

## Walkthrough

For [0,1] and target 1, either sign on zero works, giving 2 assignments.

## Cost and pitfalls

Signed-sum frequency frontier: O(n*S) time; O(S) space.
Negative-subset count DP: O(n*S) time; O(S) space.

S is sum(nums)+1 for these bounds. Both preserve inputs. Reject impossible parity and
magnitude before allocating the subset table; equal values still represent distinct input
positions.
"""


class Solution:
    """Approach: Signed-sum frequency frontier
    Time: O(n*S)
    Space: O(S)
    """

    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        counts = {0: 1}
        for value in nums:
            following = {}
            for total, count in counts.items():
                for signed in (total + value, total - value):
                    following[signed] = following.get(signed, 0) + count
            counts = following
        return counts.get(target, 0)


class SubsetSolution:
    """Approach: Negative-subset count DP
    Time: O(n*S)
    Space: O(S)
    """

    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total - target) % 2:
            return 0
        goal = (total - target) // 2
        dp = [0] * (goal + 1)
        dp[0] = 1
        for value in nums:
            for subtotal in range(goal, value - 1, -1):
                dp[subtotal] += dp[subtotal - value]
        return dp[goal]
