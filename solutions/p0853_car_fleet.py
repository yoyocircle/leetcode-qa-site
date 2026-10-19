"""
## Task

Cars move toward one target and cannot pass each other. A faster car that catches
a slower group joins its fleet, including when they meet exactly at the target.
Count arriving fleets.

## Hints

1. Process cars from nearest the target to farthest away.
2. Compare arrival times instead of simulating positions over time.

## Approach

### Descending-position fleet times

Sort position-speed pairs by decreasing position. Track the arrival time of the
last fleet. A car with an arrival time no greater than that fleet catches it;
a car with a larger time creates a new fleet. Only the last fleet matters.

### Ascending-position fleet stack

Scan cars from farthest to nearest. Keep a stack of candidate fleet arrival fractions; a nearer
slower car absorbs all faster trailing fleets whose arrival time is no later.

## Why it works

### Descending-position fleet times

A car cannot bypass the nearest fleet ahead of it. If it reaches the target
no later than that fleet would, their paths must meet by the target. Otherwise
it stays behind and starts a separate fleet.

### Ascending-position fleet stack

A trailing fleet catches the next fleet exactly when its free arrival time is no greater.
Popping all such fleets and retaining the nearer fleet time produces exactly the surviving
fleets in road order.

## Walkthrough

With target 10, positions [8, 6, 0] and speeds [1, 2, 1] have arrival times
2, 2, and 10 in front-to-back order. The first two merge; the result is 2 fleets.

## Cost and pitfalls

Default approach (Descending-position fleet times):

O(n log n) time and O(n) sorting space. Input lists are unchanged. Keep each speed
paired with its position. Equality merges fleets. This implementation uses integer
cross-products to compare arrival fractions without floating-point rounding.

Descending-position fleet times: O(n log n) time; O(n) space.
Ascending-position fleet stack: O(n log n) time; O(n) space. Scan cars from farthest to nearest.
Keep a stack of candidate fleet arrival fractions; a nearer slower car absorbs all faster
trailing fleets whose arrival time is no later.
"""


class Solution:
    """Approach: Descending-position fleet times
    Time: O(n log n)
    Space: O(n)
    """

    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        fleets = 0
        fleet_distance, fleet_speed = -1, 1
        for start, velocity in sorted(zip(position, speed, strict=True), reverse=True):
            distance = target - start
            if distance * fleet_speed > fleet_distance * velocity:
                fleets += 1
                fleet_distance, fleet_speed = distance, velocity
        return fleets


class FleetStackSolution:
    """Approach: Ascending-position fleet stack
    Time: O(n log n)
    Space: O(n)
    """

    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        fleets = []
        for start, velocity in sorted(zip(position, speed, strict=True)):
            distance = target - start
            while fleets and fleets[-1][0] * velocity <= distance * fleets[-1][1]:
                fleets.pop()
            fleets.append((distance, velocity))
        return len(fleets)
