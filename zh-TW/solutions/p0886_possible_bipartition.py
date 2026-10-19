"""## Task

Decide whether people can be split into two groups so every disliked pair belongs to
different groups.

## Hints

1. Each component admits a two-coloring exactly when it contains no odd cycle.
2. All neighbors of one person must belong to the same opposite group.

## Approach

### BFS two-coloring

Start each unseen connected component with one color and propagate opposite colors along
edges, rejecting equal-colored endpoints.

### Union opposite-neighbor groups

All neighbors of a person must share the opposite group, so union them. Reject if a dislike
ever connects two members of the same forced group.

## Why it works

### BFS two-coloring

Any valid grouping fixes alternating colors along every path from a start. A conflicting
edge disproves all colorings of that component; if none occurs, the constructed coloring
satisfies every dislike.

### Union opposite-neighbor groups

Every union expresses a necessary equality of group membership. A conflict makes these
constraints impossible; without conflicts, the implied equivalence groups admit the same
alternating component coloring as the original graph.

## Walkthrough

Pairs [1,2], [2,3], [3,1] form a triangle and cannot be split.

## Cost and pitfalls

BFS two-coloring: O(V+E) time; O(V+E) space.
Union opposite-neighbor groups: O((V+E)*alpha(V)) time; O(V+E) space.

Both preserve inputs and handle disconnected people. A visited set alone cannot detect color
contradictions; group parity or its equivalent is necessary.
"""


class Solution:
    """Approach: BFS two-coloring
    Time: O(V+E)
    Space: O(V+E)
    """

    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        from collections import deque

        graph = [[] for _ in range(n)]
        for a, b in dislikes:
            graph[a - 1].append(b - 1)
            graph[b - 1].append(a - 1)
        color = [-1] * n
        for start in range(n):
            if color[start] >= 0:
                continue
            color[start] = 0
            queue = deque([start])
            while queue:
                node = queue.popleft()
                for other in graph[node]:
                    if color[other] == color[node]:
                        return False
                    if color[other] < 0:
                        color[other] = color[node] ^ 1
                        queue.append(other)
        return True


class UnionFindSolution:
    """Approach: Union opposite-neighbor groups
    Time: O((V+E)*alpha(V))
    Space: O(V+E)
    """

    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        graph = [[] for _ in range(n)]
        for a, b in dislikes:
            graph[a - 1].append(b - 1)
            graph[b - 1].append(a - 1)
        parent, size = list(range(n)), [1] * n

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for node, others in enumerate(graph):
            if not others:
                continue
            for other in others:
                if find(node) == find(other):
                    return False
                a, b = find(others[0]), find(other)
                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
        return True
