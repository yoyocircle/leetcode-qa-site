"""
## Task

Find the largest rectangle formed by consecutive unit-width histogram bars.
The rectangle's height cannot exceed its shortest covered bar.

## Hints

1. For each candidate height, find the widest interval where it remains valid.
2. A shorter incoming bar tells you where taller candidates must end.

## Approach

### Increasing-height stack

Maintain increasing candidate heights paired with their earliest start indices.
When a shorter bar arrives, pop taller candidates and compute their maximal
rightward area. Carry the popped start leftward for the new height. A virtual
zero-height bar at the end flushes remaining candidates.

### Nearest smaller boundaries

Compute the nearest strictly smaller bar on each side with two stack scans, then use each bar as
the limiting height over its widest legal span.

## Why it works

### Increasing-height stack

Each stored height can extend from its saved start through the previous bar.
The first shorter bar is its right boundary; it cannot extend farther. Every
optimal rectangle has a minimum bar whose full valid span is evaluated.

### Nearest smaller boundaries

Any rectangle has a minimum-height bar. For that bar, the nearest smaller boundaries give the
maximal span at its height, which contains the original rectangle and has at least its area.

## Walkthrough

For [2, 4, 4, 1], the final 1 closes height-4 spans of width 1 then 2,
giving best area 8. Height 2 covers width 3 for area 6.

## Cost and pitfalls

Default approach (Increasing-height stack):

O(n) time and O(n) space; each candidate enters and leaves once. Input is unchanged.
Width is current_index-start. Propagate the earliest popped start; forgetting it
loses wide rectangles. The sentinel is virtual, so no zero is appended to the input.

Increasing-height stack: O(n) time; O(n) space.
Nearest smaller boundaries: O(n) time; O(n) space. Compute the nearest strictly smaller bar on
each side with two stack scans, then use each bar as the limiting height over its widest legal
span.
"""


class Solution:
    """Approach: Increasing-height stack
    Time: O(n)
    Space: O(n)
    """

    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        best = 0
        for i in range(len(heights) + 1):
            height = heights[i] if i < len(heights) else 0
            start = i
            while stack and stack[-1][1] > height:
                start, previous = stack.pop()
                best = max(best, previous * (i - start))
            stack.append((start, height))
        return best


class BoundarySolution:
    """Approach: Nearest smaller boundaries
    Time: O(n)
    Space: O(n)
    """

    def largestRectangleArea(self, heights: list[int]) -> int:
        size = len(heights)
        left, right = [-1] * size, [size] * size
        stack = []
        for i, value in enumerate(heights):
            while stack and heights[stack[-1]] >= value:
                stack.pop()
            if stack:
                left[i] = stack[-1]
            stack.append(i)
        stack.clear()
        for i in range(size - 1, -1, -1):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            if stack:
                right[i] = stack[-1]
            stack.append(i)
        return max(
            (height * (right[i] - left[i] - 1) for i, height in enumerate(heights)), default=0
        )
