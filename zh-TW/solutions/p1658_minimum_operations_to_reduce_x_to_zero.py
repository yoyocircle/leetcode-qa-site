"""
## Task

Remove one element from either end per operation, decreasing x by its value. Return the fewest
operations reaching exactly zero, or -1. Array values are positive.

## Hints

1. Elements not removed form one contiguous middle window.
2. Alternatively combine a left removed prefix with a disjoint right removed suffix.

## Approach

### Longest retained positive-sum window

Find the longest middle window with sum total-x using a shrinking positive-sum window, then
subtract its length from n.

### Removed-prefix map and suffix enumeration

Map each left-prefix sum to its removal count. Enumerate right-suffix sums and look up the
remaining amount, accepting only disjoint sides.

## Why it works

### Longest retained positive-sum window

Every valid removal leaves exactly one window of sum total-x, and conversely every such window
defines a valid prefix/suffix removal. Maximizing retained length therefore minimizes
operations.

### Removed-prefix map and suffix enumeration

Every removal is a unique pair of prefix and suffix lengths whose sums add to x. Positive values
make each prefix sum unique; checking all suffixes and enforcing total length at most n covers
exactly the valid pairs.

## Walkthrough

[1,1,4,2,3], x=5 keeps the middle [1,1,4] and removes the final [2,3] in two operations. If x
equals the total, removing all n elements is permitted.

## Cost and pitfalls

Longest retained positive-sum window: O(n) time; O(1) space.

Removed-prefix map and suffix enumeration: O(n) expected time; O(n) space.

Inputs are unchanged. Empty retained windows must be allowed. Positivity is essential for both
the monotone window and unique prefix-sum count map.
"""


class Solution:
    """Approach: Longest retained positive-sum window
    Time: O(n)
    Space: O(1)
    """

    def minOperations(self, nums: list[int], x: int) -> int:
        target = sum(nums) - x
        if target < 0:
            return -1
        left = total = 0
        longest = 0 if target == 0 else -1
        for right, value in enumerate(nums):
            total += value
            while total > target:
                total -= nums[left]
                left += 1
            if total == target:
                longest = max(longest, right - left + 1)
        return -1 if longest < 0 else len(nums) - longest


class RemovedSidesSolution:
    """Approach: Removed-prefix map and suffix enumeration
    Time: O(n) expected
    Space: O(n)
    """

    def minOperations(self, nums: list[int], x: int) -> int:
        prefix = {0: 0}
        total = 0
        for count, value in enumerate(nums, 1):
            total += value
            prefix[total] = count
        best = len(nums) + 1
        suffix = 0
        for right_count in range(len(nums) + 1):
            left_count = prefix.get(x - suffix)
            if left_count is not None and left_count + right_count <= len(nums):
                best = min(best, left_count + right_count)
            if right_count < len(nums):
                suffix += nums[len(nums) - 1 - right_count]
        return -1 if best > len(nums) else best
