"""
## Task

Schedule unit-time tasks with at least n idle slots between two executions of the same letter.
Return the minimum total time, allowing idle intervals.

## Hints

1. The largest frequency imposes blocks separated by cooldowns.
2. A heap can construct an optimal schedule without iterating over long idle gaps.

## Approach

### Frequency packing bound

Let f be the maximum frequency and c the number of task types achieving it. Return the larger of
task count and (f-1)(n+1)+c.

### Available-task heap with cooldown queue

Choose the most frequent available task, then put it in a time-ordered cooldown queue. Jump
directly to the next release time if no task is available.

## Why it works

### Frequency packing bound

The f copies of a most frequent task require f-1 separated blocks; the c final tied tasks occupy
the last block tail. Other tasks fill idle slots, and if they overflow the bound, all task slots
can be packed without idles.

### Available-task heap with cooldown queue

Scheduling a more frequent available type first leaves the most room for its remaining copies;
exchanging it with a less frequent available type cannot increase idle demand. The queue
enforces each exact cooldown release.

## Walkthrough

[A,A,A,B,B,B], n=2 fits A,B,idle,A,B,idle,A,B, requiring eight intervals; the packing bound is
(3-1)*3+2=8.

## Cost and pitfalls

Frequency packing bound: O(T+A) time; O(A) space.

Available-task heap with cooldown queue: O(T log A) time; O(A) space.

Inputs are unchanged. T is task count and A at most 26 distinct task types. A cooldown of zero
needs exactly T intervals.
"""

from collections import Counter, deque
from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Frequency packing bound
    Time: O(T+A)
    Space: O(A)
    """

    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        frequency = max(counts.values())
        tied = sum(count == frequency for count in counts.values())
        return max(len(tasks), (frequency - 1) * (n + 1) + tied)


class HeapSolution:
    """Approach: Available-task heap with cooldown queue
    Time: O(T log A)
    Space: O(A)
    """

    def leastInterval(self, tasks: list[str], n: int) -> int:
        heap = [-count for count in Counter(tasks).values()]
        heapify(heap)
        cooling = deque()
        time = 0
        while heap or cooling:
            if not heap:
                time = max(time, cooling[0][0])
            while cooling and cooling[0][0] <= time:
                _, count = cooling.popleft()
                heappush(heap, count)
            count = heappop(heap) + 1
            time += 1
            if count:
                cooling.append((time + n, count))
        return time
