"""## Task

Return the greatest number of cells in any four-connected island of integer ones.

## Hints

1. Flood-fill each unvisited land component and count its cells.
2. Union-find component sizes give areas directly.

## Approach

### Iterative area flood-fill

Start a stack traversal at each unseen one, mark on discovery, and count popped cells. Keep
the largest finished component area.

### Size-weighted land unions

Assign each position a union-find slot and merge upper/left land neighbors. Maintain size
only at roots and update the maximum after each land cell.

## Why it works

### Iterative area flood-fill

Each traversal reaches exactly its starting component and counts each member once. Distinct
starts are disjoint components, so their maximum area is the answer.

### Size-weighted land unions

Root size starts at one per land singleton and sums exactly on merging disjoint components.
Considering every land adjacency produces precisely the islands and their cell counts.

## Walkthrough

For [[1,0,1],[1,0,0]], the largest island has two cells.

## Cost and pitfalls

Iterative area flood-fill: O(R*C) time; O(R*C) space.
Size-weighted land unions: O(R*C*alpha(R*C)) time; O(R*C) space.

Both preserve the input grid and avoid recursion depth limits. All-water input returns zero;
diagonal adjacency never joins land.
"""


class Solution:
    """Approach: Iterative area flood-fill
    Time: O(R*C)
    Space: O(R*C)
    """

    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        rows, columns = len(grid), len(grid[0])
        seen = set()
        answer = 0
        for r in range(rows):
            for c in range(columns):
                if not grid[r][c] or (r, c) in seen:
                    continue
                stack, area = [(r, c)], 0
                seen.add((r, c))
                while stack:
                    row, column = stack.pop()
                    area += 1
                    for nr, nc in (
                        (row - 1, column),
                        (row + 1, column),
                        (row, column - 1),
                        (row, column + 1),
                    ):
                        if (
                            0 <= nr < rows
                            and 0 <= nc < columns
                            and grid[nr][nc]
                            and (nr, nc) not in seen
                        ):
                            seen.add((nr, nc))
                            stack.append((nr, nc))
                answer = max(answer, area)
        return answer


class UnionFindSolution:
    """Approach: Size-weighted land unions
    Time: O(R*C*alpha(R*C))
    Space: O(R*C)
    """

    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        rows, columns = len(grid), len(grid[0])
        parent = list(range(rows * columns))
        size = [1] * len(parent)

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        answer = 0
        for r in range(rows):
            for c in range(columns):
                if not grid[r][c]:
                    continue
                root = find(r * columns + c)
                for nr, nc in ((r - 1, c), (r, c - 1)):
                    if nr >= 0 and nc >= 0 and grid[nr][nc]:
                        other = find(nr * columns + nc)
                        root = find(root)
                        if root != other:
                            if size[root] < size[other]:
                                root, other = other, root
                            parent[other] = root
                            size[root] += size[other]
                answer = max(answer, size[find(root)])
        return answer
