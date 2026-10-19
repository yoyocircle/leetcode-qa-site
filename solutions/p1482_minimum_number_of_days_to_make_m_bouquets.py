"""
## Task

Each flower blooms on its given day. Return the minimum day when m disjoint bouquets of k
adjacent flowers can be made, or -1 if too few flowers exist.

## Hints

1. A candidate day lets a greedy scan count complete adjacent bouquets.
2. Activating flowers by bloom day lets union-find maintain lengths of consecutive bloomed runs.

## Approach

### Binary search day with consecutive-run counting

Reject m*k>n. For a candidate day, scan bloomed runs and consume every k consecutive flowers as
one bouquet.

### Bloom-order union-find run capacities

Sort flower activations by day. Each active component is one consecutive run; maintain the sum
of floor(component_size/k) while merging active neighbors.

## Why it works

### Binary search day with consecutive-run counting

A run of length L supports exactly floor(L/k) disjoint bouquets. The greedy scan attains that
count, and later days only activate more flowers, so the feasibility predicate is monotone.

### Bloom-order union-find run capacities

Activating a flower creates a singleton run and merging adjacent runs updates exactly their
combined bouquet capacity. The maintained total therefore equals feasible bouquet count after
those activations; the first day reaching m is minimal.

## Walkthrough

[1,10,3,10,2], m=3, k=1 first succeeds on day 3. The same flowers with m=3, k=2 are impossible
because six flowers would be required.

## Cost and pitfalls

Binary search day with consecutive-run counting: O(n log(D+1)) time; O(1) space.

Bloom-order union-find run capacities: O(n log n) time; O(n) space.

Inputs are unchanged. D is max(bloomDay)-min(bloomDay). Equal-day activations may be processed
separately: once enough bouquets exist during that day, the full day is also feasible.
"""


class Solution:
    """Approach: Binary search day with consecutive-run counting
    Time: O(n log(D+1))
    Space: O(1)
    """

    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        if m * k > len(bloomDay):
            return -1
        low, high = min(bloomDay), max(bloomDay)
        while low < high:
            day = (low + high) // 2
            bouquets = run = 0
            for bloom in bloomDay:
                if bloom <= day:
                    run += 1
                    if run == k:
                        bouquets += 1
                        run = 0
                else:
                    run = 0
            if bouquets >= m:
                high = day
            else:
                low = day + 1
        return low


class UnionFindSolution:
    """Approach: Bloom-order union-find run capacities
    Time: O(n log n)
    Space: O(n)
    """

    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        size = len(bloomDay)
        if m * k > size:
            return -1
        parent = list(range(size))
        lengths = [1] * size
        active = [False] * size
        bouquets = 0

        def find(index):
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        for day, index in sorted((day, index) for index, day in enumerate(bloomDay)):
            active[index] = True
            bouquets += 1 // k
            for neighbor in (index - 1, index + 1):
                if not (0 <= neighbor < size and active[neighbor]):
                    continue
                first, second = find(index), find(neighbor)
                if first == second:
                    continue
                bouquets -= lengths[first] // k + lengths[second] // k
                if lengths[first] < lengths[second]:
                    first, second = second, first
                parent[second] = first
                lengths[first] += lengths[second]
                bouquets += lengths[first] // k
            if bouquets >= m:
                return day
        return -1
