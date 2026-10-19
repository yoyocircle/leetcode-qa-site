"""## Task

Find the maximum product of edge success probabilities over paths between two vertices, or
zero if unreachable.

## Hints

1. A probability product never increases when adding an edge.
2. Relax multiplicative scores either by best-first expansion or repeated scans.

## Approach

### Maximum-probability Dijkstra

Use a min-heap of negative probabilities to finalize the greatest available path
probability. Relax neighbors by multiplication.

### Multiplicative Bellman-Ford

Scan each undirected edge in both directions and improve endpoint product scores until
stable or V-1 rounds have run.

## Why it works

### Maximum-probability Dijkstra

All factors lie in [0,1], so extending a path cannot improve its score. The greatest
unsettled score cannot be beaten through a smaller unsettled predecessor, validating
best-first finalization.

### Multiplicative Bellman-Ford

Cycles with factors at most one cannot improve a product, so an optimal path is simple and
uses at most V-1 edges. Repeated relaxation covers all such paths.

## Walkthrough

Edges 0-1 at 0.5, 1-2 at 0.5, and 0-2 at 0.2 give best probability 0.25.

## Cost and pitfalls

Maximum-probability Dijkstra: O((V+E)*log V) time; O(V+E) space.
Multiplicative Bellman-Ford: O(V*E) time; O(V) space.

Inputs remain unchanged. The repeated-relaxation baseline may be too slow on worst-case
large networks; prefer Dijkstra. Zero-probability routes correctly yield zero and need not
be enqueued.
"""


class Solution:
    """Approach: Maximum-probability Dijkstra
    Time: O((V+E)*log V)
    Space: O(V+E)
    """

    def maxProbability(
        self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int
    ) -> float:
        from heapq import heappop, heappush

        graph = [[] for _ in range(n)]
        for (a, b), probability in zip(edges, succProb, strict=True):
            graph[a].append((b, probability))
            graph[b].append((a, probability))
        best = [0.0] * n
        best[start_node] = 1.0
        heap = [(-1.0, start_node)]
        while heap:
            negative, node = heappop(heap)
            probability = -negative
            if probability != best[node]:
                continue
            if node == end_node:
                return probability
            for other, edge in graph[node]:
                following = probability * edge
                if following > best[other]:
                    best[other] = following
                    heappush(heap, (-following, other))
        return 0.0


class RelaxationSolution:
    """Approach: Multiplicative Bellman-Ford
    Time: O(V*E)
    Space: O(V)
    """

    def maxProbability(
        self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int
    ) -> float:
        best = [0.0] * n
        best[start_node] = 1.0
        for _ in range(n - 1):
            changed = False
            for (a, b), probability in zip(edges, succProb, strict=True):
                for source, target in ((a, b), (b, a)):
                    candidate = best[source] * probability
                    if candidate > best[target]:
                        best[target] = candidate
                        changed = True
            if not changed:
                break
        return best[end_node]
