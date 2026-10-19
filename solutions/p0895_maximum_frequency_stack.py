"""## Task

Support push and pop on a frequency stack. Pop removes a value with greatest current frequency,
breaking ties by most recent remaining push.

## Hints

1. Every push has both a frequency level and a timestamp.
2. Store most-recent pushes within each frequency level.

## Approach

### Frequency-level stacks

Count each value, append it to a stack for its new frequency, and track the maximum frequency.
Pop the latest value from that level, then reduce its count.

### Occurrence-priority heap

Push (-frequency,-timestamp,value) for every occurrence. Pop the minimum heap entry and
decrement that value's current count.

## Why it works

### Frequency-level stacks

Each remaining value has one historical push entry at every frequency through its current count.
The maximum level contains exactly highest-frequency candidates, ordered by the tie-breaking
push recency.

### Occurrence-priority heap

For each value the highest remaining occurrence level equals its current frequency. Ranking all
live occurrence entries by level then recency therefore selects the same required maximum and
tie winner.

## Walkthrough

Push 5,7,5,7,4,5. Pops yield 5,7,5,4: first highest count, then latest push among equal counts.

## Cost and pitfalls

Frequency-level stacks: O(1) expected per operation time; O(n) space.
Occurrence-priority heap: O(log(n+1)) per operation time; O(n) space.
Objects own state. Pop is called only when nonempty. n is the peak number of live pushes.
Zero-count values and empty frequency buckets can be removed. The heap alternative retains
per-occurrence metadata and does not achieve constant-time operations.
"""

from heapq import heappop, heappush


class FreqStack:
    """Approach: Frequency-level stacks
    Time: O(1) expected per operation
    Space: O(n)
    """

    def __init__(self):
        self.counts = {}
        self.levels = {}
        self.maximum = 0

    def push(self, val: int) -> None:
        frequency = self.counts.get(val, 0) + 1
        self.counts[val] = frequency
        self.levels.setdefault(frequency, []).append(val)
        self.maximum = max(self.maximum, frequency)

    def pop(self) -> int:
        value = self.levels[self.maximum].pop()
        self.counts[value] -= 1
        if self.counts[value] == 0:
            del self.counts[value]
        if not self.levels[self.maximum]:
            del self.levels[self.maximum]
            self.maximum -= 1
        return value


class HeapFreqStack:
    """Approach: Occurrence-priority heap
    Time: O(log(n+1)) per operation
    Space: O(n)
    """

    def __init__(self):
        self.counts = {}
        self.heap = []
        self.clock = 0

    def push(self, val: int) -> None:
        frequency = self.counts.get(val, 0) + 1
        self.counts[val] = frequency
        heappush(self.heap, (-frequency, -self.clock, val))
        self.clock += 1

    def pop(self) -> int:
        _, _, value = heappop(self.heap)
        self.counts[value] -= 1
        if self.counts[value] == 0:
            del self.counts[value]
        return value
