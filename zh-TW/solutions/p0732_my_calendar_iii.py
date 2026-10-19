"""
## Task

After each half-open interval booking, return the greatest number of simultaneous accepted
bookings. Every request is accepted.

## Hints

1. A prefix sum of start/end deltas gives active coverage.
2. A dynamically allocated segment tree can avoid sweeping all earlier endpoints.

## Approach

### Endpoint sweep after each insertion

Add start +1 and end -1 events, then sweep sorted coordinates to find the maximum prefix sum.

### Sparse lazy segment tree

Represent integer times 0..10^9-1 in a dictionary-backed segment tree. Add one over
[start,end-1], storing a lazy whole-node addition and child maximum.

## Why it works

### Endpoint sweep after each insertion

The active prefix count on each segment equals the number of intervals covering it. Its largest
value is therefore exactly maximum simultaneous coverage after the insertion.

### Sparse lazy segment tree

A node maximum equals its whole-range lazy count plus the larger child maximum. Range additions
preserve this invariant recursively, so the root always reports global maximum coverage.

## Walkthrough

(10,20),(50,60),(10,40),(5,15),(5,10),(25,55) returns [1,1,2,3,3,3]. End time 10 and start time
10 do not add an overlap.

## Cost and pitfalls

Endpoint sweep after each insertion: O(n log n) per book time; O(n) space.

Sparse lazy segment tree: O(log U) per book time; O(n log U) space.

The object owns state. n is bookings so far and U=10^9 the coordinate universe. Sparse
allocation creates only visited tree nodes; recursion depth is about 30, independent of booking
count.
"""


class MyCalendarThree:
    """Approach: Endpoint sweep after each insertion
    Time: O(n log n) per book
    Space: O(n)
    """

    def __init__(self):
        self.events = {}

    def book(self, startTime: int, endTime: int) -> int:
        self.events[startTime] = self.events.get(startTime, 0) + 1
        self.events[endTime] = self.events.get(endTime, 0) - 1
        active = answer = 0
        for point in sorted(self.events):
            active += self.events[point]
            answer = max(answer, active)
        return answer


class SegmentCalendarThree:
    """Approach: Sparse lazy segment tree
    Time: O(log U) per book
    Space: O(n log U)
    """

    def __init__(self):
        self.maximum = {}
        self.lazy = {}

    def book(self, startTime: int, endTime: int) -> int:
        def add(node, left, right):
            if endTime <= left or right < startTime:
                return
            if startTime <= left and right < endTime:
                self.maximum[node] = self.maximum.get(node, 0) + 1
                self.lazy[node] = self.lazy.get(node, 0) + 1
                return
            middle = (left + right) // 2
            add(node * 2, left, middle)
            add(node * 2 + 1, middle + 1, right)
            self.maximum[node] = self.lazy.get(node, 0) + max(
                self.maximum.get(node * 2, 0), self.maximum.get(node * 2 + 1, 0)
            )

        add(1, 0, 10**9 - 1)
        return self.maximum[1]
