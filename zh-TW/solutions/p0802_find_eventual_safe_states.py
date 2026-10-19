"""## Task

Return vertices from which every directed path eventually terminates, in increasing order.

## Hints

1. A terminal vertex is safe, and a vertex is safe when all successors are safe.
2. Alternatively detect whether a DFS path can reach a cycle.

## Approach

### Reverse edges and remove terminal layers

Start from terminal nodes and decrement their predecessors' remaining outgoing-edge counts.
A predecessor becomes safe when all outgoing edges lead to removed safe nodes.

### Iterative DFS with safe and unsafe outcomes

Use statuses unseen, active, safe, and unsafe with explicit child iterators. If an active
frame reaches an active ancestor or known unsafe vertex, mark the entire current path
unsafe; otherwise finish it safe.

## Why it works

### Reverse edges and remove terminal layers

Every released node terminates through already-safe successors. Unreleased nodes retain an
outgoing edge within the unreleased graph, so following such edges eventually enters a
cycle.

### Iterative DFS with safe and unsafe outcomes

Finishing after all safe children proves safety. A back edge reaches a cycle, and every
frame in the active path can reach it; reaching an unsafe child has the same implication.
These outcomes classify every visited vertex correctly.

## Walkthrough

In [[1],[2],[1],[]], only vertex 3 is safe because 1 and 2 form a cycle.

## Cost and pitfalls

Reverse edges and remove terminal layers: O(V+E) time; O(V+E) space.
Iterative DFS with safe and unsafe outcomes: O(V+E) time; O(V) space.

Inputs are unchanged. DFS uses the original adjacency lists instead of storing a reverse
graph and avoids recursion depth failure. A vertex merely having some terminating path is
insufficient; all paths must terminate.
"""


class Solution:
    """Approach: Reverse edges and remove terminal layers
    Time: O(V+E)
    Space: O(V+E)
    """

    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:
        from collections import deque

        reverse = [[] for _ in graph]
        remaining = [len(edges) for edges in graph]
        for node, edges in enumerate(graph):
            for other in edges:
                reverse[other].append(node)
        queue = deque(node for node, count in enumerate(remaining) if count == 0)
        safe = [False] * len(graph)
        while queue:
            node = queue.popleft()
            safe[node] = True
            for parent in reverse[node]:
                remaining[parent] -= 1
                if remaining[parent] == 0:
                    queue.append(parent)
        return [node for node, good in enumerate(safe) if good]


class DFSSolution:
    """Approach: Iterative DFS with safe and unsafe outcomes
    Time: O(V+E)
    Space: O(V)
    """

    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:
        state = [0] * len(graph)
        for start in range(len(graph)):
            if state[start]:
                continue
            state[start] = 1
            stack = [(start, iter(graph[start]))]
            while stack:
                node, children = stack[-1]
                other = next(children, None)
                if other is None:
                    state[node] = 2
                    stack.pop()
                elif state[other] in (1, 3):
                    for active, _ in stack:
                        state[active] = 3
                    stack.clear()
                elif state[other] == 0:
                    state[other] = 1
                    stack.append((other, iter(graph[other])))
        return [node for node, status in enumerate(state) if status == 2]
