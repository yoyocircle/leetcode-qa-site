"""## Task

Remove as many typed undirected edges as possible while keeping every vertex reachable for
both Alice and Bob; type 3 is shared, type 1 Alice-only, type 2 Bob-only.

## Hints

1. Shared edges should connect components before private edges are considered.
2. Contract all shared components; each player then needs a spanning tree among them.

## Approach

### Shared-first twin union-find forests

Build a maximal shared forest, clone its union-find state for each player, and add only
private edges that join distinct components. Reject if either resulting graph stays
disconnected.

### Shared-component contraction and graph connectivity

Flood-fill shared edges into components. Build a component graph of private edges for each
player and test connectivity, then count the necessary shared and private spanning-forest
edges.

## Why it works

### Shared-first twin union-find forests

A shared forest with c components uses n-c edges and benefits both players. Each player
needs at least c-1 additional private edges. Successful unions attain these lower bounds, so
the number retained is minimum.

### Shared-component contraction and graph connectivity

Each shared component has an n_i-1-edge spanning tree, and the contracted private graph has
a c-1-edge spanning tree exactly when connected. The total n-c+2(c-1) is attainable and is
also a lower bound.

## Walkthrough

If a shared tree already spans n vertices, every private edge is removable.

## Cost and pitfalls

Shared-first twin union-find forests: O((V+E)*alpha(V)) time; O(V) space.
Shared-component contraction and graph connectivity: O(V+E) time; O(V+E) space.

Inputs remain unchanged. Twin union-find copies O(V) parent/size arrays for independent
players. Processing private edges first can miss the saving from one edge serving both
players.
"""


class Solution:
    """Approach: Shared-first twin union-find forests
    Time: O((V+E)*alpha(V))
    Space: O(V)
    """

    def maxNumEdgesToRemove(self, n: int, edges: list[list[int]]) -> int:
        def find(parent, node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(parent, size, a, b):
            a, b = find(parent, a), find(parent, b)
            if a == b:
                return False
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            return True

        shared, sizes = list(range(n)), [1] * n
        used = 0
        for kind, a, b in edges:
            if kind == 3:
                used += union(shared, sizes, a - 1, b - 1)
        for kind in (1, 2):
            parent, size = shared.copy(), sizes.copy()
            for edge_type, a, b in edges:
                if edge_type == kind:
                    used += union(parent, size, a - 1, b - 1)
            if any(find(parent, node) != find(parent, 0) for node in range(n)):
                return -1
        return len(edges) - used


class ContractionSolution:
    """Approach: Shared-component contraction and graph connectivity
    Time: O(V+E)
    Space: O(V+E)
    """

    def maxNumEdgesToRemove(self, n: int, edges: list[list[int]]) -> int:
        shared = [[] for _ in range(n)]
        for kind, a, b in edges:
            if kind == 3:
                shared[a - 1].append(b - 1)
                shared[b - 1].append(a - 1)
        component = [-1] * n
        count = 0
        for start in range(n):
            if component[start] >= 0:
                continue
            component[start] = count
            stack = [start]
            while stack:
                node = stack.pop()
                for other in shared[node]:
                    if component[other] < 0:
                        component[other] = count
                        stack.append(other)
            count += 1
        for kind in (1, 2):
            graph = [[] for _ in range(count)]
            for edge_type, a, b in edges:
                if edge_type == kind:
                    x, y = component[a - 1], component[b - 1]
                    graph[x].append(y)
                    graph[y].append(x)
            seen, stack = {0}, [0]
            while stack:
                node = stack.pop()
                for other in graph[node]:
                    if other not in seen:
                        seen.add(other)
                        stack.append(other)
            if len(seen) != count:
                return -1
        return len(edges) - ((n - count) + 2 * (count - 1))
