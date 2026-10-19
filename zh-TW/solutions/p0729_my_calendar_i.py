"""
## Task

Book half-open intervals [startTime,endTime), rejecting any request that overlaps an accepted
booking. A rejected request must leave the calendar unchanged.

## Hints

1. In sorted order, only neighboring bookings can overlap a new one.
2. For a small bounded booking count, a direct scan is also viable.

## Approach

### Sorted bookings with neighbor checks

Binary-search the new start and check the predecessor end and successor start before inserting.

### Unsorted interval scan

Check intersection against every accepted interval, then append only if all checks pass. This
avoids ordered-list shifts and is suitable for the stated booking limit.

## Why it works

### Sorted bookings with neighbor checks

Accepted bookings are disjoint and sorted. Every earlier interval ends no later than the
predecessor, and every later interval starts no earlier than the successor, so these two checks
are sufficient and necessary.

### Unsorted interval scan

Two half-open intervals overlap exactly when max(starts) < min(ends). Testing every accepted
interval rejects all conflicts and accepts every disjoint request.

## Walkthrough

book(10,20) succeeds, book(15,25) fails, then book(20,30) succeeds because touching half-open
endpoints do not overlap.

## Cost and pitfalls

Sorted bookings with neighbor checks: O(n) per book time; O(n) space.

Unsorted interval scan: O(n) per book time; O(n) space.

The object owns accepted bookings. Sorting lookup is logarithmic, but Python list insertion is
linear, so do not claim O(log n) total booking time.
"""

from bisect import bisect_left


class MyCalendar:
    """Approach: Sorted bookings with neighbor checks
    Time: O(n) per book
    Space: O(n)
    """

    def __init__(self):
        self.bookings = []

    def book(self, startTime: int, endTime: int) -> bool:
        index = bisect_left(self.bookings, (startTime, endTime))
        if index and self.bookings[index - 1][1] > startTime:
            return False
        if index < len(self.bookings) and self.bookings[index][0] < endTime:
            return False
        self.bookings.insert(index, (startTime, endTime))
        return True


class ScanCalendar:
    """Approach: Unsorted interval scan
    Time: O(n) per book
    Space: O(n)
    """

    def __init__(self):
        self.bookings = []

    def book(self, startTime: int, endTime: int) -> bool:
        for start, end in self.bookings:
            if max(start, startTime) < min(end, endTime):
                return False
        self.bookings.append((startTime, endTime))
        return True
