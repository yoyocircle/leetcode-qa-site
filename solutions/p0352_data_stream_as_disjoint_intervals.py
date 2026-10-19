"""
## Task

Accept nonnegative stream values with addNum and return sorted disjoint closed intervals
covering all distinct values with getIntervals.

## Hints

1. A new value can join only its neighboring intervals.
2. Storing just a set makes insertion cheaper but defers sorting to reads.

## Approach

### Sorted interval insertion and neighbor merging

Find the interval insertion point, merge an overlapping or touching predecessor, then merge a
touching successor. Return copied intervals.

### Distinct-value set with read-time compression

Store distinct numbers in a set. Sort them on each read and coalesce consecutive values.

## Why it works

### Sorted interval insertion and neighbor merging

All unaffected intervals stay disjoint and sorted. Only immediate neighbors can touch the new
singleton because gaps separate every other interval; merging them preserves exactly the covered
integer set.

### Distinct-value set with read-time compression

Sorted distinct values split uniquely wherever adjacent numbers differ by more than one. These
maximal runs are exactly the required disjoint intervals.

## Walkthrough

Adding 1,3,7,2,6 gives [[1,3],[6,7]]. Adding 2 again leaves the same coverage.

## Cost and pitfalls

Sorted interval insertion and neighbor merging: O(k) add; O(k) get time; O(k) space.

Distinct-value set with read-time compression: O(1) expected add; O(u log u) get time; O(u)
space.

The object owns its intervals and does not expose mutable internal lists. k is interval count
and u distinct value count; choosing the set approach favors many writes and few reads.
"""

from bisect import bisect_left


class SummaryRanges:
    """Approach: Sorted interval insertion and neighbor merging
    Time: O(k) add; O(k) get
    Space: O(k)
    """

    def __init__(self):
        self.intervals = []

    def addNum(self, value: int) -> None:
        index = bisect_left(self.intervals, [value])
        start = end = value
        if index and self.intervals[index - 1][1] + 1 >= value:
            index -= 1
            start, end = self.intervals.pop(index)
            end = max(end, value)
        while index < len(self.intervals) and self.intervals[index][0] <= end + 1:
            following = self.intervals.pop(index)
            end = max(end, following[1])
        self.intervals.insert(index, [start, end])

    def getIntervals(self) -> list[list[int]]:
        return [interval[:] for interval in self.intervals]


class SetSummaryRanges:
    """Approach: Distinct-value set with read-time compression
    Time: O(1) expected add; O(u log u) get
    Space: O(u)
    """

    def __init__(self):
        self.values = set()

    def addNum(self, value: int) -> None:
        self.values.add(value)

    def getIntervals(self) -> list[list[int]]:
        answer = []
        for value in sorted(self.values):
            if answer and value == answer[-1][1] + 1:
                answer[-1][1] = value
            else:
                answer.append([value, value])
        return answer
