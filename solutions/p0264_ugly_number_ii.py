"""## Task

Return the nth positive number whose only prime factors are 2, 3, and 5. The sequence starts
with 1.

## Hints

1. Every later number is an earlier one multiplied by 2, 3, or 5.
2. When several products tie, advance every pointer producing that value.

## Approach

### Three monotone product pointers

Store generated values and three indices. Append the smallest next multiple; advance each
matching index to suppress duplicates such as 2*3 and 3*2.

### Heap with duplicate set

Start a min-heap at one. Repeatedly remove its minimum and insert unseen products by 2, 3, and 5
into a heap and membership set.

## Why it works

### Three monotone product pointers

Each pointer identifies its factor's smallest product beyond the generated prefix. Their minimum
is therefore the smallest unseen valid number, and advancing all ties prevents duplicates.

### Heap with duplicate set

Multiplication generates only valid numbers, and every valid number except one has a smaller
valid predecessor by removing a prime factor. Minimum extraction therefore enumerates them in
ascending order.

## Walkthrough

The first six values are 1,2,3,4,5,6, so n=6 returns 6. At 6 both factor-2 and factor-3
producers advance.

## Cost and pitfalls

Three monotone product pointers: O(n) time; O(n) space.
Heap with duplicate set: O(n log n) time; O(n) space.
Inputs are scalars and remain unchanged. Include 1 even though it has no prime factors. The heap
uses more bookkeeping than the pointer method; its seen set must track values before enqueueing.
"""

from heapq import heappop, heappush


class Solution:
    """Approach: Three monotone product pointers
    Time: O(n)
    Space: O(n)
    """

    def nthUglyNumber(self, n: int) -> int:
        values = [1]
        pointers = [0, 0, 0]
        factors = (2, 3, 5)
        while len(values) < n:
            candidates = [
                factor * values[index] for factor, index in zip(factors, pointers, strict=True)
            ]
            following = min(candidates)
            values.append(following)
            for index, candidate in enumerate(candidates):
                if candidate == following:
                    pointers[index] += 1
        return values[-1]


class HeapSolution:
    """Approach: Heap with duplicate set
    Time: O(n log n)
    Space: O(n)
    """

    def nthUglyNumber(self, n: int) -> int:
        heap, seen = [1], {1}
        for _ in range(n):
            value = heappop(heap)
            for factor in (2, 3, 5):
                following = value * factor
                if following not in seen:
                    seen.add(following)
                    heappush(heap, following)
        return value
