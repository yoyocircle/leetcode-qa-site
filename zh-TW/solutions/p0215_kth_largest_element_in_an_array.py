"""## Task

Return the kth largest array element, counting repeated values separately.
The requested k lies between 1 and the array length.

## Hints

1. You only need to retain the k largest values seen so far.
2. A min-heap exposes the weakest member of those k candidates.

## Approach

### Size-k min-heap

Heapify the first k values. For each later value, replace the heap root only
when the new value is larger. The final root is the kth largest.

### Randomized three-way quickselect

Partition a copied array around a random pivot into smaller, equal, and larger regions. Continue
only in the region containing ascending rank n-k. Three-way partitioning handles many duplicates
without repeatedly selecting them.

### Bounded-domain counting

Count values in the official -10000..10000 domain, then scan frequencies from
largest to smallest until k occurrences are consumed. This replaces comparison
selection with fixed-domain direct addressing.

## Why it works

### Size-k min-heap

Inductively, the heap contains the k largest values in the processed prefix.
A value no larger than its minimum cannot enter that set. A larger value must
replace that minimum. The invariant makes the root the desired rank at the end.

### Randomized three-way quickselect

Partition places every smaller value before every equal value and every larger value after. The
target rank either lies in the equal band or remains unchanged inside exactly one retained
interval.

### Bounded-domain counting

Descending counts describe all values in nonincreasing multiset order. The
bucket containing the kth occurrence therefore contains the required answer.

## Walkthrough

For [5,1,5,3] and k=2, the initial heap contains 1 and 5. The next 5
replaces 1, and 3 cannot replace either 5. Return 5.

## Cost and pitfalls

Default approach costs and behavior:

O(n log(k+1)) time and O(k) auxiliary space. Input is unchanged, and the scan
avoids copying the remaining suffix. Duplicates count toward rank; converting
to a set changes the problem. Sorting is simpler but costs O(n log n);
randomized quickselect offers expected linear time with a different tradeoff.

Alternative tradeoff: O(n) expected; O(n^2) worst time; O(n) copied array space.

Counting-domain costs: O(n+U) time and O(U) space for U=20001. Input is unchanged.
"""

from heapq import heapify, heapreplace
from random import randrange


class Solution:
    """Approach: Size-k min-heap
    Time: O(n log(k+1))
    Space: O(k)
    """

    def findKthLargest(self, nums: list[int], k: int) -> int:
        heap = nums[:k]
        heapify(heap)
        for i in range(k, len(nums)):
            if nums[i] > heap[0]:
                heapreplace(heap, nums[i])
        return heap[0]


class QuickselectSolution:
    """Approach: Randomized three-way quickselect
    Time: O(n) expected; O(n^2) worst
    Space: O(n) copied array
    """

    def findKthLargest(self, nums: list[int], k: int) -> int:
        values = nums.copy()
        target = len(values) - k
        low, high = 0, len(values) - 1
        while True:
            pivot = values[randrange(low, high + 1)]
            smaller, scan, larger = low, low, high
            while scan <= larger:
                if values[scan] < pivot:
                    values[smaller], values[scan] = values[scan], values[smaller]
                    smaller += 1
                    scan += 1
                elif values[scan] > pivot:
                    values[scan], values[larger] = values[larger], values[scan]
                    larger -= 1
                else:
                    scan += 1
            if target < smaller:
                high = smaller - 1
            elif target > larger:
                low = larger + 1
            else:
                return pivot


class CountingDomainSolution:
    """Approach: Bounded-domain counting
    Time: O(n+U), U=20001
    Space: O(U)
    """

    def findKthLargest(self, nums: list[int], k: int) -> int:
        counts = [0] * 20001
        for value in nums:
            counts[value + 10000] += 1
        for index in range(20000, -1, -1):
            k -= counts[index]
            if k <= 0:
                return index - 10000
        raise AssertionError("k is valid under the problem contract")
