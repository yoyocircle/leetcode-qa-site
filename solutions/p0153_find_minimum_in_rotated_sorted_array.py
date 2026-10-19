"""
## Task

Find the smallest value in a rotated ascending array of distinct values.
An array with no visible rotation is also valid.

## Hints

1. Compare the middle value with the current rightmost value.
2. Can the middle itself still be the minimum when it is smaller?

## Approach

### Compare with right boundary

Maintain an interval that contains the minimum. If middle exceeds right, the
rotation boundary lies strictly after middle. Otherwise the minimum is at middle
or to its left. Stop when only one candidate remains.

### Search relative to first value

Return the first element immediately for an unrotated array. Otherwise binary-search the first
value smaller than the original first value.

## Why it works

### Compare with right boundary

A larger middle than right proves a descending wrap occurs in the right half.
A smaller middle than right means that right segment is sorted, so its interior
cannot improve on middle. Each update preserves the minimum and shortens the interval.

### Search relative to first value

In a rotated distinct array, values at least the first value form the first sorted run and
smaller values form the second. The first index in the second run is exactly the minimum.

## Walkthrough

For [4, 7, 9, 1, 2], middle 9 exceeds right 2, so left becomes index 3.
Next middle 1 is below 2, so right becomes 3. Return 1.

## Cost and pitfalls

Default approach (Compare with right boundary):

O(log n) time and O(1) space; input is unchanged. Use right=middle, not
middle-1, because middle may be the answer. Compare against the current right
boundary. Duplicate values are excluded by this problem's contract.

Compare with right boundary: O(log n) time; O(1) space.
Search relative to first value: O(log n) time; O(1) space. Return the first element immediately
for an unrotated array. Otherwise binary-search the first value smaller than the original first
value.
"""


class Solution:
    """Approach: Compare with right boundary
    Time: O(log n)
    Space: O(1)
    """

    def findMin(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            middle = (left + right) // 2
            if nums[middle] > nums[right]:
                left = middle + 1
            else:
                right = middle
        return nums[left]


class FirstValueSolution:
    """Approach: Search relative to first value
    Time: O(log n)
    Space: O(1)
    """

    def findMin(self, nums: list[int]) -> int:
        if nums[0] <= nums[-1]:
            return nums[0]
        low, high = 1, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            if nums[middle] >= nums[0]:
                low = middle + 1
            else:
                high = middle
        return nums[low]
