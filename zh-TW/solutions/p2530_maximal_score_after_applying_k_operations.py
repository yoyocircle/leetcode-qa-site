"""## Task

Perform exactly k operations. Each chooses one array value, adds it to the score, and replaces
it with its ceiling after division by three. Return the maximum total score.

## Hints

1. The largest current value offers the greatest available next reward.
2. Equal maximum values can be processed as a batch before any smaller value becomes
   competitive.

## Approach

### Max-heap greedy replacement

Heapify negated values. Repeatedly take the maximum reward and replace that heap root with its
reduced positive integer ceiling.

### Frequency-compressed maximum batches

Count equal values and heapify distinct maxima. Consume up to the maximum's full multiplicity in
one batch, merging its reduced values into their count bucket. At maximum one, every remaining
reward is one.

## Why it works

### Max-heap greedy replacement

Each element offers a decreasing reward sequence under repeated division. Taking the largest
exposed reward is the standard merge of those decreasing sequences, selecting the globally
largest k rewards.

### Frequency-compressed maximum batches

While any copies of maximum v remain, their reward v dominates all other exposed rewards,
including their reduced successors. Batching them therefore makes the same greedy choices while
reducing heap operations.

## Walkthrough

For [9,3] and k=3, take 9, then either 3, then the other 3, totaling 15. Ceiling division maps 4
to 2, not 1.

## Cost and pitfalls

Max-heap greedy replacement: O(n+k log(n+1)) time; O(n) space.
Frequency-compressed maximum batches: O(n+k log(n+1)) worst time; O(n) space.
Inputs are unchanged because both variants own their heaps/counts. Use (value+2)//3 for exact
integer ceiling. The compressed approach helps duplicate-heavy inputs but has the same
worst-case bound when all maxima are distinct.
"""

from collections import Counter
from heapq import heapify, heappop, heappush, heapreplace


class Solution:
    """Approach: Max-heap greedy replacement
    Time: O(n+k log(n+1))
    Space: O(n)
    """

    def maxKelements(self, nums: list[int], k: int) -> int:
        heap = [-value for value in nums]
        heapify(heap)
        score = 0
        for _ in range(k):
            value = -heap[0]
            score += value
            heapreplace(heap, -((value + 2) // 3))
        return score


class CountedHeapSolution:
    """Approach: Frequency-compressed maximum batches
    Time: O(n+k log(n+1)) worst
    Space: O(n)
    """

    def maxKelements(self, nums: list[int], k: int) -> int:
        counts = Counter(nums)
        heap = [-value for value in counts]
        heapify(heap)
        score = 0
        while k:
            value = -heappop(heap)
            multiplicity = counts.pop(value)
            if value == 1:
                return score + k
            taken = min(k, multiplicity)
            score += taken * value
            k -= taken
            if taken < multiplicity:
                counts[value] = multiplicity - taken
                heappush(heap, -value)
            reduced = (value + 2) // 3
            if reduced not in counts:
                counts[reduced] = 0
                heappush(heap, -reduced)
            counts[reduced] += taken
        return score
