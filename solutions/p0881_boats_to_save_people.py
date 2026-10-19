"""
## Task

Each boat holds at most two people and total weight at most limit. Return the minimum number of
boats. Every person individually fits.

## Hints

1. A heaviest remaining person must take a boat now.
2. Pair that person with the lightest if any partner is possible.

## Approach

### Sort and pair extremes

Sort a copy. Assign the heaviest person a boat and include the lightest remaining person
whenever their sum fits.

### Weight-frequency pairing

Count each possible weight, then use moving lightest/heaviest occupied buckets. This avoids
comparison sorting when the bounded weight range is favorable.

## Why it works

### Sort and pair extremes

If the lightest cannot share with the heaviest, nobody can. If they fit, exchanging the lightest
into the heaviest boat cannot increase the boats needed by an optimal assignment.

### Weight-frequency pairing

Bucket pointers represent the same lightest and heaviest remaining people as the sorted
algorithm. Each iteration removes the heaviest and the lightest feasible partner, preserving its
optimal exchange argument.

## Walkthrough

[3,2,2,1], limit 3: the 3 goes alone, one 2 pairs with 1, and the other 2 goes alone, for three
boats.

## Cost and pitfalls

Sort and pair extremes: O(n log n) time; O(n) space.

Weight-frequency pairing: O(n+limit) time; O(limit) space.

Inputs are unchanged. The two-person capacity is essential; this greedy proof does not solve
unrestricted bin packing.
"""


class Solution:
    """Approach: Sort and pair extremes
    Time: O(n log n)
    Space: O(n)
    """

    def numRescueBoats(self, people: list[int], limit: int) -> int:
        weights = sorted(people)
        left, right, boats = 0, len(weights) - 1, 0
        while left <= right:
            if left < right and weights[left] + weights[right] <= limit:
                left += 1
            right -= 1
            boats += 1
        return boats


class CountingSolution:
    """Approach: Weight-frequency pairing
    Time: O(n+limit)
    Space: O(limit)
    """

    def numRescueBoats(self, people: list[int], limit: int) -> int:
        counts = [0] * (limit + 1)
        for weight in people:
            counts[weight] += 1
        light, heavy, remaining, boats = 1, limit, len(people), 0
        while remaining:
            while counts[heavy] == 0:
                heavy -= 1
            counts[heavy] -= 1
            remaining -= 1
            boats += 1
            if not remaining:
                break
            while counts[light] == 0:
                light += 1
            if light + heavy <= limit:
                counts[light] -= 1
                remaining -= 1
        return boats
