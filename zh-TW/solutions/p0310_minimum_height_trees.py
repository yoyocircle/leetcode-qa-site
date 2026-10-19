"""## Task

Return all roots minimizing the height of a given undirected tree.

## Hints

1. Tree centers remain after repeatedly trimming all current leaves.
2. The midpoint or two midpoints of a diameter are the centers.

## Approach

### Trim simultaneous leaf layers

Queue every degree-one vertex and remove complete leaf layers until at most two vertices remain.

### Find a diameter and choose its midpoint

A BFS from any vertex finds a diameter endpoint; a second BFS finds the other and records
parents. Reconstruct that path and return its middle vertices.

## Why it works

### Trim simultaneous leaf layers

Removing all leaves shortens every longest outward route equally without changing the
centers. Repeated removal therefore leaves exactly the one or two minimum-eccentricity
roots.

### Find a diameter and choose its midpoint

A tree center minimizes maximum distance to diameter endpoints, forcing it to a midpoint.
Other branches cannot extend beyond the diameter, so those midpoint heights are globally
minimal.

## Walkthrough

For the path 0-1-2-3, roots 1 and 2 both minimize height.

## Cost and pitfalls

Trim simultaneous leaf layers: O(V) time; O(V) space.
Find a diameter and choose its midpoint: O(V) time; O(V) space.

Inputs remain unchanged. The final path slice allocates at most two output elements. Tree
connectivity and acyclicity are required; these methods are not general-graph center
algorithms.
"""


class Solution:
    """Approach: Trim simultaneous leaf layers
    Time: O(V)
    Space: O(V)
    """

    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        from collections import deque

        if n == 1:
            return [0]
        graph = [[] for _ in range(n)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        degree = [len(neighbors) for neighbors in graph]
        queue = deque(i for i in range(n) if degree[i] == 1)
        remaining = n
        while remaining > 2:
            remaining -= len(queue)
            for _ in range(len(queue)):
                node = queue.popleft()
                for other in graph[node]:
                    degree[other] -= 1
                    if degree[other] == 1:
                        queue.append(other)
        return list(queue)


class DiameterSolution:
    """Approach: Find a diameter and choose its midpoint
    Time: O(V)
    Space: O(V)
    """

    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        from collections import deque

        graph = [[] for _ in range(n)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        def farthest(start):
            parent = [-1] * n
            parent[start] = start
            queue = deque([start])
            node = start
            while queue:
                node = queue.popleft()
                for other in graph[node]:
                    if parent[other] < 0:
                        parent[other] = node
                        queue.append(other)
            return node, parent

        first, _ = farthest(0)
        last, parent = farthest(first)
        path = [last]
        while path[-1] != first:
            path.append(parent[path[-1]])
        middle = len(path) // 2
        return path[middle : middle + 1] if len(path) % 2 else path[middle - 1 : middle + 1]
