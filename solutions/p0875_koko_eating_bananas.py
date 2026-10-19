"""
## Task

Find the smallest integer eating speed that finishes all piles within h hours.
Each hour handles only one pile. There are at least as many hours as piles.

## Hints

1. At speed k, a pile of p needs ceiling(p/k) whole hours.
2. If one speed works, which larger speeds also work?

## Approach

### Binary search feasible speed

Binary search the answer from 1 through the largest pile. A speed is feasible
when the sum of its per-pile ceiling hours is at most h. Keep the lower half
when feasible and the upper half otherwise.

### Enumerate candidate speeds

Try speeds in increasing order and return the first meeting the hour budget. This educational
baseline may time out for large pile values; it exposes the monotone predicate used by binary
search.

## Why it works

### Binary search feasible speed

Increasing speed never increases required hours, so feasibility changes from
False to True at most once. The interval always contains the first feasible
speed; max(piles) is feasible because it finishes each pile within one hour.

### Enumerate candidate speeds

Each tested speed consumes the sum of ceiling-divided pile sizes. Testing every smaller speed
before returning proves that the first feasible one is minimal.

## Walkthrough

For piles [4, 8] and h=4, speed 2 needs 2+4=6 hours, while speed 3 needs
2+3=5. Speed 4 needs 1+2=3, so the minimum is 4.

## Cost and pitfalls

Default approach (Binary search feasible speed):

O(n log M) time and O(1) auxiliary space for maximum pile M; input is unchanged.
Use (pile+speed-1)//speed for exact integer ceilings. Averaging total bananas
across hours ignores the restriction against sharing an hour between piles.

Binary search feasible speed: O(n log M) time; O(1) space.
Enumerate candidate speeds: O(nM) time; O(1) space. Try speeds in increasing order and return
the first meeting the hour budget. This educational baseline may time out for large pile values;
it exposes the monotone predicate used by binary search.
"""


class Solution:
    """Approach: Binary search feasible speed
    Time: O(n log M)
    Space: O(1)
    """

    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        left, right = 1, max(piles)
        while left < right:
            speed = (left + right) // 2
            hours = sum((pile + speed - 1) // speed for pile in piles)
            if hours <= h:
                right = speed
            else:
                left = speed + 1
        return left


class EnumerationSolution:
    """Approach: Enumerate candidate speeds
    Time: O(nM)
    Space: O(1)
    """

    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        for speed in range(1, max(piles) + 1):
            if sum((pile + speed - 1) // speed for pile in piles) <= h:
                return speed
        raise ValueError("The problem guarantees enough hours")
