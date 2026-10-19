"""
## Task

For every zero in the original matrix, set its entire row and column to zero in place. Return
None.

## Hints

1. Do not let newly written zeroes become new triggers.
2. Use the first row and first column as marker storage.

## Approach

### First-row and first-column markers

Remember whether the first row or column originally contains zero. Mark interior zeroes on those
boundaries, zero the interior, then finish the boundaries.

### Explicit zero row and column sets

Collect all original zero row and column indices before mutating any cell, then zero the
indicated cells in a second pass.

## Why it works

### First-row and first-column markers

Markers record exactly the rows and columns containing original zeroes. Delaying writes
preserves original observations, and separate boundary flags prevent marker writes from
inventing boundary triggers.

### Explicit zero row and column sets

The stored sets contain only original zero coordinates. A cell is overwritten exactly when its
row or column belongs to the trigger sets, matching the specification directly.

## Walkthrough

[[1,1,1],[1,0,1],[1,1,1]] becomes [[1,0,1],[0,0,0],[1,0,1]]. The new zero at (0,1) must not zero
row 0 completely.

## Cost and pitfalls

First-row and first-column markers: O(mn) time; O(1) space.

Explicit zero row and column sets: O(mn) time; O(m+n) space.

Both methods mutate the original rows and preserve object identity. The set method is a valid
simpler alternative but does not meet the optional constant-space follow-up.
"""


class Solution:
    """Approach: First-row and first-column markers
    Time: O(mn)
    Space: O(1)
    """

    def setZeroes(self, matrix: list[list[int]]) -> None:
        rows, cols = len(matrix), len(matrix[0])
        first_row = any(value == 0 for value in matrix[0])
        first_col = any(matrix[row][0] == 0 for row in range(rows))
        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][col] == 0:
                    matrix[row][0] = matrix[0][col] = 0
        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][0] == 0 or matrix[0][col] == 0:
                    matrix[row][col] = 0
        if first_row:
            for col in range(cols):
                matrix[0][col] = 0
        if first_col:
            for row in range(rows):
                matrix[row][0] = 0


class SetSolution:
    """Approach: Explicit zero row and column sets
    Time: O(mn)
    Space: O(m+n)
    """

    def setZeroes(self, matrix: list[list[int]]) -> None:
        rows, cols = set(), set()
        for row, values in enumerate(matrix):
            for col, value in enumerate(values):
                if value == 0:
                    rows.add(row)
                    cols.add(col)
        for row, values in enumerate(matrix):
            for col in range(len(values)):
                if row in rows or col in cols:
                    values[col] = 0
