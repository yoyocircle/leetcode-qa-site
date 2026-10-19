"""
## Task

Return any index whose value exceeds its neighbors. Adjacent values differ and positions beyond
the array are negative infinity. Required time is logarithmic.

## Hints

1. An uphill slope guarantees a peak somewhere to the right.
2. An endpoint is a valid peak if its single real neighbor is smaller.

## Approach

### Binary search on slope

Compare the midpoint with its right neighbor. Keep the uphill side, including the midpoint on a
downward slope.

### First descending edge

Walk along the initial increasing run and return its final index. This educational baseline
misses the required logarithmic-time bound.

## Why it works

### Binary search on slope

An increasing slope must eventually reach a peak before the right negative-infinity boundary;
the symmetric downward argument guarantees a peak in the retained left half.

### First descending edge

The run endpoint is larger than its left neighbor, if any. It is either the last index or
followed by a smaller value, so both peak inequalities hold.

## Walkthrough

[1,2,1,3,5,6,4] permits index 1 or 5. Tests must validate the returned peak rather than require
one particular index.

## Cost and pitfalls

Binary search on slope: O(log n) time; O(1) space.

First descending edge: O(n) time; O(1) space.

Inputs are unchanged. The problem does not promise a single mountain, so a global maximum search
is unnecessary.
"""


class Solution:
    """Approach: Binary search on slope
    Time: O(log n)
    Space: O(1)
    """

    def findPeakElement(self, nums: list[int]) -> int:
        low, high = 0, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            if nums[middle] < nums[middle + 1]:
                low = middle + 1
            else:
                high = middle
        return low


class ScanSolution:
    """Approach: First descending edge
    Time: O(n)
    Space: O(1)
    """

    def findPeakElement(self, nums: list[int]) -> int:
        index = 0
        while index + 1 < len(nums) and nums[index] < nums[index + 1]:
            index += 1
        return index
