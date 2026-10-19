"""## Task

Maintain a growing integer stream and return its median after insertions.
A median query is made only after at least one number has been added.

## Hints

1. Only the boundary between the lower and upper halves determines the median.
2. Keep the lower half's maximum and upper half's minimum directly accessible.

## Approach

### Two balanced heaps

Store the lower half in a max-heap via negation and the upper half in a min-heap.
Insert into lower, move its maximum to upper, then rebalance so lower has the
same size as upper or exactly one more element.

### Sorted stream array

Keep all inserted values in a sorted Python list using bisect.insort. Read one or two middle
entries for the median. Binary search locates insertion quickly, but shifting list references
still takes linear time.

## Why it works

### Two balanced heaps

Moving lower's largest value to upper preserves the partition order: every lower
value is no greater than any upper value. Rebalancing preserves this order and
the size invariant. The median is therefore lower's top or the average of both tops.

### Sorted stream array

Insertion preserves sorted order and multiplicity. The central rank of an odd-length sorted
list, or the mean of its two central ranks for even length, is the median by definition.

## Walkthrough

Add 4, 1, 7 in sequence. The medians are 4, 2.5, and 4. After all three,
the lower half holds [1,4], while the upper half holds [7].

## Cost and pitfalls

Default approach costs and behavior:

Insertion is O(log n), median lookup O(1), and storage O(n). The object owns
both heaps. Remember to negate the lower root when reading it. Equal values
may occupy both heaps; strict partition separation is unnecessary.

Alternative tradeoff: O(n) add; O(1) median time; O(n) space.
"""

from bisect import insort
from heapq import heappop, heappush


class MedianFinder:
    """Approach: Two balanced heaps
    Time: O(log n) add; O(1) median
    Space: O(n)
    """

    def __init__(self):
        self.lower = []
        self.upper = []

    def addNum(self, num: int) -> None:
        heappush(self.lower, -num)
        heappush(self.upper, -heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heappush(self.lower, -heappop(self.upper))

    def findMedian(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2


class SortedMedianFinder:
    """Approach: Sorted stream array
    Time: O(n) add; O(1) median
    Space: O(n)
    """

    def __init__(self):
        self.values = []

    def addNum(self, num: int) -> None:
        insort(self.values, num)

    def findMedian(self) -> float:
        middle = len(self.values) // 2
        if len(self.values) % 2:
            return float(self.values[middle])
        return (self.values[middle - 1] + self.values[middle]) / 2
