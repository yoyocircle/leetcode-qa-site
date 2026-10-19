"""
## Task

Rotate an n by n matrix 90 degrees clockwise in place. Return None and retain the matrix and row
objects.

## Hints

1. A transpose followed by reversing each row gives a clockwise rotation.
2. A layer can also be rotated by four-cell cycles.

## Approach

### Transpose then reverse rows

Swap entries across the main diagonal, then reverse each row in place.

### Four-cell layer cycles

For every layer, move corresponding left, bottom, right, and top cells around one four-way
cycle.

## Why it works

### Transpose then reverse rows

Transposition maps (r,c) to (c,r), and row reversal maps that position to (c,n-1-r), exactly the
clockwise rotation coordinate.

### Four-cell layer cycles

The four cells in a cycle are successive clockwise rotations of one coordinate. Every noncentral
cell belongs to exactly one such cycle, so all cells rotate once.

## Walkthrough

[[1,2],[3,4]] maps its top-left 1 to top-right, producing [[3,1],[4,2]]. The center of an odd-
sized matrix stays fixed.

## Cost and pitfalls

Transpose then reverse rows: O(n squared) time; O(1) space.

Four-cell layer cycles: O(n squared) time; O(1) space.

Both methods mutate existing rows and require square input. Assigning matrix to a new rotated
list would not satisfy the in-place contract.
"""


class Solution:
    """Approach: Transpose then reverse rows
    Time: O(n squared)
    Space: O(1)
    """

    def rotate(self, matrix: list[list[int]]) -> None:
        size = len(matrix)
        for row in range(size):
            for col in range(row + 1, size):
                matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]
        for row in matrix:
            row.reverse()


class LayerSolution:
    """Approach: Four-cell layer cycles
    Time: O(n squared)
    Space: O(1)
    """

    def rotate(self, matrix: list[list[int]]) -> None:
        size = len(matrix)
        for first in range(size // 2):
            last = size - 1 - first
            for col in range(first, last):
                offset = col - first
                top = matrix[first][col]
                matrix[first][col] = matrix[last - offset][first]
                matrix[last - offset][first] = matrix[last][last - offset]
                matrix[last][last - offset] = matrix[col][last]
                matrix[col][last] = top
