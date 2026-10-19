"""
## Task

Return the unique peak index in a mountain array: a strictly increasing prefix followed by a
strictly decreasing suffix.

## Hints

1. Use the sign of the midpoint slope.
2. A unimodal function also supports ternary interval elimination.

## Approach

### Binary slope search

If the midpoint rises to its successor, move left past it; otherwise retain the midpoint in the
left side.

### Ternary mountain search

Compare two trisection positions and discard the outside third that cannot contain the peak;
scan the final at-most-three indices.

## Why it works

### Binary slope search

Strict mountain slopes are positive before the peak and negative after it. Each comparison
retains the unique transition point.

### Ternary mountain search

If the left sample is smaller than the right sample, the peak cannot lie at or left of the left
sample. The opposite comparison symmetrically excludes the right side; equal samples retain the
middle interval.

## Walkthrough

[0,2,5,3,1] has its only slope change at index 2, value 5.

## Cost and pitfalls

Binary slope search: O(log n) time; O(1) space.

Ternary mountain search: O(log n) time; O(1) space.

Inputs are unchanged. Ternary search relies on the unique mountain shape and uses more
comparisons than binary slope search.
"""


class Solution:
    """Approach: Binary slope search
    Time: O(log n)
    Space: O(1)
    """

    def peakIndexInMountainArray(self, arr: list[int]) -> int:
        low, high = 0, len(arr) - 1
        while low < high:
            middle = (low + high) // 2
            if arr[middle] < arr[middle + 1]:
                low = middle + 1
            else:
                high = middle
        return low


class TernarySolution:
    """Approach: Ternary mountain search
    Time: O(log n)
    Space: O(1)
    """

    def peakIndexInMountainArray(self, arr: list[int]) -> int:
        low, high = 0, len(arr) - 1
        while high - low > 2:
            left = low + (high - low) // 3
            right = high - (high - low) // 3
            if arr[left] < arr[right]:
                low = left + 1
            elif arr[left] > arr[right]:
                high = right - 1
            else:
                low, high = left + 1, right - 1
        return max(range(low, high + 1), key=arr.__getitem__)
