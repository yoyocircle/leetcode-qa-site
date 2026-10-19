"""
## Task

Create an n by n matrix filled with integers 1 through n squared in clockwise spiral order.

## Hints

1. Use the same four-edge traversal as reading a spiral.
2. A zero-filled output can itself mark unfilled cells.

## Approach

### Layer boundary filling

Fill each outer rectangle edge, then advance its boundaries inward.

### Output-marked direction simulation

Walk in four directions, turning when the next output entry is already nonzero or out of bounds.

## Why it works

### Layer boundary filling

The boundaries enclose exactly the unfilled cells. Each edge receives consecutive values in
spiral order and is then excluded, so every cell gets its required rank once.

### Output-marked direction simulation

Every filled entry is positive while every unfilled entry is zero. The obstacle rule follows the
clockwise unfilled boundary until all ranks are assigned exactly once.

## Walkthrough

n=3 yields [[1,2,3],[8,9,4],[7,6,5]]. The final value 9 occupies the center.

## Cost and pitfalls

Layer boundary filling: O(n squared) time; O(1) auxiliary plus output space.

Output-marked direction simulation: O(n squared) time; O(1) auxiliary plus output space.

There is no mutable input. Returned rows must be independent; [[0]*n]*n would incorrectly share
all rows.
"""


class Solution:
    """Approach: Layer boundary filling
    Time: O(n squared)
    Space: O(1) auxiliary plus output
    """

    def generateMatrix(self, n: int) -> list[list[int]]:
        matrix = [[0] * n for _ in range(n)]
        top, bottom, left, right, value = 0, n - 1, 0, n - 1, 1
        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                matrix[top][col] = value
                value += 1
            top += 1
            for row in range(top, bottom + 1):
                matrix[row][right] = value
                value += 1
            right -= 1
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    matrix[bottom][col] = value
                    value += 1
                bottom -= 1
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    matrix[row][left] = value
                    value += 1
                left += 1
        return matrix


class SimulationSolution:
    """Approach: Output-marked direction simulation
    Time: O(n squared)
    Space: O(1) auxiliary plus output
    """

    def generateMatrix(self, n: int) -> list[list[int]]:
        matrix = [[0] * n for _ in range(n)]
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        row = col = direction = 0
        for value in range(1, n * n + 1):
            matrix[row][col] = value
            dr, dc = directions[direction]
            nr, nc = row + dr, col + dc
            if not (0 <= nr < n and 0 <= nc < n) or matrix[nr][nc]:
                direction = (direction + 1) % 4
                dr, dc = directions[direction]
            row, col = row + dr, col + dc
        return matrix
