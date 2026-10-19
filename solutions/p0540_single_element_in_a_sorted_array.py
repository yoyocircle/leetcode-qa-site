"""
## Task

In a sorted array, every value appears exactly twice except one appearing once. Return that
singleton in logarithmic time and constant extra space.

## Hints

1. Before the singleton, pairs start at even indices.
2. Align a midpoint to an even index before comparing the pair.

## Approach

### Even-pair boundary binary search

Compare an even-indexed midpoint with its successor. A complete pair moves the search past it; a
broken pair keeps the left half.

### XOR cancellation baseline

XOR every value so duplicate pairs cancel. This simple independent baseline misses the required
logarithmic-time bound and does not use sorted order.

## Why it works

### Even-pair boundary binary search

Before the singleton, equal pairs occupy even/odd positions. After it, that alignment shifts.
The first broken even pair is therefore the singleton position, and each comparison preserves
that boundary.

### XOR cancellation baseline

XOR is associative and each equal pair contributes zero. The only uncancelled contribution is
the singleton value.

## Walkthrough

[1,1,2,3,3,4,4,8,8] first breaks even pair alignment at index 2, whose value is 2.

## Cost and pitfalls

Even-pair boundary binary search: O(log n) time; O(1) space.

XOR cancellation baseline: O(n) time; O(1) space.

Inputs are unchanged. The array length is odd and at least one. Aligning the midpoint before
reading middle+1 keeps the read inside the current search interval.
"""


class Solution:
    """Approach: Even-pair boundary binary search
    Time: O(log n)
    Space: O(1)
    """

    def singleNonDuplicate(self, nums: list[int]) -> int:
        low, high = 0, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            middle -= middle % 2
            if nums[middle] == nums[middle + 1]:
                low = middle + 2
            else:
                high = middle
        return nums[low]


class XorSolution:
    """Approach: XOR cancellation baseline
    Time: O(n)
    Space: O(1)
    """

    def singleNonDuplicate(self, nums: list[int]) -> int:
        answer = 0
        for value in nums:
            answer ^= value
        return answer
