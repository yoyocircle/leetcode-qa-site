"""
## Task

Decide whether two different indices differ by at most indexDiff and their values differ by at
most valueDiff.

## Hints

1. Maintain exactly the previous indexDiff values.
2. Buckets of width valueDiff+1 localize near-value candidates.

## Approach

### Sliding value buckets

Map each value to a width-(valueDiff+1) bucket. A match can only be in its own bucket or an
adjacent bucket; evict values leaving the index window.

### Sorted sliding-window list

Maintain a sorted list of preceding values. Binary-search the first value at least current-
valueDiff; list insertions and deletions make this a simple educational baseline that may time
out.

## Why it works

### Sliding value buckets

Values in one bucket differ by at most valueDiff. Values in nonadjacent buckets differ by more
than valueDiff. Exact neighbor checks plus timely eviction therefore test precisely the allowed
pairs.

### Sorted sliding-window list

The lower-bound candidate is the smallest prior value that could satisfy the lower difference
bound. It qualifies exactly when it also satisfies the upper bound, and eviction enforces the
index distance.

## Walkthrough

[1,2,3,1], indexDiff=3, valueDiff=0 returns true from the two 1 values. With indexDiff=2 that
pair is outside the live window.

## Cost and pitfalls

Sliding value buckets: O(n) expected time; O(min(n,k)) space.

Sorted sliding-window list: O(n*k) time; O(min(n,k)) space.

Inputs are unchanged. k=indexDiff and valueDiff is nonnegative. Python floor division gives
correct consecutive buckets for negative values too.
"""

from bisect import bisect_left, insort


class Solution:
    """Approach: Sliding value buckets
    Time: O(n) expected
    Space: O(min(n,k))
    """

    def containsNearbyAlmostDuplicate(
        self, nums: list[int], indexDiff: int, valueDiff: int
    ) -> bool:
        buckets = {}
        width = valueDiff + 1
        for i, value in enumerate(nums):
            bucket = value // width
            if bucket in buckets:
                return True
            if bucket - 1 in buckets and value - buckets[bucket - 1] <= valueDiff:
                return True
            if bucket + 1 in buckets and buckets[bucket + 1] - value <= valueDiff:
                return True
            buckets[bucket] = value
            if i >= indexDiff:
                del buckets[nums[i - indexDiff] // width]
        return False


class SortedWindowSolution:
    """Approach: Sorted sliding-window list
    Time: O(n*k)
    Space: O(min(n,k))
    """

    def containsNearbyAlmostDuplicate(
        self, nums: list[int], indexDiff: int, valueDiff: int
    ) -> bool:
        window = []
        for i, value in enumerate(nums):
            position = bisect_left(window, value - valueDiff)
            if position < len(window) and window[position] <= value + valueDiff:
                return True
            insort(window, value)
            if i >= indexDiff:
                window.pop(bisect_left(window, nums[i - indexDiff]))
        return False
