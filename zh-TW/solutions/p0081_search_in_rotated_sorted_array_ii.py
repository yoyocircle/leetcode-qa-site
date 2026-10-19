"""
## Task

Decide whether target occurs in a nondecreasing array rotated at an unknown position. Duplicate
values are allowed.

## Hints

1. Equal endpoints can hide which side is sorted.
2. Adjacent equal runs can be compressed before searching a strictly ordered rotation.

## Approach

### Duplicate-aware sorted-half search

Use binary search when one half is distinguishably sorted. When left, middle, and right values
match, discard the equal endpoints after checking the midpoint.

### Run compression then rotated binary search

Copy one value per adjacent equal run. If the first and last runs represent the same value,
remove the final copy, then search the distinct rotated sequence.

## Why it works

### Duplicate-aware sorted-half search

Sorted-half comparisons discard only values outside the target interval. In an ambiguous equal-
endpoint case the endpoints equal the already-checked non-target midpoint, so removing them
cannot lose a match.

### Run compression then rotated binary search

Compression removes only duplicate occurrences, preserving membership. Removing a duplicated
wraparound endpoint leaves a rotation of strictly increasing distinct values, where one half is
always sorted.

## Walkthrough

[2,5,6,0,0,1,2] contains 0 but not 3. Compression produces [2,5,6,0,1] after removing the
repeated wraparound 2.

## Cost and pitfalls

Duplicate-aware sorted-half search: O(n) worst; O(log n) with informative splits time; O(1)
space.

Run compression then rotated binary search: O(n) time; O(n) space.

Inputs are unchanged. Duplicates make logarithmic worst-case time impossible: an array of equal
values can conceal one distinct target anywhere. Compression exchanges extra storage for
deterministic preprocessing.
"""


class Solution:
    """Approach: Duplicate-aware sorted-half search
    Time: O(n) worst; O(log n) with informative splits
    Space: O(1)
    """

    def search(self, nums: list[int], target: int) -> bool:
        low, high = 0, len(nums) - 1
        while low <= high:
            middle = (low + high) // 2
            if nums[middle] == target:
                return True
            if nums[low] == nums[middle] == nums[high]:
                low += 1
                high -= 1
            elif nums[low] <= nums[middle]:
                if nums[low] <= target < nums[middle]:
                    high = middle - 1
                else:
                    low = middle + 1
            elif nums[middle] < target <= nums[high]:
                low = middle + 1
            else:
                high = middle - 1
        return False


class RunCompressionSolution:
    """Approach: Run compression then rotated binary search
    Time: O(n)
    Space: O(n)
    """

    def search(self, nums: list[int], target: int) -> bool:
        values = []
        for value in nums:
            if not values or value != values[-1]:
                values.append(value)
        if len(values) > 1 and values[0] == values[-1]:
            values.pop()
        low, high = 0, len(values) - 1
        while low <= high:
            middle = (low + high) // 2
            if values[middle] == target:
                return True
            if values[low] <= values[middle]:
                if values[low] <= target < values[middle]:
                    high = middle - 1
                else:
                    low = middle + 1
            elif values[middle] < target <= values[high]:
                low = middle + 1
            else:
                high = middle - 1
        return False
