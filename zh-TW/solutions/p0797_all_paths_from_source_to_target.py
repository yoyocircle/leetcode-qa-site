"""## Task

Return every directed path from vertex zero to vertex n-1 in a directed acyclic graph. Paths
contain vertex identifiers in traversal order.

## Hints

1. Acyclicity guarantees every exploration terminates.
2. You can enumerate paths forward or combine already known suffix paths backward.

## Approach

### Path-local DAG backtracking

Append each next neighbor to a shared path, recurse, and undo. Copy the path when the target is
reached, then stop that branch.

### Topological suffix-path DP

Compute a topological order, then process it backward. Seed the target with its one-node suffix
and prepend each vertex to every suffix of its outgoing neighbors.

## Why it works

### Path-local DAG backtracking

Every directed source-to-target path has one neighbor-choice sequence. The search explores each
such sequence once; no visited set may suppress a vertex reached through another prefix.

### Topological suffix-path DP

All child suffix catalogs are complete before a parent is processed. A path from that parent
uniquely chooses its first edge and one target-reaching suffix, so the combination is exact.

## Walkthrough

For [[1,2],[3],[3],[]], output [0,1,3] and [0,2,3]. Both paths legitimately share vertex 3.

## Cost and pitfalls

Path-local DAG backtracking: O(V*2^V) loose bound time; O(V) auxiliary plus output space.
Topological suffix-path DP: O(V+E+total copied suffix lengths) time; O(V+E+total stored suffix
lengths) space.
The graph is unchanged. Recursive depth is safe under the official small vertex limit; output
may be exponential. Suffix DP can store paths from vertices unreachable from zero, whereas
backtracking stores only one live prefix plus answers.
"""

from collections import deque


class Solution:
    """Approach: Path-local DAG backtracking
    Time: O(V*2^V) loose bound
    Space: O(V) auxiliary plus output
    """

    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        path, result = [0], []

        def visit(node):
            if node == len(graph) - 1:
                result.append(path.copy())
                return
            for neighbor in graph[node]:
                path.append(neighbor)
                visit(neighbor)
                path.pop()

        visit(0)
        return result


class SuffixDPSolution:
    """Approach: Topological suffix-path DP
    Time: O(V+E+total copied suffix lengths)
    Space: O(V+E+total stored suffix lengths)
    """

    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        indegree = [0] * len(graph)
        for neighbors in graph:
            for neighbor in neighbors:
                indegree[neighbor] += 1
        queue = deque(node for node, count in enumerate(indegree) if count == 0)
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        paths = [[] for _ in graph]
        paths[-1] = [[len(graph) - 1]]
        for node in reversed(order):
            if node != len(graph) - 1:
                paths[node] = [
                    [node] + suffix for neighbor in graph[node] for suffix in paths[neighbor]
                ]
        return paths[0]
