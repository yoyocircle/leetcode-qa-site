"""## Task

Computers are connected by undirected network cables. One operation can move an existing cable
to connect a different pair. Return the minimum operations to connect all computers, or -1 if
impossible.

## Hints

1. A connected graph on n vertices needs at least n-1 cables.
2. If enough cables exist, only the current number of components matters.

## Approach

### Disjoint-set component counting

Reject fewer than n-1 cables. Union endpoints with size weighting and path compression;
decrement component count on every successful merge. Return components-1.

### Iterative component traversal

Build undirected adjacency, count connected components using explicit DFS, and apply the same
cable-supply condition.

## Why it works

### Disjoint-set component counting

A forest spanning all current components uses V-components cables, leaving enough redundant
cables for components-1 joins exactly when E>=V-1. Each join reduces components by at most one,
so this count is both necessary and sufficient.

### Iterative component traversal

Each DFS discovers exactly one existing component. After counting them, reconnecting one
redundant cable between components joins two without breaking the source component, achieving
the lower bound.

## Walkthrough

For n=4 and cables [[0,1],[0,2],[1,2]], the triangle supplies one redundant cable to attach
computer 3, so return 1.

## Cost and pitfalls

Disjoint-set component counting: O((V+E)*alpha(V)) time; O(V) space.
Iterative component traversal: O(V+E) time; O(V+E) space.
Connections are unchanged. Isolated computers count as components. A single computer requires
zero moves. alpha is inverse Ackermann; the traversal variant stores all adjacency edges rather
than just union-find arrays.
"""


class Solution:
    """Approach: Disjoint-set component counting
    Time: O((V+E)*alpha(V))
    Space: O(V)
    """

    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        parent = list(range(n))
        size = [1] * n
        components = n

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for left, right in connections:
            left, right = find(left), find(right)
            if left != right:
                if size[left] < size[right]:
                    left, right = right, left
                parent[right] = left
                size[left] += size[right]
                components -= 1
        return components - 1


class TraversalSolution:
    """Approach: Iterative component traversal
    Time: O(V+E)
    Space: O(V+E)
    """

    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        adjacency = [[] for _ in range(n)]
        for left, right in connections:
            adjacency[left].append(right)
            adjacency[right].append(left)
        seen = set()
        components = 0
        for start in range(n):
            if start in seen:
                continue
            components += 1
            seen.add(start)
            stack = [start]
            while stack:
                node = stack.pop()
                for neighbor in adjacency[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
        return components - 1
