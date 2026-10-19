"""## Task

Return every bridge of a connected undirected network: an edge whose removal disconnects the
graph.

## Hints

1. For each DFS subtree, find its earliest reachable ancestor through a non-parent edge.
2. A tree edge is a bridge exactly when the child cannot reach its parent or an earlier
ancestor.

## Approach

### Iterative Tarjan low-link DFS

Retain discovery times, low-link values, and explicit DFS child iterators. On child
completion, propagate its low value and report the parent edge when it exceeds the parent
discovery time.

### Remove each edge and test endpoint reachability

For each edge index, traverse the original adjacency graph while ignoring that edge, then
test whether its endpoints still connect.

## Why it works

### Iterative Tarjan low-link DFS

Low-link is the earliest ancestor reachable from a subtree using downward tree edges and at
most one back edge. If it cannot reach the parent or above, removing the parent edge
separates the subtree; otherwise a bypass cycle preserves connectivity.

### Remove each edge and test endpoint reachability

Removing one edge disconnects its component exactly when no alternate path connects its
endpoints. The reachability test is therefore the bridge definition applied directly.

## Walkthrough

In a triangle 0-1-2-0 with an extra edge 1-3, only [1,3] is critical.

## Cost and pitfalls

Iterative Tarjan low-link DFS: O(V+E) time; O(V+E) space.
Remove each edge and test endpoint reachability: O(E*(V+E)) time; O(V+E) space.

Inputs remain unchanged. The removal baseline is explanatory and will time out at the
100000-vertex scale; use the linear default. Both use explicit stacks, so long chains do not
overflow Python recursion.
"""


class Solution:
    """Approach: Iterative Tarjan low-link DFS
    Time: O(V+E)
    Space: O(V+E)
    """

    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        graph = [[] for _ in range(n)]
        for edge, (a, b) in enumerate(connections):
            graph[a].append((b, edge))
            graph[b].append((a, edge))
        discovery, low = [-1] * n, [0] * n
        bridges = []
        clock = 0
        for start in range(n):
            if discovery[start] >= 0:
                continue
            discovery[start] = low[start] = clock
            clock += 1
            stack = [(start, -1, iter(graph[start]))]
            while stack:
                node, parent_edge, neighbors = stack[-1]
                following = next(neighbors, None)
                if following is None:
                    stack.pop()
                    if stack:
                        parent = stack[-1][0]
                        if low[node] > discovery[parent]:
                            bridges.append([parent, node])
                        low[parent] = min(low[parent], low[node])
                    continue
                other, edge = following
                if edge == parent_edge:
                    continue
                if discovery[other] < 0:
                    discovery[other] = low[other] = clock
                    clock += 1
                    stack.append((other, edge, iter(graph[other])))
                else:
                    low[node] = min(low[node], discovery[other])
        return bridges


class RemovalSolution:
    """Approach: Remove each edge and test endpoint reachability
    Time: O(E*(V+E))
    Space: O(V+E)
    """

    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        graph = [[] for _ in range(n)]
        for edge, (a, b) in enumerate(connections):
            graph[a].append((b, edge))
            graph[b].append((a, edge))
        answer = []
        for removed, (start, end) in enumerate(connections):
            stack, seen = [start], {start}
            while stack:
                node = stack.pop()
                for other, edge in graph[node]:
                    if edge != removed and other not in seen:
                        seen.add(other)
                        stack.append(other)
            if end not in seen:
                answer.append([start, end])
        return answer
