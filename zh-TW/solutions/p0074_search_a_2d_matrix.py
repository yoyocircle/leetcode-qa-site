"""
## Task

Search a rectangular matrix whose rows increase and whose next-row first value exceeds the
preceding row's last value.

## Hints

1. The whole matrix is one increasing sequence in row-major order.
2. You can instead choose a row before searching inside it.

## Approach

### Virtual flattened binary search

Binary-search indices from zero to mn-1 and translate each midpoint with divmod by the column
count.

### Row selection then column search

Find the last row whose first value is at most target, then binary-search that row.

## Why it works

### Virtual flattened binary search

The row separation guarantee makes virtual row-major order globally sorted. Ordinary binary-
search comparisons therefore discard only impossible indices.

### Row selection then column search

Every earlier row ends below the selected row's first value and every later row starts above
target. Only the selected row can contain target; its internal order permits binary search.

## Walkthrough

In [[1,3,5],[7,9,11]], target 9 maps to virtual index 4 and row 1, column 1.

## Cost and pitfalls

Virtual flattened binary search: O(log(mn)) time; O(1) space.

Row selection then column search: O(log m+log n) time; O(1) space.

Input is unchanged. m and n are rows and columns. The stronger row separation guarantee is
required; independently sorted rows and columns alone do not suffice.
"""


class Solution:
    """Approach: Virtual flattened binary search
    Time: O(log(mn))
    Space: O(1)
    """

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        low, high = 0, rows * cols - 1
        while low <= high:
            middle = (low + high) // 2
            row, col = divmod(middle, cols)
            if matrix[row][col] == target:
                return True
            if matrix[row][col] < target:
                low = middle + 1
            else:
                high = middle - 1
        return False


class TwoStageSolution:
    """Approach: Row selection then column search
    Time: O(log m+log n)
    Space: O(1)
    """

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        low, high = 0, len(matrix)
        while low < high:
            middle = (low + high) // 2
            if matrix[middle][0] <= target:
                low = middle + 1
            else:
                high = middle
        if low == 0:
            return False
        row = matrix[low - 1]
        left, right = 0, len(row)
        while left < right:
            middle = (left + right) // 2
            if row[middle] < target:
                left = middle + 1
            else:
                right = middle
        return left < len(row) and row[left] == target
