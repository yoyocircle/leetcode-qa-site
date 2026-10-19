"""
## Task

Insert one closed interval into an already sorted, non-overlapping interval list.
Merge any overlaps and retain sorted order.

## Hints

1. The existing order is useful; sorting again is unnecessary.
2. Split the scan into intervals before, overlapping, and after the new interval.

## Approach

### Three-phase interval scan

Copy intervals ending strictly before the new start. Merge every interval whose
start is at most the evolving end. Append the resulting interval, then copy the
remaining suffix. Local start/end variables keep the supplied new interval unchanged.

### Sort and merge all intervals

Add the new interval to a copied sequence, sort it, and run a full union merge. This reuses a
familiar general algorithm at the cost of discarding the sorted-input advantage.

## Why it works

### Three-phase interval scan

Sorted, disjoint input ensures all intervals before the first phase are separate,
all intervals in the second phase connect to the inserted union, and all remaining
intervals start after that union. The three phases therefore form the complete
sorted answer.

### Sort and merge all intervals

Sorted order guarantees no later interval can overlap an already-closed output segment.
Repeatedly extending the current end builds exactly each connected union component.

## Walkthrough

Insert [2,6] into [[1,3],[5,7],[9,10]]. Merge the first two with the new
interval to obtain [1,7], then retain [9,10].

## Cost and pitfalls

Default approach (Three-phase interval scan):

O(n) time and O(1) auxiliary state excluding the O(n) output. Input nested lists
and newInterval are unchanged; returned intervals are fresh lists. Touching
endpoints merge. An empty existing list still returns the inserted interval.

Three-phase interval scan: O(n) time; O(1) auxiliary plus output space.
Sort and merge all intervals: O(n log n) time; O(n) plus output space. Add the new interval to a
copied sequence, sort it, and run a full union merge. This reuses a familiar general algorithm
at the cost of discarding the sorted-input advantage.
"""


class Solution:
    """Approach: Three-phase interval scan
    Time: O(n)
    Space: O(1) auxiliary plus output
    """

    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        start, end = newInterval
        i = 0
        while i < len(intervals) and intervals[i][1] < start:
            result.append(intervals[i][:])
            i += 1
        while i < len(intervals) and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        result.append([start, end])
        while i < len(intervals):
            result.append(intervals[i][:])
            i += 1
        return result


class SortingSolution:
    """Approach: Sort and merge all intervals
    Time: O(n log n)
    Space: O(n) plus output
    """

    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        for start, end in sorted([*intervals, newInterval]):
            if result and start <= result[-1][1]:
                result[-1][1] = max(result[-1][1], end)
            else:
                result.append([start, end])
        return result
