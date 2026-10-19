"""## Task

Connect all planar points at minimum total Manhattan edge cost.

## Hints

1. This is a minimum spanning tree of the complete weighted graph.
2. Dense Prim avoids materializing every pairwise edge.

## Approach

### Dense Prim with on-demand distances

Maintain each unchosen point's cheapest edge into the chosen tree. Select its minimum by
scanning and update distances on demand.

### All-edge Kruskal

Materialize every unordered point pair with its Manhattan weight, sort edges, and accept
each edge joining different components.

## Why it works

### Dense Prim with on-demand distances

The selected edge is the cheapest edge across the current tree cut, so the MST cut property
makes it safe. Repeating until all points are included yields an MST.

### All-edge Kruskal

The next accepted edge is a cheapest edge crossing some remaining component cut, so it is
safe by the MST cut property. Rejecting cycles leaves a spanning tree with minimum cost.

## Walkthrough

Points [0,0], [2,0], and [2,3] connect with costs 2 and 3, totaling 5.

## Cost and pitfalls

Dense Prim with on-demand distances: O(n^2) time; O(n) space.
All-edge Kruskal: O(n^2 log n) time; O(n^2) space.

Both preserve points. Kruskal explicitly allocates O(n^2) tuples and can consume substantial
memory at the largest input; dense Prim is the recommended default.
"""


class Solution:
    """Approach: Dense Prim with on-demand distances
    Time: O(n^2)
    Space: O(n)
    """

    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        distance, used = [float("inf")] * n, [False] * n
        distance[0] = 0
        total = 0
        for _ in range(n):
            node = min((i for i in range(n) if not used[i]), key=lambda i: distance[i])
            total += distance[node]
            used[node] = True
            x, y = points[node]
            for other, (ox, oy) in enumerate(points):
                if not used[other]:
                    distance[other] = min(distance[other], abs(x - ox) + abs(y - oy))
        return total


class KruskalSolution:
    """Approach: All-edge Kruskal
    Time: O(n^2 log n)
    Space: O(n^2)
    """

    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        edges = sorted(
            (abs(a[0] - b[0]) + abs(a[1] - b[1]), i, j)
            for i, a in enumerate(points)
            for j, b in enumerate(points)
            if i < j
        )
        parent, size = list(range(len(points))), [1] * len(points)

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        total, remaining = 0, len(points) - 1
        for cost, a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            total += cost
            remaining -= 1
            if remaining == 0:
                break
        return total
