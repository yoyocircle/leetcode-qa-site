"""
## Task

Return the k closest elements to x from a sorted array, in ascending order. Prefer the smaller
value when distances tie.

## Hints

1. The chosen values form a consecutive length-k window.
2. Compare the two values that compete when moving a candidate window one position right.

## Approach

### Binary search the chosen window start

Search possible starts from 0 to n-k. Compare x-arr[mid] with arr[mid+k]-x to decide whether the
left edge should be replaced by the competing right value.

### Discard the farther endpoint

Keep a surviving interval and discard its farther endpoint until exactly k values remain. On
ties discard the larger right endpoint.

## Why it works

### Binary search the chosen window start

The edge-distance comparison changes monotonically with the start. If the left edge is strictly
farther, moving right improves the window; otherwise keeping the earlier window preserves the
smaller-value tie rule.

### Discard the farther endpoint

In sorted order, a farthest remaining value always lies at an endpoint. Removing the worse
endpoint cannot remove a preferred top-k value; repeated removal leaves exactly the required
multiset in sorted order.

## Walkthrough

[1,2,3,4,5], k=4, x=3 discards 5 on the distance tie with 1, leaving [1,2,3,4].

## Cost and pitfalls

Binary search the chosen window start: O(log(n-k+1)+k) time; O(k) output; O(1) auxiliary space.

Discard the farther endpoint: O(n) time; O(k) output; O(1) auxiliary space.

Inputs are unchanged; the returned slice is a fresh list. Include O(k) copying time in the
binary-search variant, and keep the output sorted rather than sorting by distance.
"""


class Solution:
    """Approach: Binary search the chosen window start
    Time: O(log(n-k+1)+k)
    Space: O(k) output; O(1) auxiliary
    """

    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        low, high = 0, len(arr) - k
        while low < high:
            middle = (low + high) // 2
            if x - arr[middle] > arr[middle + k] - x:
                low = middle + 1
            else:
                high = middle
        return arr[low : low + k]


class ShrinkingSolution:
    """Approach: Discard the farther endpoint
    Time: O(n)
    Space: O(k) output; O(1) auxiliary
    """

    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        left, right = 0, len(arr) - 1
        while right - left + 1 > k:
            if abs(arr[left] - x) > abs(arr[right] - x):
                left += 1
            else:
                right -= 1
        return arr[left : right + 1]
