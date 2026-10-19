"""
## Task

Remove as few intervals as possible so the remaining intervals do not overlap.
Intervals that only touch at an endpoint are compatible.

## Hints

1. Minimizing removals is the same as maximizing how many intervals you keep.
2. Which next interval leaves the most room for future choices?

## Approach

### Keep earliest finishing intervals

Sort by ending position. Greedily keep an interval if its start is at least the
last kept end. Subtract the number kept from the input count.

### Start-order overlap replacement

Sort by start. When intervals overlap, remove one and retain the smaller end; otherwise advance
the kept end.

## Why it works

### Keep earliest finishing intervals

Among available compatible intervals, the earliest-finishing one leaves at least
as much room as any other choice. Replacing an optimal solution's first choice
with this one cannot reduce how many later intervals fit. Apply that exchange
argument repeatedly.

### Start-order overlap replacement

Among overlapping intervals, keeping the earlier end leaves at least as much room for every
future interval. Replacing a later-ending candidate therefore preserves an optimal kept count.

## Walkthrough

For [[1,4],[2,3],[3,5]], keep [2,3] first, then [3,5]. Two intervals
remain, so remove one.

## Cost and pitfalls

Default approach (Keep earliest finishing intervals):

O(n log n) time and O(n) sorting space in this Python implementation. Inputs are
unchanged. Compare start>=end so touching intervals are allowed. Sorting by start
and always keeping the first interval can retain a long interval that blocks
several short ones.

Keep earliest finishing intervals: O(n log n) time; O(n) space.
Start-order overlap replacement: O(n log n) time; O(n) space. Sort by start. When intervals
overlap, remove one and retain the smaller end; otherwise advance the kept end.
"""


class Solution:
    """Approach: Keep earliest finishing intervals
    Time: O(n log n)
    Space: O(n)
    """

    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        end = float("-inf")
        kept = 0
        for start, finish in sorted(intervals, key=lambda interval: interval[1]):
            if start >= end:
                kept += 1
                end = finish
        return len(intervals) - kept


class StartOrderSolution:
    """Approach: Start-order overlap replacement
    Time: O(n log n)
    Space: O(n)
    """

    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        end = float("-inf")
        removed = 0
        for start, finish in sorted(intervals):
            if start < end:
                removed += 1
                end = min(end, finish)
            else:
                end = finish
        return removed
