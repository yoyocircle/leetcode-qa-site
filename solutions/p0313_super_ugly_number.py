"""## Task

Return the nth positive integer whose prime factors all belong to the supplied distinct prime
list. The sequence begins with 1.

## Hints

1. Merge one sorted product stream per prime.
2. Each stream multiplies an increasing prefix of the generated sequence.

## Approach

### Prime-pointer dynamic programming

Store generated values and one producer index per prime. Append the minimum next product and
advance every producer tied at that value.

### Heap merge of prime product streams

Keep one heap entry per prime stream. Append the heap minimum once, then advance all entries
tied at that minimum. This avoids scanning unrelated producers each round.

## Why it works

### Prime-pointer dynamic programming

Every permitted number except 1 has a smaller permitted predecessor after removing a prime
factor. Producer minima therefore expose the smallest unseen value, and advancing all ties
removes duplicate factorizations.

### Heap merge of prime product streams

Each heap entry is its stream's smallest unreported product. Minimum extraction yields the next
global value, and draining all equal entries prevents repeated output without a separate global
seen set.

## Walkthrough

For primes [2,7] the first six values are 1,2,4,7,8,14, so n=6 returns 14.

## Cost and pitfalls

Prime-pointer dynamic programming: O(n*k) time; O(n+k) space.
Heap merge of prime product streams: O(k+A log(k+1)), A<=n*k stream advances time; O(n+k) space.
Inputs are unchanged. k is prime count and A total producer advances, including ties. The heap
is not guaranteed asymptotically faster in heavily tied cases. Product arithmetic remains
bounded by the official numeric limits.
"""

from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Prime-pointer dynamic programming
    Time: O(n*k)
    Space: O(n+k)
    """

    def nthSuperUglyNumber(self, n: int, primes: list[int]) -> int:
        values = [1]
        positions = [0] * len(primes)
        while len(values) < n:
            candidates = [
                prime * values[index] for prime, index in zip(primes, positions, strict=True)
            ]
            following = min(candidates)
            values.append(following)
            for index, candidate in enumerate(candidates):
                if candidate == following:
                    positions[index] += 1
        return values[-1]


class HeapStreamsSolution:
    """Approach: Heap merge of prime product streams
    Time: O(k+A log(k+1)), A<=n*k stream advances
    Space: O(n+k)
    """

    def nthSuperUglyNumber(self, n: int, primes: list[int]) -> int:
        values = [1]
        heap = [(prime, prime, 0) for prime in primes]
        heapify(heap)
        while len(values) < n:
            following = heap[0][0]
            values.append(following)
            while heap[0][0] == following:
                _, prime, index = heappop(heap)
                index += 1
                heappush(heap, (prime * values[index], prime, index))
        return values[-1]
