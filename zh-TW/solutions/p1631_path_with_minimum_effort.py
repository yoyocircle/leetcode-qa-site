"""## Task

Find a grid path minimizing its largest absolute height difference on any step.

## Hints

1. Relax paths using max(current effort, edge difference), not addition.
2. Alternatively add edges by weight until the two endpoints become connected.

## Approach

### Minimax Dijkstra

Use a heap keyed by the best maximum step cost. Extending a path takes the maximum of its
prior effort and the new edge.

### Threshold connectivity by sorted edges

Sort orthogonal edges by absolute difference. Union endpoints in that order, stopping as
soon as start and destination connect.

## Why it works

### Minimax Dijkstra

Path extension cannot decrease effort, giving the same minimum-label finalization argument
as Dijkstra. Relaxing all neighbors finds each optimal bottleneck.

### Threshold connectivity by sorted edges

After processing threshold t, components contain exactly paths whose every edge costs at
most t. The first connecting threshold is therefore the smallest possible maximum edge cost.

## Walkthrough

For [[1,10],[2,3]], down then right has effort max(1,1)=1.

## Cost and pitfalls

Minimax Dijkstra: O(R*C log(R*C)) time; O(R*C) space.
Threshold connectivity by sorted edges: O(R*C log(R*C)) time; O(R*C) space.

Inputs remain unchanged. A single cell needs zero effort. Kruskal stores and sorts all grid
edges; Dijkstra can stop without examining every cell. Neither minimizes the sum of step
differences.
"""


class Solution:
    """Approach: Minimax Dijkstra
    Time: O(R*C log(R*C))
    Space: O(R*C)
    """

    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        from heapq import heappop, heappush

        rows, columns = len(heights), len(heights[0])
        best = {(0, 0): 0}
        heap = [(0, 0, 0)]
        while heap:
            effort, r, c = heappop(heap)
            if best[(r, c)] != effort:
                continue
            if (r, c) == (rows - 1, columns - 1):
                return effort
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < columns:
                    candidate = max(effort, abs(heights[r][c] - heights[nr][nc]))
                    if candidate < best.get((nr, nc), float("inf")):
                        best[(nr, nc)] = candidate
                        heappush(heap, (candidate, nr, nc))
        return 0


class KruskalSolution:
    """Approach: Threshold connectivity by sorted edges
    Time: O(R*C log(R*C))
    Space: O(R*C)
    """

    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        rows, columns = len(heights), len(heights[0])
        parent, size = list(range(rows * columns)), [1] * (rows * columns)
        edges = []
        for r in range(rows):
            for c in range(columns):
                for nr, nc in ((r + 1, c), (r, c + 1)):
                    if nr < rows and nc < columns:
                        edges.append(
                            (
                                abs(heights[r][c] - heights[nr][nc]),
                                r * columns + c,
                                nr * columns + nc,
                            )
                        )

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for cost, a, b in sorted(edges):
            ra, rb = find(a), find(b)
            if ra != rb:
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
            if find(0) == find(rows * columns - 1):
                return cost
        return 0
