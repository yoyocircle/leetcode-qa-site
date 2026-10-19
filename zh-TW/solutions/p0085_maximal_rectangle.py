"""## Task

Return the largest area of an axis-aligned all-one rectangle in a binary character matrix.

## Hints

1. Each row can be the bottom of a histogram of consecutive ones.
2. Alternatively track persistent left and right boundaries for every column.

## Approach

### Histogram heights and monotone stack

Update vertical one-runs, then solve each row histogram. A zero sentinel flushes a stack of
increasing-height indices.

### Persistent left and right limits

Retain each column height and the intersection of horizontal one-runs over that height. A
left scan tightens lower bounds and a right scan tightens upper bounds.

## Why it works

### Histogram heights and monotone stack

Every all-one rectangle has a bottom row and a minimum histogram height. Popping that height
finds its widest allowed span, covering the optimum; each stack index enters and leaves
once.

### Persistent left and right limits

Intersecting the horizontal runs of all contributing rows gives exactly the legal width for
that height. Each candidate rectangle is valid, and the minimum-height column of any optimum
considers an at-least-as-wide candidate.

## Walkthrough

For [["1","0","1"],["1","1","1"]], the bottom row gives area 3.

## Cost and pitfalls

Histogram heights and monotone stack: O(R*C) time; O(C) space.
Persistent left and right limits: O(R*C) time; O(C) space.

Inputs are unchanged. Reset both bounds when a zero breaks the vertical run. Histogram
sentinel storage and boundary arrays are auxiliary, not modifications to matrix.
"""


class Solution:
    """Approach: Histogram heights and monotone stack
    Time: O(R*C)
    Space: O(C)
    """

    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        heights = [0] * (len(matrix[0]) + 1)
        answer = 0
        for row in matrix:
            for column, value in enumerate(row):
                heights[column] = heights[column] + 1 if value == "1" else 0
            stack = [-1]
            for column, height in enumerate(heights):
                while len(stack) > 1 and heights[stack[-1]] > height:
                    top = stack.pop()
                    answer = max(answer, heights[top] * (column - stack[-1] - 1))
                stack.append(column)
        return answer


class BoundarySolution:
    """Approach: Persistent left and right limits
    Time: O(R*C)
    Space: O(C)
    """

    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        width = len(matrix[0])
        heights, left, right = [0] * width, [0] * width, [width] * width
        answer = 0
        for row in matrix:
            boundary = 0
            for c in range(width):
                if row[c] == "1":
                    heights[c] += 1
                    left[c] = max(left[c], boundary)
                else:
                    heights[c], left[c], right[c], boundary = 0, 0, width, c + 1
            boundary = width
            for c in range(width - 1, -1, -1):
                if row[c] == "1":
                    right[c] = min(right[c], boundary)
                    answer = max(answer, heights[c] * (right[c] - left[c]))
                else:
                    boundary = c
        return answer
