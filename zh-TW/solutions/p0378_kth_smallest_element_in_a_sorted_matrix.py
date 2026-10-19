"""## Task

Return the kth smallest entry of an n-by-n matrix sorted in ascending order across every row and
column. Repeated values occupy separate ranks.

## Hints

1. Count how many entries are no larger than a candidate value.
2. The count can be computed with a single staircase across the matrix.

## Approach

### Binary search the value range

Binary search from the smallest to largest value. For each midpoint, walk from bottom-left:
include a column prefix when its bottom candidate is small enough, otherwise move up.

### Heap merge sorted rows

Heapify the first entry of each sorted row. Pop k times, replacing each removed entry with its
next row neighbor.

## Why it works

### Binary search the value range

The staircase counts exactly entries at most the midpoint. This count is monotone, so the
smallest value with count at least k is the kth order statistic, including duplicates.

### Heap merge sorted rows

Every row head is its row's smallest remaining entry. Repeatedly choosing the minimum head
yields the matrix entries in sorted multiset order.

## Walkthrough

For [[1,3],[2,5]], sorted entries are [1,2,3,5]; k=3 returns 3.

## Cost and pitfalls

Binary search the value range: O(n log(W+1)) time; O(1) space.
Heap merge sorted rows: O(n + k log(n+1)) time; O(n) space.
The matrix is unchanged. W is max-min. Binary search returns a value, not a matrix index. The
heap method can be preferable when k is small, while value search avoids storage proportional to
n.
"""

from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Binary search the value range
    Time: O(n log(W+1))
    Space: O(1)
    """

    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        n = len(matrix)
        low, high = matrix[0][0], matrix[-1][-1]
        while low < high:
            middle = (low + high) // 2
            row, col, count = n - 1, 0, 0
            while row >= 0 and col < n:
                if matrix[row][col] <= middle:
                    count += row + 1
                    col += 1
                else:
                    row -= 1
            if count < k:
                low = middle + 1
            else:
                high = middle
        return low


class RowHeapSolution:
    """Approach: Heap merge sorted rows
    Time: O(n + k log(n+1))
    Space: O(n)
    """

    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        heap = [(row[0], index, 0) for index, row in enumerate(matrix)]
        heapify(heap)
        for _ in range(k):
            value, row, col = heappop(heap)
            if col + 1 < len(matrix):
                heappush(heap, (matrix[row][col + 1], row, col + 1))
        return value
