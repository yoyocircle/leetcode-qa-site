"""## Task

Choose values to earn their full summed occurrences, but selecting value x removes every
occurrence of x-1 and x+1.

## Hints

1. All copies of the same value can be aggregated.
2. The conflict graph becomes a path along sorted integer values.

## Approach

### Sparse sorted-value take and skip

Aggregate earnings in a dictionary and process distinct values in order. Taking an adjacent
value requires the preceding skip state; across a gap, either prior optimum is allowed.

### Dense value-axis robber DP

Allocate one earnings bucket for every value through the maximum and run the ordinary
two-prefix robber recurrence over those buckets.

## Why it works

### Sparse sorted-value take and skip

Once x is chosen, taking all its identical copies adds earnings without creating new
conflicts. Only neighboring integer values conflict, so the take/skip path recurrence is
exhaustive.

### Dense value-axis robber DP

Each neighboring bucket represents exactly a forbidden pair of selected values. Taking or
skipping each bucket therefore describes every legal value selection, with empty buckets
naturally bridging gaps.

## Walkthrough

For [2,2,3,3,3,4], choosing all threes earns 9, beating all twos plus the four for 8.

## Cost and pitfalls

Sparse sorted-value take and skip: O(n+u log u) expected time; O(u) space.
Dense value-axis robber DP: O(n+U) time; O(U) space.

u is distinct count and U=max(nums)+1. Both preserve nums. The dense variant is attractive
for the official value bound of 10000; sparse storage avoids paying for a large mostly empty
value axis.
"""


class Solution:
    """Approach: Sparse sorted-value take and skip
    Time: O(n+u log u) expected
    Space: O(u)
    """

    def deleteAndEarn(self, nums: list[int]) -> int:
        points = {}
        for value in nums:
            points[value] = points.get(value, 0) + value
        take = skip = 0
        previous = None
        for value in sorted(points):
            best = max(take, skip)
            take, skip = (
                (skip if previous is not None and value == previous + 1 else best) + points[value],
                best,
            )
            previous = value
        return max(take, skip)


class BucketSolution:
    """Approach: Dense value-axis robber DP
    Time: O(n+U)
    Space: O(U)
    """

    def deleteAndEarn(self, nums: list[int]) -> int:
        points = [0] * (max(nums) + 1)
        for value in nums:
            points[value] += value
        older = previous = 0
        for gain in points:
            older, previous = previous, max(previous, older + gain)
        return previous
