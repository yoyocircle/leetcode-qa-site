"""
## Task

Return all entries of a rectangular matrix in clockwise spiral order, starting at the top-left
cell.

## Hints

1. Maintain the four boundaries of the unvisited rectangle.
2. A visited grid can instead drive one step at a time.

## Approach

### Shrinking rectangular boundaries

Emit top row, right column, bottom row, and left column, shrinking each completed boundary.

### Direction simulation with visited cells

Walk east, south, west, north, turning when the next cell is outside the matrix or already
visited.

## Why it works

### Shrinking rectangular boundaries

The remaining unvisited cells always form the inner rectangle. Each boundary pass visits a
disjoint outer edge; guards prevent revisiting the last single row or column.

### Direction simulation with visited cells

Each move follows the current unvisited boundary. Turning at an obstacle traces exactly the next
spiral edge; recording visited cells prevents repetition until all mn cells are emitted.

## Walkthrough

[[1,2,3],[4,5,6],[7,8,9]] emits [1,2,3,6,9,8,7,4,5]. A one-row matrix is emitted once.

## Cost and pitfalls

Shrinking rectangular boundaries: O(mn) time; O(1) auxiliary plus output space.

Direction simulation with visited cells: O(mn) time; O(mn) space.

Input is unchanged. m and n are dimensions. The boundary method emits entries directly instead
of allocating a row slice. Guard the final row and column against duplicate visits.
"""


class Solution:
    """Approach: Shrinking rectangular boundaries
    Time: O(mn)
    Space: O(1) auxiliary plus output
    """

    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
        answer = []
        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                answer.append(matrix[top][col])
            top += 1
            for row in range(top, bottom + 1):
                answer.append(matrix[row][right])
            right -= 1
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    answer.append(matrix[bottom][col])
                bottom -= 1
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    answer.append(matrix[row][left])
                left += 1
        return answer


class SimulationSolution:
    """Approach: Direction simulation with visited cells
    Time: O(mn)
    Space: O(mn)
    """

    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        rows, cols = len(matrix), len(matrix[0])
        visited = [[False] * cols for _ in range(rows)]
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        row = col = direction = 0
        answer = []
        for _ in range(rows * cols):
            answer.append(matrix[row][col])
            visited[row][col] = True
            dr, dc = directions[direction]
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or visited[nr][nc]:
                direction = (direction + 1) % 4
                dr, dc = directions[direction]
            row, col = row + dr, col + dc
        return answer
