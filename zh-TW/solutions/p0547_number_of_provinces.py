"""## Task

Count connected provinces in a symmetric city adjacency matrix.

## Hints

1. Each unseen city starts one connected component.
2. Each undirected adjacency can instead merge two disjoint sets.

## Approach

### Iterative adjacency-matrix DFS

Visit each unseen city and traverse all connected matrix neighbors, counting one new
province per traversal start.

### Union the upper matrix triangle

Begin with n components and union every off-diagonal connection once, using matrix symmetry
to skip the lower half.

## Why it works

### Iterative adjacency-matrix DFS

Each traversal marks exactly its connected component, so no later start belongs to that
province and every province starts once.

### Union the upper matrix triangle

Each successful union reduces the number of connected components by one; redundant
connections and diagonal self-connections do not alter it.

## Walkthrough

For [[1,1,0],[1,1,0],[0,0,1]], cities 0 and 1 form one province and city 2 another.

## Cost and pitfalls

Iterative adjacency-matrix DFS: O(n^2) time; O(n) space.
Union the upper matrix triangle: O(n^2*alpha(n)) time; O(n) space.

Both preserve the matrix. Reading adjacency rows costs quadratic time even for a sparse
represented graph; do not claim adjacency-list O(V+E) scanning for this input
representation.
"""


class Solution:
    """Approach: Iterative adjacency-matrix DFS
    Time: O(n^2)
    Space: O(n)
    """

    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        seen = set()
        count = 0
        for start in range(len(isConnected)):
            if start in seen:
                continue
            count += 1
            seen.add(start)
            stack = [start]
            while stack:
                node = stack.pop()
                for other, connected in enumerate(isConnected[node]):
                    if connected and other not in seen:
                        seen.add(other)
                        stack.append(other)
        return count


class UnionFindSolution:
    """Approach: Union the upper matrix triangle
    Time: O(n^2*alpha(n))
    Space: O(n)
    """

    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        parent, size = list(range(n)), [1] * n

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        count = n
        for a in range(n):
            for b in range(a + 1, n):
                if isConnected[a][b]:
                    ra, rb = find(a), find(b)
                    if ra != rb:
                        if size[ra] < size[rb]:
                            ra, rb = rb, ra
                        parent[rb] = ra
                        size[ra] += size[rb]
                        count -= 1
        return count
