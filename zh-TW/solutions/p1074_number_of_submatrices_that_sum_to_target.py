"""
## Task

Count nonempty axis-aligned submatrices whose entries sum to target. Values may be negative.

## Hints

1. Fix two row boundaries and compress the columns.
2. A two-dimensional prefix sum gives another direct rectangle-sum representation.

## Approach

### Row-pair compression with prefix counts

For each top row, extend a bottom row and accumulate column sums. Count target-sum subarrays in
the compressed vector using prefix frequencies.

### Two-dimensional prefixes and rectangle enumeration

Build a two-dimensional prefix-sum table and evaluate every rectangle with four lookups. This
educational baseline may time out at the largest dimensions.

## Why it works

### Row-pair compression with prefix counts

Every submatrix has a unique top/bottom pair and a unique column subarray. Compression preserves
its sum, and the one-dimensional prefix-count algorithm counts each such subarray exactly once.

### Two-dimensional prefixes and rectangle enumeration

Inclusion-exclusion removes the strips above and left of a rectangle, then restores their
double-subtracted intersection. Enumerating all boundary pairs therefore checks every rectangle
sum exactly once.

## Walkthrough

[[0,1,0],[1,1,1],[0,1,0]], target 0 has four zero-valued single-cell submatrices and no larger
zero-sum rectangle.

## Cost and pitfalls

Row-pair compression with prefix counts: O(m squared*n) time; O(n) space.

Two-dimensional prefixes and rectangle enumeration: O(m squared*n squared) time; O(mn) space.

Inputs are unchanged. m and n are dimensions. Negative values mean a positive-only sliding
window cannot replace prefix frequencies.
"""


class Solution:
    """Approach: Row-pair compression with prefix counts
    Time: O(m squared*n)
    Space: O(n)
    """

    def numSubmatrixSumTarget(self, matrix: list[list[int]], target: int) -> int:
        rows, cols = len(matrix), len(matrix[0])
        answer = 0
        for top in range(rows):
            compressed = [0] * cols
            for bottom in range(top, rows):
                counts = {0: 1}
                prefix = 0
                for col in range(cols):
                    compressed[col] += matrix[bottom][col]
                    prefix += compressed[col]
                    answer += counts.get(prefix - target, 0)
                    counts[prefix] = counts.get(prefix, 0) + 1
        return answer


class RectangleSolution:
    """Approach: Two-dimensional prefixes and rectangle enumeration
    Time: O(m squared*n squared)
    Space: O(mn)
    """

    def numSubmatrixSumTarget(self, matrix: list[list[int]], target: int) -> int:
        rows, cols = len(matrix), len(matrix[0])
        prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                prefix[r + 1][c + 1] = (
                    matrix[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
                )
        answer = 0
        for top in range(rows):
            for bottom in range(top + 1, rows + 1):
                for left in range(cols):
                    for right in range(left + 1, cols + 1):
                        total = (
                            prefix[bottom][right]
                            - prefix[top][right]
                            - prefix[bottom][left]
                            + prefix[top][left]
                        )
                        answer += total == target
        return answer
