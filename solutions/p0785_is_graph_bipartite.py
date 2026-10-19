"""## Task

Decide whether an undirected graph can be split into two groups so every edge crosses groups.
Disconnected components and isolated vertices are allowed.

## Hints

1. Assign a vertex the opposite color of every neighbor.
2. A disjoint-set model can represent each vertex and its required opposite.

## Approach

### Component-wise two-color BFS

Start an uncolored component at color zero and BFS its edges. Assign unseen neighbors the
opposite color; reject any edge joining equal colors.

### Union-find with opposite copies

Represent vertex u and its opposite as u and u+V. Each edge joins u with opposite(v) and
opposite(u) with v. Reject when any vertex becomes equivalent to its own opposite.

## Why it works

### Component-wise two-color BFS

Every traversed edge enforces exactly the bipartition constraint. A conflict proves an
inconsistent parity cycle; without conflicts the resulting colors explicitly provide a valid
partition.

### Union-find with opposite copies

The unions encode every edge's inequality as equivalence to an opposite. A vertex equaling its
opposite is precisely a contradiction; otherwise each equivalence component can be assigned
consistently opposite its paired component.

## Walkthrough

A triangle 0-1-2-0 forces the third edge to join equal colors and fails. A four-cycle alternates
colors and succeeds.

## Cost and pitfalls

Component-wise two-color BFS: O(V+E) time; O(V) space.
Union-find with opposite copies: O((V+E)*alpha(V)) time; O(V) space.
The graph is unchanged. Start every disconnected component, not only vertex zero. Union-find
uses two copies per vertex; alpha denotes inverse Ackermann. Iteration avoids deep recursive
traversal.
"""

from collections import deque


class Solution:
    """Approach: Component-wise two-color BFS
    Time: O(V+E)
    Space: O(V)
    """

    def isBipartite(self, graph: list[list[int]]) -> bool:
        colors = [-1] * len(graph)
        for start in range(len(graph)):
            if colors[start] != -1:
                continue
            colors[start] = 0
            queue = deque([start])
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if colors[neighbor] == -1:
                        colors[neighbor] = 1 - colors[node]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[node]:
                        return False
        return True


class OppositeSetsSolution:
    """Approach: Union-find with opposite copies
    Time: O((V+E)*alpha(V))
    Space: O(V)
    """

    def isBipartite(self, graph: list[list[int]]) -> bool:
        n = len(graph)
        parent = list(range(2 * n))
        size = [1] * (2 * n)

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(left, right):
            left, right = find(left), find(right)
            if left == right:
                return
            if size[left] < size[right]:
                left, right = right, left
            parent[right] = left
            size[left] += size[right]

        for node, neighbors in enumerate(graph):
            for neighbor in neighbors:
                union(node, neighbor + n)
                union(node + n, neighbor)
        return all(find(node) != find(node + n) for node in range(n))
