"""
## Task

Return the first and last indices of target in a sorted array, or [-1,-1] when absent. Required
time is logarithmic.

## Hints

1. Find the first index greater than or equal to target.
2. A second boundary search finds the first index strictly greater.

## Approach

### Two lower-bound searches

Implement lower bound for target and target+1. Check presence before converting the second
insertion position to a last index.

### Directional equality searches

Search for target twice. On equality save the index and continue left for the first search or
right for the second.

## Why it works

### Two lower-bound searches

Lower bound partitions values below the query from values at least the query. The two boundaries
enclose exactly the target run because the array is sorted.

### Directional equality searches

A saved match remains a valid bound while the unresolved half contains every possible more
extreme match. Exhausting that half proves the saved match is the corresponding endpoint.

## Walkthrough

[5,7,7,8,8,10], target 8 has insertion boundaries 3 and 5, giving inclusive range [3,4].

## Cost and pitfalls

Two lower-bound searches: O(log n) time; O(1) space.

Directional equality searches: O(log n) time; O(1) space.

Inputs are unchanged. Empty input returns [-1,-1]. Avoid scanning duplicate runs after finding
one occurrence, which can become linear.
"""


class Solution:
    """Approach: Two lower-bound searches
    Time: O(log n)
    Space: O(1)
    """

    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def lower(value):
            left, right = 0, len(nums)
            while left < right:
                middle = (left + right) // 2
                if nums[middle] < value:
                    left = middle + 1
                else:
                    right = middle
            return left

        start = lower(target)
        if start == len(nums) or nums[start] != target:
            return [-1, -1]
        return [start, lower(target + 1) - 1]


class DirectionalSolution:
    """Approach: Directional equality searches
    Time: O(log n)
    Space: O(1)
    """

    def searchRange(self, nums: list[int], target: int) -> list[int]:
        answer = []
        for first in (True, False):
            low, high, found = 0, len(nums) - 1, -1
            while low <= high:
                middle = (low + high) // 2
                if nums[middle] == target:
                    found = middle
                    if first:
                        high = middle - 1
                    else:
                        low = middle + 1
                elif nums[middle] < target:
                    low = middle + 1
                else:
                    high = middle - 1
            answer.append(found)
        return answer
