"""
## Task

Search a rectangular matrix in which each row and each column is sorted in increasing order. Row
ranges may overlap.

## Hints

1. At the top-right corner, a comparison eliminates one whole row or column.
2. Each row can also be searched independently.

## Approach

### Top-right staircase elimination

Start at the top-right. Move left for a value above target and down for a value below it.

### Binary search each candidate row

Skip rows whose endpoints exclude target, then run ordinary binary search within every remaining
row.

## Why it works

### Top-right staircase elimination

A too-large corner excludes its entire remaining column because lower entries are no smaller. A
too-small corner excludes its remaining row because left entries are no larger. The target
remains in the surviving rectangle.

### Binary search each candidate row

Row order guarantees binary search finds a target if it belongs to that row. Endpoint skips
exclude only impossible rows, and examining all other rows covers every matrix position.

## Walkthrough

In [[1,4,7],[2,5,8],[3,6,9]], searching for 6 moves left from 7, down from 4 and 5, then finds
6.

## Cost and pitfalls

Top-right staircase elimination: O(m+n) time; O(1) space.

Binary search each candidate row: O(m log(n+1)) time; O(1) space.

Inputs are unchanged. m and n are row and column counts. Flattened binary search is invalid here
because row-major order need not be globally sorted.
"""


class Solution:
    """Approach: Top-right staircase elimination
    Time: O(m+n)
    Space: O(1)
    """

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        row, col = 0, len(matrix[0]) - 1
        while row < len(matrix) and col >= 0:
            value = matrix[row][col]
            if value == target:
                return True
            if value > target:
                col -= 1
            else:
                row += 1
        return False


class RowSearchSolution:
    """Approach: Binary search each candidate row
    Time: O(m log(n+1))
    Space: O(1)
    """

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        for row in matrix:
            if target < row[0] or target > row[-1]:
                continue
            low, high = 0, len(row) - 1
            while low <= high:
                middle = (low + high) // 2
                if row[middle] == target:
                    return True
                if row[middle] < target:
                    low = middle + 1
                else:
                    high = middle - 1
        return False
