"""
## Task

Return the kth smallest absolute difference among all unordered pairs of distinct indices. Equal
values at different indices form valid distance-zero pairs.

## Hints

1. For a distance bound, count sorted pairs within that distance using two pointers.
2. Distances from each fixed sorted left index form a sorted stream.

## Approach

### Binary search a pair-count threshold

Sort a copy. Binary-search the distance whose count of pairs at most that distance first reaches
k; compute each count with a moving left boundary.

### Heap merge of fixed-left distance streams

For each left index, seed the pair with its immediate successor. Pop the smallest distance and
advance only that stream until k pairs have been removed. This baseline may time out when k is
quadratic in n.

## Why it works

### Binary search a pair-count threshold

For every right index, the valid left indices form one suffix of earlier indices and contribute
right-left pairs. The count is monotone in the bound, so its first count reaching k is the kth
order statistic.

### Heap merge of fixed-left distance streams

Each stream lists all distances sharing one left index in nondecreasing order. A min-heap of
stream heads emits the union in global order, counting every index pair once, so its kth pop is
correct.

## Walkthrough

[1,3,1] has sorted pair distances [0,2,2], so k=1 returns 0. The two equal 1 values belong to
different indices.

## Cost and pitfalls

Binary search a pair-count threshold: O(n log n+n log(W+1)) time; O(n) space.

Heap merge of fixed-left distance streams: O(n log n+k log n) time; O(n) space.

Inputs are unchanged. W is max(nums)-min(nums). Do not deduplicate the array, because
multiplicity determines the pair rank.
"""

from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Binary search a pair-count threshold
    Time: O(n log n+n log(W+1))
    Space: O(n)
    """

    def smallestDistancePair(self, nums: list[int], k: int) -> int:
        values = sorted(nums)
        low, high = 0, values[-1] - values[0]
        while low < high:
            distance = (low + high) // 2
            left = count = 0
            for right, value in enumerate(values):
                while value - values[left] > distance:
                    left += 1
                count += right - left
            if count >= k:
                high = distance
            else:
                low = distance + 1
        return low


class PairHeapSolution:
    """Approach: Heap merge of fixed-left distance streams
    Time: O(n log n+k log n)
    Space: O(n)
    """

    def smallestDistancePair(self, nums: list[int], k: int) -> int:
        values = sorted(nums)
        heap = [(values[i + 1] - values[i], i, i + 1) for i in range(len(values) - 1)]
        heapify(heap)
        for _ in range(k):
            distance, left, right = heappop(heap)
            if right + 1 < len(values):
                heappush(heap, (values[right + 1] - values[left], left, right + 1))
        return distance
