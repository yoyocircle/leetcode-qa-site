"""
## Task

Return the minimum in a rotated nondecreasing array that may contain duplicate values.

## Hints

1. Compare the midpoint with the rightmost value.
2. A fully sorted interval reveals its minimum immediately.

## Approach

### Right-boundary binary elimination

A larger midpoint places the minimum to its right; a smaller midpoint keeps it in the left half.
On equality, drop one rightmost duplicate.

### Divide and combine with sorted-interval pruning

Return the first value for a strictly ordered endpoint interval. Otherwise recursively split
into two nonempty halves and take their smaller minimum.

## Why it works

### Right-boundary binary elimination

The minimum remains in the retained interval. Equal midpoint and right values mean removing
right cannot remove the only minimum occurrence, since the midpoint has the same value.

### Divide and combine with sorted-interval pruning

Distinct ordered endpoints certify no rotation drop lies inside that interval. Ambiguous
intervals are partitioned completely, so taking the minimum of both exact recursive answers
cannot miss the global minimum.

## Walkthrough

[2,2,2,0,1] has minimum 0. Equal values can force the first approach to remove duplicate
endpoints one by one.

## Cost and pitfalls

Right-boundary binary elimination: O(n) worst; O(log n) without ambiguous ties time; O(1) space.

Divide and combine with sorted-interval pruning: O(n) worst time; O(log n) space.

Inputs are unchanged. The divide variant uses index ranges rather than copied slices, and
balanced splits keep recursion depth logarithmic even for thousands of identical values.
"""


class Solution:
    """Approach: Right-boundary binary elimination
    Time: O(n) worst; O(log n) without ambiguous ties
    Space: O(1)
    """

    def findMin(self, nums: list[int]) -> int:
        low, high = 0, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            if nums[middle] > nums[high]:
                low = middle + 1
            elif nums[middle] < nums[high]:
                high = middle
            else:
                high -= 1
        return nums[low]


class DivideSolution:
    """Approach: Divide and combine with sorted-interval pruning
    Time: O(n) worst
    Space: O(log n)
    """

    def findMin(self, nums: list[int]) -> int:
        def minimum(low, high):
            if low == high or nums[low] < nums[high]:
                return nums[low]
            middle = (low + high) // 2
            return min(minimum(low, middle), minimum(middle + 1, high))

        return minimum(0, len(nums) - 1)
