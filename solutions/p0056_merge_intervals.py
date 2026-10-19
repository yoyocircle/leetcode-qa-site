"""
## Task

Replace overlapping closed intervals with their union, returning disjoint
intervals that cover the same positions. Touching endpoints count as overlap.

## Hints

1. Sort by starting position so only the most recent merged interval matters.
2. The merged end must be the greater end, not necessarily the incoming end.

## Approach

### Sort intervals by start

Sort intervals by start. Append a new output interval when it begins after the
previous merged end. Otherwise extend that end if needed. Create new output
lists so no caller-owned interval is changed.

### Sweep endpoint events

Sort start and end events with starts before ends at equal coordinates. Start an output interval
when active coverage becomes positive and close it when coverage returns to zero.

## Why it works

### Sort intervals by start

Once a new interval starts beyond the current merged end, all later starts are
also beyond it, so that merged interval is final. Overlapping intervals extend
the same connected covered region; taking the maximum end preserves its full union.

### Sweep endpoint events

The active count is the number of intervals covering the current sweep segment. Maximal
positive-count segments are exactly the merged union; processing starts first merges touching
intervals.

## Walkthrough

For [[5,7],[1,3],[3,6]], sorting gives [1,3], [3,6], [5,7]. The second
touches the first and extends it to [1,6]; the last extends it to [1,7].

## Cost and pitfalls

Default approach (Sort intervals by start):

O(n log n) time and O(n) auxiliary sorting space, plus output. Inputs and their
nested lists are unchanged. A contained interval must not shorten the merged
end. The overlap rule here differs from Non-overlapping Intervals, where touching
intervals can both be kept.

Sort intervals by start: O(n log n) time; O(n) plus output space.
Sweep endpoint events: O(n log n) time; O(n) plus output space. Sort start and end events with
starts before ends at equal coordinates. Start an output interval when active coverage becomes
positive and close it when coverage returns to zero.
"""


class Solution:
    """Approach: Sort intervals by start
    Time: O(n log n)
    Space: O(n) plus output
    """

    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        result = []
        for start, end in sorted(intervals):
            if result and start <= result[-1][1]:
                result[-1][1] = max(result[-1][1], end)
            else:
                result.append([start, end])
        return result


class EventSolution:
    """Approach: Sweep endpoint events
    Time: O(n log n)
    Space: O(n) plus output
    """

    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        events = [
            (point, kind) for start, end in intervals for point, kind in ((start, 1), (end, -1))
        ]
        events.sort(key=lambda event: (event[0], -event[1]))
        active = 0
        result = []
        for point, change in events:
            if active == 0:
                start = point
            active += change
            if active == 0:
                result.append([start, point])
        return result
