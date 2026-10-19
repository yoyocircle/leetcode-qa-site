"""## Task

Count all axis-aligned square submatrices containing only integer ones.

## Hints

1. The largest square ending at a cell determines the count of all squares ending there.
2. Prefix sums can test a candidate square size exactly.

## Approach

### Rolling largest-square endpoint DP

For a one cell, take one plus the minimum largest-square side from above, left, and the
saved diagonal. Add that side length to the total count.

### Prefix sums and endpoint size searches

Build rectangle-sum prefixes, then binary-search the largest all-one square ending at each
cell and add its side length.

## Why it works

### Rolling largest-square endpoint DP

The three predecessor squares support exactly a square one larger than their minimum. If the
largest ending square has side L, it contains exactly one ending square for each side 1..L,
so its contribution is L.

### Prefix sums and endpoint size searches

A candidate is all ones exactly when its count equals its area. Feasible ending sizes form a
prefix because every smaller ending square lies inside the larger one, validating binary
search and the side-length count.

## Walkthrough

An all-one 2x2 matrix has four single-cell squares and one larger square, giving 5.

## Cost and pitfalls

Rolling largest-square endpoint DP: O(R*C) time; O(C) space.
Prefix sums and endpoint size searches: O(R*C*log(min(R,C)+1)) time; O(R*C) space.

Both preserve matrix. Prefix storage offers reusable rectangle queries at a higher memory
cost; the rolling DP needs only one row and an old diagonal. Return a square count, not the
largest area.
"""


class Solution:
    """Approach: Rolling largest-square endpoint DP
    Time: O(R*C)
    Space: O(C)
    """

    def countSquares(self, matrix: list[list[int]]) -> int:
        dp = [0] * (len(matrix[0]) + 1)
        answer = 0
        for row in matrix:
            diagonal = 0
            for column, value in enumerate(row, 1):
                above = dp[column]
                dp[column] = 1 + min(above, dp[column - 1], diagonal) if value else 0
                answer += dp[column]
                diagonal = above
        return answer


class PrefixSolution:
    """Approach: Prefix sums and endpoint size searches
    Time: O(R*C*log(min(R,C)+1))
    Space: O(R*C)
    """

    def countSquares(self, matrix: list[list[int]]) -> int:
        rows, columns = len(matrix), len(matrix[0])
        prefix = [[0] * (columns + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(columns):
                prefix[r + 1][c + 1] = (
                    matrix[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
                )
        answer = 0
        for r in range(1, rows + 1):
            for c in range(1, columns + 1):
                low, high = 0, min(r, c) + 1
                while low + 1 < high:
                    side = (low + high) // 2
                    count = (
                        prefix[r][c]
                        - prefix[r - side][c]
                        - prefix[r][c - side]
                        + prefix[r - side][c - side]
                    )
                    if count == side * side:
                        low = side
                    else:
                        high = side
                answer += low
        return answer
