"""## Task

Return the k most frequent distinct values. Answer order is irrelevant, and
the selected set is guaranteed unique.

## Hints

1. First count each value.
2. Frequencies are bounded by n, so can they be used as array indices?

## Approach

### Frequency buckets

Count with a frequency map. Place each distinct value in a bucket indexed by
its frequency, then scan buckets from high to low until k values are collected.
This avoids sorting all distinct values.

### Size-k frequency heap

Count distinct values, then retain a min-heap of the k strongest (frequency,value) pairs. This
avoids n frequency buckets but does not guarantee the linear follow-up bound when k grows with
n.

## Why it works

### Frequency buckets

Every value appears in exactly its frequency bucket. Descending bucket order
visits values in nonincreasing frequency, so the first k are precisely the most
frequent set. The uniqueness promise removes ambiguity at the cutoff.

### Size-k frequency heap

After each distinct value, the heap contains the k largest frequency pairs seen. The guaranteed
unique cutoff makes tie order irrelevant to the selected set.

## Walkthrough

For [2,2,2,4,4,7] and k=2, buckets 3,2,1 contain [2],[4],[7].
Read buckets 3 and 2 to return [2,4].

## Cost and pitfalls

Default approach costs and behavior:

Expected O(n) time and O(n) auxiliary space, plus O(k) output. Input is unchanged.
This meets the requested better-than-O(n log n) follow-up. Allocate independent
bucket lists with a comprehension, not repeated references to one list. A heap
is an alternative when avoiding n empty buckets matters.

Alternative tradeoff: O(n + u log(k+1)); worst misses linear follow-up time; O(u+k) space.
"""

from collections import Counter
from heapq import heappop, heappush


class Solution:
    """Approach: Frequency buckets
    Time: O(n) expected
    Space: O(n)
    """

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        frequencies = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for number, count in frequencies.items():
            buckets[count].append(number)
        result = []
        for count in range(len(nums), 0, -1):
            for number in buckets[count]:
                result.append(number)
                if len(result) == k:
                    return result
        raise ValueError("k must not exceed the distinct value count")


class FrequencyHeapSolution:
    """Approach: Size-k frequency heap
    Time: O(n + u log(k+1)); worst misses linear follow-up
    Space: O(u+k)
    """

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        heap = []
        for value, count in Counter(nums).items():
            heappush(heap, (count, value))
            if len(heap) > k:
                heappop(heap)
        return [value for _, value in heap]
