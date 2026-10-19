"""
## Task

Unit-width bars have nonnegative heights. Return the total water held between
them after rain; outside water drains away.

## Hints

1. Water at a bar depends on the smaller of the tallest boundaries on both sides.
2. If one known boundary is lower, must you know the other side's exact maximum?

## Approach

### Two running side maxima

Prefix and suffix maximum arrays give a linear baseline. Reduce their storage to
two running maxima. Process the side with the smaller known maximum, update that
maximum with its current bar, and add the difference above that bar.

### Monotonic basin stack

Keep decreasing-height indices. A taller incoming bar pops basin bottoms; the remaining left
wall and incoming right wall determine each newly closed water layer.

### Prefix and suffix maximum arrays

Materialize the tallest wall to each side of every bar. Its water depth is the shorter wall
minus the bar height. This uses more space than two pointers but makes each local depth
explicit.

## Why it works

### Two running side maxima

If the processed bar is below its side's maximum, the opposite known boundary is
at least that high, so the water level is settled. If it exceeds the maximum, it
is a new boundary and holds zero water. Each bar is settled once.

### Monotonic basin stack

Each popped bottom contributes the layer above it bounded by the shorter neighboring wall.
Layers are disjoint in height or horizontal position, and every bounded layer is closed once.

### Prefix and suffix maximum arrays

A cell can hold water precisely up to the shorter of the tallest walls on its two sides. Prefix
and suffix maxima compute those exact walls, so summing their bounded depths counts all water
once.

## Walkthrough

For [3, 0, 2, 0, 4], the inner positions hold 3, 1, and 3 units. Both end
bars hold zero, giving total 7.

## Cost and pitfalls

Default approach (Two running side maxima):

O(n) time and O(1) space; inputs are unchanged. Update the side maximum before
adding water so the contribution cannot be negative. Height alone is not a water
level; both boundaries matter. A single bar holds no water.

Two running side maxima: O(n) time; O(1) space.
Monotonic basin stack: O(n) time; O(n) space. Keep decreasing-height indices. A taller incoming
bar pops basin bottoms; the remaining left wall and incoming right wall determine each newly
closed water layer.

Prefix and suffix maximum arrays: O(n) time; O(n) space. Materialize the tallest wall to each
side of every bar. Its water depth is the shorter wall minus the bar height. This uses more
space than two pointers but makes each local depth explicit.
"""


class Solution:
    """Approach: Two running side maxima
    Time: O(n)
    Space: O(1)
    """

    def trap(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = right_max = water = 0
        while left <= right:
            if left_max <= right_max:
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1
        return water


class StackSolution:
    """Approach: Monotonic basin stack
    Time: O(n)
    Space: O(n)
    """

    def trap(self, height: list[int]) -> int:
        stack = []
        water = 0
        for right, value in enumerate(height):
            while stack and height[stack[-1]] < value:
                bottom = stack.pop()
                if not stack:
                    break
                left = stack[-1]
                water += (min(height[left], value) - height[bottom]) * (right - left - 1)
            stack.append(right)
        return water


class PrefixSuffixSolution:
    """Approach: Prefix and suffix maximum arrays
    Time: O(n)
    Space: O(n)
    """

    def trap(self, height: list[int]) -> int:
        prefix, suffix = height[:], height[:]
        for i in range(1, len(height)):
            prefix[i] = max(prefix[i - 1], height[i])
        for i in range(len(height) - 2, -1, -1):
            suffix[i] = max(suffix[i + 1], height[i])
        return sum(min(prefix[i], suffix[i]) - value for i, value in enumerate(height))
