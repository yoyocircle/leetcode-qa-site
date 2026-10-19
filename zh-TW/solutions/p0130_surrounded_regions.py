"""## Task

Replace every "O" region disconnected from the board boundary with "X", modifying the board
in place.

## Hints

1. Only boundary-connected O cells survive.
2. A virtual exterior vertex can join all boundary O cells.

## Approach

### Boundary flood-fill

Traverse O cells outward from every boundary O. Change only O cells not in the resulting
safe set.

### Union-find with an exterior sentinel

Union adjacent O cells and union boundary O cells with a virtual exterior node. Use
size-weighted unions and iterative path compression; flip cells whose root differs from the
exterior root.

## Why it works

### Boundary flood-fill

An O region survives exactly when it has an O path to a boundary. Flood-fill finds precisely
these paths, so the complement consists exactly of surrounded regions.

### Union-find with an exterior sentinel

A component joins the exterior exactly when some member touches the boundary. Union
connectivity therefore gives the same survival criterion without exploring each region from
a seed.

## Walkthrough

For a 3x3 board of X around a central O, the center becomes X; a boundary O stays O.

## Cost and pitfalls

Boundary flood-fill: O(R*C) time; O(R*C) space.
Union-find with an exterior sentinel: O(R*C*alpha(R*C)) time; O(R*C) space.

Both intentionally mutate board and return None. The sentinel is an auxiliary node, not an
extra board cell. Single-row and single-column boards cannot contain surrounded regions.
"""


class Solution:
    """Approach: Boundary flood-fill
    Time: O(R*C)
    Space: O(R*C)
    """

    def solve(self, board: list[list[str]]) -> None:
        rows, columns = len(board), len(board[0])
        safe = set()
        stack = [
            (r, c)
            for r in range(rows)
            for c in range(columns)
            if (r in (0, rows - 1) or c in (0, columns - 1)) and board[r][c] == "O"
        ]
        while stack:
            r, c = stack.pop()
            if (r, c) in safe:
                continue
            safe.add((r, c))
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (
                    0 <= nr < rows
                    and 0 <= nc < columns
                    and board[nr][nc] == "O"
                    and (nr, nc) not in safe
                ):
                    stack.append((nr, nc))
        for r in range(rows):
            for c in range(columns):
                if board[r][c] == "O" and (r, c) not in safe:
                    board[r][c] = "X"


class UnionFindSolution:
    """Approach: Union-find with an exterior sentinel
    Time: O(R*C*alpha(R*C))
    Space: O(R*C)
    """

    def solve(self, board: list[list[str]]) -> None:
        rows, columns = len(board), len(board[0])
        outside = rows * columns
        parent = list(range(outside + 1))
        size = [1] * len(parent)

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(a, b):
            a, b = find(a), find(b)
            if a == b:
                return
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]

        for r in range(rows):
            for c in range(columns):
                if board[r][c] != "O":
                    continue
                current = r * columns + c
                if r in (0, rows - 1) or c in (0, columns - 1):
                    union(current, outside)
                for nr, nc in ((r - 1, c), (r, c - 1)):
                    if nr >= 0 and nc >= 0 and board[nr][nc] == "O":
                        union(current, nr * columns + nc)
        root = find(outside)
        for r in range(rows):
            for c in range(columns):
                if board[r][c] == "O" and find(r * columns + c) != root:
                    board[r][c] = "X"
