"""
## Task

Accept half-open bookings unless they create a time covered by at least three accepted
intervals. Double booking is allowed; rejected requests must not change accepted coverage.

## Hints

1. A new booking is invalid if it intersects an existing double-booked segment.
2. A sweep-line count can instead test a tentative update and roll it back on failure.

## Approach

### Store bookings and double intersections

Reject any overlap with an existing double-covered segment. Otherwise record intersections with
all prior bookings as new double-covered segments, then append the booking.

### Sweep event counts with rollback

Tentatively increment the start event and decrement the end event, sweep sorted coordinates, and
reverse those two changes if active coverage reaches three.

## Why it works

### Store bookings and double intersections

Triple coverage exists exactly when the new interval intersects a point already covered twice.
Once that test passes, every new intersection with one old booking is safely a double-covered
segment.

### Sweep event counts with rollback

Prefix sums of endpoint deltas equal coverage on each half-open segment. A sweep maximum above
two is exactly a forbidden triple overlap; rollback restores the prior valid event map.

## Walkthrough

Bookings (10,20),(50,60),(10,40) succeed. (5,15) fails because [10,15) would be triple covered.
A later (5,10) still succeeds.

## Cost and pitfalls

Store bookings and double intersections: O(n squared) worst case per book time; O(n squared)
space.

Sweep event counts with rollback: O(n log n) per book time; O(n) space.

Both objects own their state. Endpoint deltas at the same coordinate combine before measuring
coverage. The conservative intersection-list bound allows quadratic storage; the sweep
representation stores only endpoints.
"""


class MyCalendarTwo:
    """Approach: Store bookings and double intersections
    Time: O(n squared) worst case per book
    Space: O(n squared)
    """

    def __init__(self):
        self.bookings = []
        self.doubles = []

    def book(self, startTime: int, endTime: int) -> bool:
        if any(max(start, startTime) < min(end, endTime) for start, end in self.doubles):
            return False
        for start, end in self.bookings:
            left, right = max(start, startTime), min(end, endTime)
            if left < right:
                self.doubles.append((left, right))
        self.bookings.append((startTime, endTime))
        return True


class SweepCalendarTwo:
    """Approach: Sweep event counts with rollback
    Time: O(n log n) per book
    Space: O(n)
    """

    def __init__(self):
        self.events = {}

    def book(self, startTime: int, endTime: int) -> bool:
        self.events[startTime] = self.events.get(startTime, 0) + 1
        self.events[endTime] = self.events.get(endTime, 0) - 1
        active = 0
        for point in sorted(self.events):
            active += self.events[point]
            if active > 2:
                self.events[startTime] -= 1
                self.events[endTime] += 1
                if self.events[startTime] == 0:
                    del self.events[startTime]
                if self.events.get(endTime) == 0:
                    del self.events[endTime]
                return False
        return True
