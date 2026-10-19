"""## Task

Return cells whose water can reach both oceans. The Pacific touches the top
and left edges; the Atlantic touches the bottom and right edges. Water moves
orthogonally to cells of equal or lower height.

## Hints

1. Searching downhill from every cell repeats much of the same work.
2. Reverse the direction: start at each ocean and move uphill or across equal heights.

## Approach

### Two reversed-flow DFS traversals

Seed two iterative traversals with the respective ocean boundaries. In reversed
flow, a neighbor is reachable when its height is at least the current height.
Each traversal records its reachable set. Return their intersection in row order.

### Fused ocean-label propagation

Use one queue carrying newly learned Pacific or Atlantic bits. Seed border cells, then
propagate each ocean bit to equal-or-higher neighbors; return cells with both bits.

## Why it works

### Two reversed-flow DFS traversals

Reversing edges turns a downhill path to an ocean into an uphill path from
that ocean. Each traversal thus finds exactly the cells that can drain to its
ocean. Membership in both sets means the cell has a path to each ocean;
these paths need not be the same.

### Fused ocean-label propagation

Reversed paths exactly represent downhill routes to an ocean. Each bit is propagated once
per cell, so the fixed point contains exactly reachable ocean labels; mask three means both
routes exist.

## Walkthrough

For [[1,2],[4,3]], reversed Pacific flow reaches all four cells through
1->2->3 and 1->4. Reversed Atlantic flow cannot move down to height 1.
The cells reaching both oceans are [0,1], [1,0], and [1,1].

## Cost and pitfalls

For the default Two reversed-flow DFS traversals approach:

O(rows * cols) time and auxiliary space, including the result. Heights are
unchanged. Reversed traversal must allow equal heights. Using the original
downhill comparison from the ocean would compute the wrong reachability set.

Two reversed-flow DFS traversals: O(R*C) time; O(R*C) space.
Fused ocean-label propagation: O(R*C) time; O(R*C) space.
The fused version stores one small mask grid rather than two coordinate sets. Both are
iterative and preserve heights. Equal-height edges must remain traversable.
"""


class Solution:
    """Approach: Two reversed-flow DFS traversals
    Time: O(R*C)
    Space: O(R*C)
    """

    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        rows, cols = len(heights), len(heights[0])

        def reach(starts):
            visited = set(starts)
            stack = list(visited)
            while stack:
                row, col = stack.pop()
                for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and heights[nr][nc] >= heights[row][col]
                        and (nr, nc) not in visited
                    ):
                        visited.add((nr, nc))
                        stack.append((nr, nc))
            return visited

        pacific = reach([(0, col) for col in range(cols)] + [(row, 0) for row in range(rows)])
        atlantic = reach(
            [(rows - 1, col) for col in range(cols)] + [(row, cols - 1) for row in range(rows)]
        )
        return [
            [row, col]
            for row in range(rows)
            for col in range(cols)
            if (row, col) in pacific and (row, col) in atlantic
        ]


class MaskSolution:
    """Approach: Fused ocean-label propagation
    Time: O(R*C)
    Space: O(R*C)
    """

    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        from collections import deque

        rows, columns = len(heights), len(heights[0])
        masks = [[0] * columns for _ in range(rows)]
        queue = deque()

        def add(row, column, bit):
            if not masks[row][column] & bit:
                masks[row][column] |= bit
                queue.append((row, column, bit))

        for row in range(rows):
            add(row, 0, 1)
            add(row, columns - 1, 2)
        for column in range(columns):
            add(0, column, 1)
            add(rows - 1, column, 2)
        while queue:
            row, column, bit = queue.popleft()
            for nr, nc in (
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ):
                if 0 <= nr < rows and 0 <= nc < columns and heights[nr][nc] >= heights[row][column]:
                    add(nr, nc, bit)
        return [[r, c] for r in range(rows) for c in range(columns) if masks[r][c] == 3]
