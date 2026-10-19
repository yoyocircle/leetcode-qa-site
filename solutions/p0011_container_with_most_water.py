"""
## Task

Choose two vertical lines to maximize the area between them and the horizontal
axis. The area is the distance between indices times the shorter height.

## Hints

1. Begin with the widest candidate.
2. Can moving the taller endpoint improve the area while the shorter stays fixed?

## Approach

### Inward height pointers

All pairs take O(n squared) time. Evaluate the two outside lines, then move the
shorter endpoint inward. Continue until the endpoints meet.

### Enumerate wall pairs

Evaluate every pair of walls directly. This educational baseline may time out at full
constraints and is useful as a small-input oracle.

## Why it works

### Inward height pointers

Keeping the shorter line while decreasing width cannot improve the current area:
the limiting height stays at most that short line. Thus no better pair needs that
endpoint among the remaining candidates. Repeating this safe elimination preserves
an optimal pair until its area is considered.

### Enumerate wall pairs

Every possible container is one unordered pair of indices. Its width times the shorter height is
its exact area, so the maximum over all pairs is the answer.

## Walkthrough

For [2, 5, 4, 3], the outside pair gives 3*2=6. Move left to height 5:
the pair with height 3 gives 2*3=6. The last pair gives 4, so the answer is 6.

## Cost and pitfalls

Default approach (Inward height pointers):

O(n) time and O(1) space. Inputs are unchanged. Width is right-left, not the
number of included bars. Equal heights allow either endpoint to move. Do not
confuse this with Trapping Rain Water, which sums water across all positions.

Inward height pointers: O(n) time; O(1) space.
Enumerate wall pairs: O(n squared) time; O(1) space. Evaluate every pair of walls directly. This
educational baseline may time out at full constraints and is useful as a small-input oracle.
"""


class Solution:
    """Approach: Inward height pointers
    Time: O(n)
    Space: O(1)
    """

    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            best = max(best, (right - left) * min(height[left], height[right]))
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1
        return best


class PairEnumerationSolution:
    """Approach: Enumerate wall pairs
    Time: O(n squared)
    Space: O(1)
    """

    def maxArea(self, height: list[int]) -> int:
        best = 0
        for left in range(len(height)):
            for right in range(left + 1, len(height)):
                best = max(best, (right - left) * min(height[left], height[right]))
        return best
