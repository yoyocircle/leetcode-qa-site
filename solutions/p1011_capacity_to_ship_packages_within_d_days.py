"""
## Task

Ship packages in their original order within days days. Return the smallest ship capacity; each
day carries a consecutive block.

## Hints

1. A capacity is feasible if a greedy scan uses at most days trips.
2. Larger capacities never require more trips.

## Approach

### Binary search with greedy loading

Search capacities between the largest package and total weight. Greedily fill each day as far as
possible to test feasibility.

### Partition dynamic programming

Let dp[i] be the least maximum load for the first i packages using at most the current number of
days. Try every possible final-day start. This educational baseline may time out at full
constraints.

## Why it works

### Binary search with greedy loading

For a fixed capacity, any valid first day ends no later than the greedy first day. Induction
shows greedy uses the fewest days. Feasibility is monotone, so lower-bound search returns the
minimum capacity.

### Partition dynamic programming

Every ordered partition has a final block. Its capacity is the maximum of that block sum and the
optimal preceding partition capacity. Minimizing over all splits implements this exhaustive
optimal substructure.

## Walkthrough

[1,2,3,1,1], days=4 needs capacity 3: [1,2], [3], [1,1] takes three days. Capacity 2 cannot
carry the weight-3 package.

## Cost and pitfalls

Binary search with greedy loading: O(n log S) time; O(1) space.

Partition dynamic programming: O(days*n squared) time; O(n) space.

Inputs are unchanged. S is total weight. The requirement is at most days trips, so unused days
are allowed; package order cannot be changed.
"""


class Solution:
    """Approach: Binary search with greedy loading
    Time: O(n log S)
    Space: O(1)
    """

    def shipWithinDays(self, weights: list[int], days: int) -> int:
        low, high = max(weights), sum(weights)
        while low < high:
            capacity = (low + high) // 2
            used, load = 1, 0
            for weight in weights:
                if load + weight > capacity:
                    used += 1
                    load = 0
                load += weight
            if used <= days:
                high = capacity
            else:
                low = capacity + 1
        return low


class PartitionSolution:
    """Approach: Partition dynamic programming
    Time: O(days*n squared)
    Space: O(n)
    """

    def shipWithinDays(self, weights: list[int], days: int) -> int:
        size = len(weights)
        prefix = [0]
        for weight in weights:
            prefix.append(prefix[-1] + weight)
        previous = [0] + [float("inf")] * size
        for _ in range(days):
            current = [0] + [float("inf")] * size
            for end in range(1, size + 1):
                current[end] = min(
                    max(previous[start], prefix[end] - prefix[start]) for start in range(end)
                )
            previous = current
        return int(previous[-1])
