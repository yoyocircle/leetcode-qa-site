"""
## Task

Construct an immutable rectangular range-sum object. sumRegion(row1,col1,row2,col2) returns the
inclusive rectangle sum.

## Hints

1. Pad prefix sums with a zero row and column.
2. Row prefixes trade faster construction logic for slower rectangle queries.

## Approach

### Two-dimensional prefix sums

Store a padded table of top-left rectangle sums. Answer with four prefix accesses by inclusion-
exclusion.

### Independent row prefix sums

Store prefix sums separately in each row and add the requested column-slice sum across the
requested rows.

## Why it works

### Two-dimensional prefix sums

Subtracting the top and left strips from the bottom-right prefix removes all outside cells;
adding back their intersection corrects double subtraction.

### Independent row prefix sums

Two row-prefix values give each included row's exact horizontal slice. Summing the disjoint
slices covers exactly the queried rectangle.

## Walkthrough

For [[1,2],[3,4]], sumRegion(0,1,1,1) adds the right column 2+4=6.

## Cost and pitfalls

Two-dimensional prefix sums: O(mn) construction; O(1) query time; O(mn) space.

Independent row prefix sums: O(mn) construction; O(m) query time; O(mn) space.

The constructor snapshots sums and does not mutate or retain mutable input rows. m and n are
dimensions; all query coordinates are valid and inclusive.
"""


class NumMatrix:
    """Approach: Two-dimensional prefix sums
    Time: O(mn) construction; O(1) query
    Space: O(mn)
    """

    def __init__(self, matrix: list[list[int]]):
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for row in range(rows):
            for col in range(cols):
                self.prefix[row + 1][col + 1] = (
                    matrix[row][col]
                    + self.prefix[row][col + 1]
                    + self.prefix[row + 1][col]
                    - self.prefix[row][col]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self.prefix
        return p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1] + p[row1][col1]


class RowPrefixNumMatrix:
    """Approach: Independent row prefix sums
    Time: O(mn) construction; O(m) query
    Space: O(mn)
    """

    def __init__(self, matrix: list[list[int]]):
        self.prefix = []
        for row in matrix:
            sums = [0]
            for value in row:
                sums.append(sums[-1] + value)
            self.prefix.append(sums)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum(
            self.prefix[row][col2 + 1] - self.prefix[row][col1] for row in range(row1, row2 + 1)
        )
