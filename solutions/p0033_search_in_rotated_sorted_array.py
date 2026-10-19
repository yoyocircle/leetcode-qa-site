"""
## Task

Find a target's index in an ascending array that has been rotated. Values are
distinct. Return -1 if absent, in logarithmic time.

## Hints

1. At least one half around the middle is still sorted.
2. Test whether target lies within that half's value range before choosing a side.

## Approach

### Sorted-half binary search

Binary search an inclusive interval. After checking the middle value, identify
the sorted half. Keep it only if its endpoint inequalities contain target;
otherwise search the other half.

### Find pivot then binary search

Locate the minimum element, then binary-search virtual indices in the restored sorted order. Map
each virtual index back through the pivot offset.

## Why it works

### Sorted-half binary search

With distinct values and a single rotation boundary, both halves cannot be
unsorted. The sorted half's range precisely tells whether target could occur
there. Each step keeps every possible target position and halves the search space.

### Find pivot then binary search

The pivot separates the two increasing runs. Rotating virtual indices around it creates the
original strictly sorted sequence, so ordinary binary search retains its ordering invariant.

## Walkthrough

For [6, 8, 1, 3, 4] and target 8, the middle is 1 and the right half is
sorted. Target lies outside [1,4], so search left and find index 1.

## Cost and pitfalls

Default approach (Sorted-half binary search):

O(log n) time and O(1) space; input is unchanged. Include the left endpoint when
checking which half is sorted, especially for two-element intervals. These rules
depend on distinct values; duplicate-heavy variants require a different argument.

Sorted-half binary search: O(log n) time; O(1) space.
Find pivot then binary search: O(log n) time; O(1) space. Locate the minimum element, then
binary-search virtual indices in the restored sorted order. Map each virtual index back through
the pivot offset.
"""


class Solution:
    """Approach: Sorted-half binary search
    Time: O(log n)
    Space: O(1)
    """

    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle
            if nums[left] <= nums[middle]:
                if nums[left] <= target < nums[middle]:
                    right = middle - 1
                else:
                    left = middle + 1
            elif nums[middle] < target <= nums[right]:
                left = middle + 1
            else:
                right = middle - 1
        return -1


class PivotSolution:
    """Approach: Find pivot then binary search
    Time: O(log n)
    Space: O(1)
    """

    def search(self, nums: list[int], target: int) -> int:
        low, high = 0, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            if nums[middle] > nums[high]:
                low = middle + 1
            else:
                high = middle
        pivot = low
        low, high = 0, len(nums) - 1
        while low <= high:
            middle = (low + high) // 2
            index = (middle + pivot) % len(nums)
            if nums[index] == target:
                return index
            if nums[index] < target:
                low = middle + 1
            else:
                high = middle - 1
        return -1
