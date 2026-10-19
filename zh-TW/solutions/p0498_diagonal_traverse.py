"""
## Task

Return a rectangular matrix in alternating upward-right and downward-left diagonal order,
starting at its top-left entry.

## Hints

1. Every diagonal has a constant row+column sum.
2. The parity of that sum determines traversal direction.

## Approach

### Diagonal coordinate bounds

For each row+column sum, enumerate its bounded row range forward or backward according to
parity.

### Group cells by diagonal

Append cells in row-major order to row+column buckets, then reverse even buckets before
concatenation.

## Why it works

### Diagonal coordinate bounds

Each cell belongs to exactly one sum diagonal. Reversing the row direction on alternating
diagonals produces precisely the required zigzag order without a visited grid.

### Group cells by diagonal

Row-major insertion orders each bucket by increasing row. Odd diagonals need that order, while
even diagonals need its reverse. Ordered bucket concatenation covers every cell once.

## Walkthrough

[[1,2,3],[4,5,6],[7,8,9]] gives [1,2,4,7,5,3,6,8,9]. Sum-2 diagonal is read from row 2 down to
row 0.

## Cost and pitfalls

Diagonal coordinate bounds: O(mn) time; O(1) auxiliary plus output space.

Group cells by diagonal: O(mn) time; O(mn) space.

Inputs are unchanged. m and n are dimensions. Single rows and columns follow the same coordinate
rules without special traversal code.
"""


class Solution:
    """Approach: Diagonal coordinate bounds
    Time: O(mn)
    Space: O(1) auxiliary plus output
    """

    def findDiagonalOrder(self, mat: list[list[int]]) -> list[int]:
        rows, cols = len(mat), len(mat[0])
        answer = []
        for diagonal in range(rows + cols - 1):
            low, high = max(0, diagonal - cols + 1), min(rows - 1, diagonal)
            indices = range(high, low - 1, -1) if diagonal % 2 == 0 else range(low, high + 1)
            for row in indices:
                answer.append(mat[row][diagonal - row])
        return answer


class BucketSolution:
    """Approach: Group cells by diagonal
    Time: O(mn)
    Space: O(mn)
    """

    def findDiagonalOrder(self, mat: list[list[int]]) -> list[int]:
        buckets = [[] for _ in range(len(mat) + len(mat[0]) - 1)]
        for row, values in enumerate(mat):
            for col, value in enumerate(values):
                buckets[row + col].append(value)
        answer = []
        for diagonal, values in enumerate(buckets):
            answer.extend(reversed(values) if diagonal % 2 == 0 else values)
        return answer
