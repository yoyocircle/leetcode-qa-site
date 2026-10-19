"""## Task

For every binary grid cell, return its shortest orthogonal distance to any zero; at least
one zero exists.

## Hints

1. All zero cells are simultaneous BFS sources.
2. Two opposite sweeps cover the four predecessor directions.

## Approach

### Multi-source zero BFS

Initialize zero distances and enqueue every zero. First discovery of a one assigns its
neighbor distance plus one.

### Forward and backward distance sweeps

Create a separate distance matrix. Relax top/left neighbors in a forward scan, then
bottom/right in a backward scan.

## Why it works

### Multi-source zero BFS

BFS processes increasing distance from the full source set. Every shortest path reaches a
predecessor one step nearer a zero, so first discovery is globally minimal.

### Forward and backward distance sweeps

Without obstacles, shortest distance is Manhattan distance to some zero. For any zero/cell
relative position, a shortest monotone route has a forward segment followed by a backward
segment in these scan orders. The two sweeps therefore propagate every needed minimum.

## Walkthrough

For [[0,1,1]], distances are [[0,1,2]].

## Cost and pitfalls

Multi-source zero BFS: O(R*C) time; O(R*C) space.
Forward and backward distance sweeps: O(R*C) time; O(R*C) space.

Both return a new matrix and preserve mat. The sweep argument relies on an obstacle-free
grid; it does not generalize unchanged to maze walls. Output storage dominates both bounds.
"""


class Solution:
    """Approach: Multi-source zero BFS
    Time: O(R*C)
    Space: O(R*C)
    """

    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        from collections import deque

        rows, columns = len(mat), len(mat[0])
        distance = [[-1] * columns for _ in range(rows)]
        queue = deque()
        for r in range(rows):
            for c in range(columns):
                if mat[r][c] == 0:
                    distance[r][c] = 0
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < columns and distance[nr][nc] < 0:
                    distance[nr][nc] = distance[r][c] + 1
                    queue.append((nr, nc))
        return distance


class SweepSolution:
    """Approach: Forward and backward distance sweeps
    Time: O(R*C)
    Space: O(R*C)
    """

    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        rows, columns = len(mat), len(mat[0])
        distance = [[0 if value == 0 else rows + columns for value in row] for row in mat]
        for r in range(rows):
            for c in range(columns):
                if r:
                    distance[r][c] = min(distance[r][c], distance[r - 1][c] + 1)
                if c:
                    distance[r][c] = min(distance[r][c], distance[r][c - 1] + 1)
        for r in range(rows - 1, -1, -1):
            for c in range(columns - 1, -1, -1):
                if r + 1 < rows:
                    distance[r][c] = min(distance[r][c], distance[r + 1][c] + 1)
                if c + 1 < columns:
                    distance[r][c] = min(distance[r][c], distance[r][c + 1] + 1)
        return distance
