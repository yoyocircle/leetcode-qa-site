"""
## Task

For positive integers nums and positive target, return the shortest nonempty contiguous subarray
with sum at least target, or zero if none exists.

## Hints

1. Positive values make shrinking reduce the sum.
2. Prefix sums are strictly increasing and can be binary-searched.

## Approach

### Shrinking positive-sum window

Extend right, then remove left values while the sum still reaches target, recording each valid
length.

### Prefix sums and lower bounds

Build increasing prefix sums. For each starting prefix, binary-search the first ending prefix
reaching target more.

## Why it works

### Shrinking positive-sum window

For each right endpoint, shrinking finds its shortest valid window. Any earlier discarded left
boundary only gives longer windows at later endpoints.

### Prefix sums and lower bounds

Prefix[j]-prefix[i] is the subarray sum. Strictly increasing prefixes make lower bound return
the shortest feasible end for that start; minimizing across starts finds the global optimum.

## Walkthrough

For target 7 and [2,3,1,2,4,3], the final window [4,3] has length 2. Positive values are why the
left boundary never needs to move backward.

## Cost and pitfalls

Shrinking positive-sum window: O(n) time; O(1) space.

Prefix sums and lower bounds: O(n log n) time; O(n) space.

Inputs are unchanged. These window and binary-search invariants do not extend to arbitrary
negative values.
"""

from bisect import bisect_left


class Solution:
    """Approach: Shrinking positive-sum window
    Time: O(n)
    Space: O(1)
    """

    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        left = total = 0
        best = len(nums) + 1
        for right, value in enumerate(nums):
            total += value
            while total >= target:
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if best > len(nums) else best


class PrefixSearchSolution:
    """Approach: Prefix sums and lower bounds
    Time: O(n log n)
    Space: O(n)
    """

    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        best = len(nums) + 1
        for i in range(len(nums)):
            j = bisect_left(prefix, prefix[i] + target, i + 1)
            if j < len(prefix):
                best = min(best, j - i)
        return 0 if best > len(nums) else best
