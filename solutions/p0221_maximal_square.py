"""## Task

Find the area of the largest square containing only character "1" cells.

## Hints

1. A square ending here depends on its upper, left, and diagonal neighbors.
2. A rectangle-sum table can test whether any chosen square is all ones.

## Approach

### Rolling square-side DP

Store the largest all-one square ending at each column. For a one, grow the smallest of the
three neighboring square sizes; reset at zero.

### Prefix sums and binary-search side length

Build a two-dimensional count prefix table. Test all square locations in constant time each,
and binary-search the greatest feasible side.

## Why it works

### Rolling square-side DP

A square of side k requires all three predecessor squares of side k-1 and the current one.
Their union supplies every cell, making their minimum plus one both sufficient and
necessary.

### Prefix sums and binary-search side length

A square is all ones exactly when its count equals its area. Any feasible square contains
smaller feasible squares, so side feasibility is monotone and binary search is valid.

## Walkthrough

For [["1","1"],["1","1"]], the greatest side length is 2 and area is 4.

## Cost and pitfalls

Rolling square-side DP: O(R*C) time; O(C) space.
Prefix sums and binary-search side length: O(R*C*log(min(R,C)+1)) time; O(R*C) space.

Inputs are unchanged. Return area, not side length. Prefix sums use more space and time but
demonstrate reusable rectangle queries.
"""


class Solution:
    """Approach: Rolling square-side DP
    Time: O(R*C)
    Space: O(C)
    """

    def maximalSquare(self, matrix: list[list[str]]) -> int:
        dp = [0] * (len(matrix[0]) + 1)
        best = 0
        for row in matrix:
            diagonal = 0
            for column, value in enumerate(row, 1):
                above = dp[column]
                dp[column] = 1 + min(above, dp[column - 1], diagonal) if value == "1" else 0
                diagonal = above
                best = max(best, dp[column])
        return best * best


class PrefixSolution:
    """Approach: Prefix sums and binary-search side length
    Time: O(R*C*log(min(R,C)+1))
    Space: O(R*C)
    """

    def maximalSquare(self, matrix: list[list[str]]) -> int:
        rows, columns = len(matrix), len(matrix[0])
        prefix = [[0] * (columns + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(columns):
                prefix[r + 1][c + 1] = (
                    int(matrix[r][c]) + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
                )

        def possible(side):
            for r in range(side, rows + 1):
                for c in range(side, columns + 1):
                    total = (
                        prefix[r][c]
                        - prefix[r - side][c]
                        - prefix[r][c - side]
                        + prefix[r - side][c - side]
                    )
                    if total == side * side:
                        return True
            return False

        low, high = 0, min(rows, columns) + 1
        while low + 1 < high:
            middle = (low + high) // 2
            if possible(middle):
                low = middle
            else:
                high = middle
        return low * low
