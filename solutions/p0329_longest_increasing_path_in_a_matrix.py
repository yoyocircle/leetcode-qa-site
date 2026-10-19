"""## Task

Find the longest strictly increasing path through a nonempty matrix.
Move to an orthogonal neighbor at each step; diagonal moves are forbidden.
The path length counts cells, including its start.

## Hints

1. Direct an edge from each cell to every larger neighbor; increasing edges cannot cycle.
2. Process this directed acyclic graph in layers, starting with cells of indegree zero.

## Approach

### Topological indegree layers

Count each cell's smaller neighbors as its incoming edges. Queue all cells
with zero indegree. Process one queue layer at a time: remove its cells,
decrement the indegrees of their larger neighbors, and enqueue neighbors
whose indegree becomes zero. Return the number of layers. A neighbor helper
keeps boundary handling in one place. The matrix itself remains unchanged.

### Value-ordered path DP

Sort cell records by height. A cell starts with path length one and extends the longest path
ending at any strictly smaller neighbor, whose record has already been processed.

## Why it works

### Topological indegree layers

Strictly increasing edges exclude cycles. A source cell has longest incoming
path length one. Any other cell is released only after every smaller
neighbor has been removed, so its layer is one greater than the latest
predecessor layer. This is exactly the longest-path recurrence on a DAG.
Consequently the final layer number equals the longest path over all cells.

### Value-ordered path DP

Every increasing path into a cell ends at a smaller neighbor. Value order is a topological
order of all increasing edges, so taking the maximum predecessor length computes the exact
DAG longest-path recurrence.

## Walkthrough

For [[1,2],[4,3]], the only initial source is 1. The layers contain 1,
then 2, then 3, then 4. The path follows the square's perimeter and has
length 4. Equal neighboring values would create no edge.

## Cost and pitfalls

For the default Topological indegree layers approach:

O(rows*columns) time and space; each cell has at most four edges. Input
is unchanged. Processing the entire current layer before the next is essential.
Iteration handles paths of tens of thousands of cells without Python's
recursion-depth limit. Ordinary BFS distance finds shortest paths instead.

Topological indegree layers: O(R*C) time; O(R*C) space.
Value-ordered path DP: O(R*C log(R*C)) time; O(R*C) space.
Sorting allocates cell tuples and adds a logarithmic factor. Equal values never extend each
other. Both variants avoid recursion and preserve the matrix.
"""

from collections import deque


class Solution:
    """Approach: Topological indegree layers
    Time: O(R*C)
    Space: O(R*C)
    """

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        rows, columns = len(matrix), len(matrix[0])

        def neighbors(row: int, column: int):
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                other_row, other_column = row + dr, column + dc
                if 0 <= other_row < rows and 0 <= other_column < columns:
                    yield other_row, other_column

        indegree = [[0] * columns for _ in range(rows)]
        queue = deque()
        for row in range(rows):
            for column in range(columns):
                indegree[row][column] = sum(
                    matrix[nr][nc] < matrix[row][column] for nr, nc in neighbors(row, column)
                )
                if indegree[row][column] == 0:
                    queue.append((row, column))
        layers = 0
        while queue:
            layers += 1
            for _ in range(len(queue)):
                row, column = queue.popleft()
                for nr, nc in neighbors(row, column):
                    if matrix[nr][nc] > matrix[row][column]:
                        indegree[nr][nc] -= 1
                        if indegree[nr][nc] == 0:
                            queue.append((nr, nc))
        return layers


class SortedSolution:
    """Approach: Value-ordered path DP
    Time: O(R*C log(R*C))
    Space: O(R*C)
    """

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        rows, columns = len(matrix), len(matrix[0])
        cells = sorted((matrix[r][c], r, c) for r in range(rows) for c in range(columns))
        best = [[1] * columns for _ in range(rows)]
        answer = 1
        for value, row, column in cells:
            for nr, nc in (
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ):
                if 0 <= nr < rows and 0 <= nc < columns and matrix[nr][nc] < value:
                    best[row][column] = max(best[row][column], best[nr][nc] + 1)
            answer = max(answer, best[row][column])
        return answer
