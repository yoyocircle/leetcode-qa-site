"""## Task

Count connected groups of land cells in a rectangular grid of "1" and "0".
Land connects through shared sides; diagonal contact does not join islands.

## Hints

1. Once you find unvisited land, explore everything connected to it.
2. Mark cells when adding them to the worklist so multiple neighbors cannot add them again.

## Approach

### Iterative land-component DFS

Scan the grid. Every unvisited land cell starts one new island and an iterative
depth-first traversal. A stack holds discovered cells, and a visited set records
them. Add only in-bounds, unvisited land neighbors. Keep the grid unchanged so
the original map remains available after counting.

### Union neighboring land cells

Start with one component per land cell. Scan only upper and left land edges, merging
endpoint roots with size-weighted union and path compression.

## Why it works

### Iterative land-component DFS

The traversal reaches precisely the land component containing its starting
cell: each step crosses a legal land edge, and every such neighbor is explored.
All cells of that component become visited. The outer scan therefore starts
exactly once per component, so its count equals the number of islands.

### Union neighboring land cells

Each merge reduces component count exactly when two previously separate land groups connect.
All undirected land edges are considered once, so final sets are exactly the islands.

## Walkthrough

For [["1","0","1"],["1","0","0"]], the upper-left start visits both
left-column land cells. The upper-right cell starts another traversal. Return 2.

## Cost and pitfalls

For the default Iterative land-component DFS approach:

O(rows * cols) time and auxiliary space. Each cell is scanned once and each
land cell enters the stack once. The grid is unchanged. Diagonal movement would
merge separate islands. Iteration also handles a long connected strip without
depending on Python's recursion limit.

Iterative land-component DFS: O(R*C) time; O(R*C) space.
Union neighboring land cells: O(R*C*alpha(R*C)) time; O(R*C) space.
Neither variant mutates the grid. Union-find stores arrays for water cells too, but only
land contributes to the component count; alpha is inverse Ackermann.
"""


class Solution:
    """Approach: Iterative land-component DFS
    Time: O(R*C)
    Space: O(R*C)
    """

    def numIslands(self, grid: list[list[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()
        count = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] != "1" or (row, col) in visited:
                    continue
                count += 1
                visited.add((row, col))
                stack = [(row, col)]
                while stack:
                    r, c = stack.pop()
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and grid[nr][nc] == "1"
                            and (nr, nc) not in visited
                        ):
                            visited.add((nr, nc))
                            stack.append((nr, nc))
        return count


class UnionFindSolution:
    """Approach: Union neighboring land cells
    Time: O(R*C*alpha(R*C))
    Space: O(R*C)
    """

    def numIslands(self, grid: list[list[str]]) -> int:
        rows, columns = len(grid), len(grid[0])
        parent = list(range(rows * columns))
        size = [1] * len(parent)
        count = sum(cell == "1" for row in grid for cell in row)

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for row in range(rows):
            for column in range(columns):
                if grid[row][column] != "1":
                    continue
                for nr, nc in ((row - 1, column), (row, column - 1)):
                    if nr >= 0 and nc >= 0 and grid[nr][nc] == "1":
                        a, b = find(row * columns + column), find(nr * columns + nc)
                        if a != b:
                            if size[a] < size[b]:
                                a, b = b, a
                            parent[b] = a
                            size[a] += size[b]
                            count -= 1
        return count
