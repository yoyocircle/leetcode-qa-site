"""## Task

Each minute, rotten oranges infect fresh oranges in their four neighboring
cells. Return the time until no fresh oranges remain, or -1 if some cannot rot.
An input with no fresh oranges needs zero minutes.

## Hints

1. Infection spreads from every initially rotten orange at the same time.
2. A breadth-first search layer represents one minute of simultaneous spread.

## Approach

### Multi-source infection BFS

Count fresh oranges and queue all rotten cells. A set records cells already
rotten or scheduled to rot. Process a fixed layer, enqueue newly infected
neighbors, and decrease the fresh count. Advance time after the layer. Stop
when no fresh oranges or queued cells remain.

### Synchronous copied-grid rounds

Copy the grid and repeatedly scan for fresh cells adjacent to current rotten cells. Record
all changes, then apply them together after the scan.

## Why it works

### Multi-source infection BFS

The initial queue contains the minute-zero sources. A layer of cells infected
at minute t discovers the newly reachable cells at minute t+1. Immediate marking
prevents duplicate counts. Breadth-first layers give each orange its earliest
infection time; fresh cells remaining after exhaustion have no path from a source.

### Synchronous copied-grid rounds

A scan reads only the preceding minute, so newly rotten cells cannot infect another cell too
early. If fresh cells remain without changes, the process has reached a fixed point and they
are unreachable.

## Walkthrough

For [[2,1,1],[0,0,1]], the two top-row fresh oranges rot at minutes 1 and 2.
The lower-right orange then rots at minute 3, which is the answer.

## Cost and pitfalls

For the default Multi-source infection BFS approach:

O(rows * cols) time and auxiliary space. The grid is unchanged; infection state
lives in the set. Counting each source separately would lose simultaneous
spread. Do not increment time while processing individual oranges within a layer.

Multi-source infection BFS: O(R*C) time; O(R*C) space.
Synchronous copied-grid rounds: O((R*C)^2) time; O(R*C) space.
The simulation is a simple baseline; repeated full scans are quadratic in cell count and may
be slow on generalized large grids. Changes are staged to preserve simultaneous spread, and
input stays unchanged.
"""

from collections import deque


class Solution:
    """Approach: Multi-source infection BFS
    Time: O(R*C)
    Space: O(R*C)
    """

    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        rotten = set()
        fresh = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    rotten.add((row, col))
                elif grid[row][col] == 1:
                    fresh += 1
        queue = deque(rotten)
        minutes = 0
        while queue and fresh:
            for _ in range(len(queue)):
                row, col = queue.popleft()
                for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == 1
                        and (nr, nc) not in rotten
                    ):
                        rotten.add((nr, nc))
                        queue.append((nr, nc))
                        fresh -= 1
            minutes += 1
        return -1 if fresh else minutes


class SimulationSolution:
    """Approach: Synchronous copied-grid rounds
    Time: O((R*C)^2)
    Space: O(R*C)
    """

    def orangesRotting(self, grid: list[list[int]]) -> int:
        state = [row.copy() for row in grid]
        rows, columns = len(state), len(state[0])
        minutes = 0
        while True:
            changes = []
            fresh = 0
            for r in range(rows):
                for c in range(columns):
                    if state[r][c] != 1:
                        continue
                    fresh += 1
                    if any(
                        0 <= nr < rows and 0 <= nc < columns and state[nr][nc] == 2
                        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                    ):
                        changes.append((r, c))
            if not fresh:
                return minutes
            if not changes:
                return -1
            for r, c in changes:
                state[r][c] = 2
            minutes += 1
