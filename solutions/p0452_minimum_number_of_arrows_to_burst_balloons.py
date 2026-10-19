"""
## Task

Each closed interval describes a balloon. An arrow at x bursts every balloon whose interval
contains x. Return the minimum arrows.

## Hints

1. Shoot at the earliest ending remaining interval.
2. Overlapping balloon groups can also be tracked by their common intersection.

## Approach

### Earliest-end arrow placement

Sort by right endpoint. Place a new arrow at an interval end only when the preceding arrow lies
before its start.

### Start-order intersection groups

Sort by start and maintain the right edge of the common intersection. A disjoint new interval
closes one arrow group.

## Why it works

### Earliest-end arrow placement

Any arrow bursting the earliest-ending balloon can be moved to its right endpoint without losing
any other currently intersected balloon. Repeating this exchange yields an optimal greedy
assignment.

### Start-order intersection groups

All intervals in a group share the maintained intersection, so one arrow suffices. A new start
beyond that intersection requires a second arrow in every assignment, justifying the group
split.

## Walkthrough

[[10,16],[2,8],[1,6],[7,12]] can be burst at x=6 and x=12, for two arrows.

## Cost and pitfalls

Earliest-end arrow placement: O(n log n) time; O(n) space.

Start-order intersection groups: O(n log n) time; O(n) space.

Inputs are unchanged. Intervals are closed: touching endpoints share an arrow, unlike the
compatibility rule for non-overlapping half-open intervals.
"""


class Solution:
    """Approach: Earliest-end arrow placement
    Time: O(n log n)
    Space: O(n)
    """

    def findMinArrowShots(self, points: list[list[int]]) -> int:
        arrows = 0
        position = float("-inf")
        for start, end in sorted(points, key=lambda point: point[1]):
            if start > position:
                arrows += 1
                position = end
        return arrows


class IntersectionSolution:
    """Approach: Start-order intersection groups
    Time: O(n log n)
    Space: O(n)
    """

    def findMinArrowShots(self, points: list[list[int]]) -> int:
        end = float("-inf")
        arrows = 0
        for start, finish in sorted(points):
            if start > end:
                arrows += 1
                end = finish
            else:
                end = min(end, finish)
        return arrows
