"""## Task

Count shortest routes from vertex zero to vertex n-1 in an undirected graph with strictly
positive road times. Return the count modulo 1,000,000,007.

## Hints

1. When a shorter distance appears, replace its route count; when an equal distance appears, add
   counts.
2. Positive weights orient every shortest-path edge toward a strictly larger source distance.

## Approach

### Dijkstra distances and tied-route counts

Track best distances and counts together in heap Dijkstra. A strict improvement copies its
predecessor count; an equal-distance relaxation adds that count modulo the modulus.

### Floyd distances and shortest-path DAG DP

Compute all-pairs distances with Floyd-Warshall. Sort vertices by distance from zero and
propagate counts only over edges satisfying dist[u]+weight=dist[v].

## Why it works

### Dijkstra distances and tied-route counts

Every shortest route has a final edge from a strictly nearer predecessor. All such predecessors
are finalized before the vertex is popped, so their disjoint final-edge route families can be
summed exactly.

### Floyd distances and shortest-path DAG DP

Floyd gives exact shortest metrics. Positivity makes the retained edges a DAG ordered by source
distance, and its forward path-count DP enumerates exactly all shortest routes.

## Walkthrough

For roads 0-1 of time 1, 1-3 of time 2, 0-2 of time 1, and 2-3 of time 2, the distance to 3 is 3
with two routes.

## Cost and pitfalls

Dijkstra distances and tied-route counts: O((V+E) log(V+1)) time; O(V+E) space.
Floyd distances and shortest-path DAG DP: O(V^3+V log(V+1)+E) time; O(V^2+E) space.
Roads are unchanged. Equal-distance discoveries must add rather than overwrite. Do not push
another heap entry solely for a tie. The dense Floyd alternative is useful at the small vertex
limit but substantially slower on sparse graphs.
"""

from heapq import heappop, heappush


class Solution:
    """Approach: Dijkstra distances and tied-route counts
    Time: O((V+E) log(V+1))
    Space: O(V+E)
    """

    def countPaths(self, n: int, roads: list[list[int]]) -> int:
        modulus = 1_000_000_007
        adjacency = [[] for _ in range(n)]
        for left, right, weight in roads:
            adjacency[left].append((right, weight))
            adjacency[right].append((left, weight))
        distances = [float("inf")] * n
        counts = [0] * n
        distances[0], counts[0] = 0, 1
        heap = [(0, 0)]
        while heap:
            distance, node = heappop(heap)
            if distance != distances[node]:
                continue
            for neighbor, weight in adjacency[node]:
                candidate = distance + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    counts[neighbor] = counts[node]
                    heappush(heap, (candidate, neighbor))
                elif candidate == distances[neighbor]:
                    counts[neighbor] = (counts[neighbor] + counts[node]) % modulus
        return counts[-1]


class FloydDAGSolution:
    """Approach: Floyd distances and shortest-path DAG DP
    Time: O(V^3+V log(V+1)+E)
    Space: O(V^2+E)
    """

    def countPaths(self, n: int, roads: list[list[int]]) -> int:
        modulus = 1_000_000_007
        distances = [[float("inf")] * n for _ in range(n)]
        adjacency = [[] for _ in range(n)]
        for node in range(n):
            distances[node][node] = 0
        for left, right, weight in roads:
            distances[left][right] = distances[right][left] = weight
            adjacency[left].append((right, weight))
            adjacency[right].append((left, weight))
        for middle in range(n):
            for left in range(n):
                prefix = distances[left][middle]
                for right in range(n):
                    candidate = prefix + distances[middle][right]
                    if candidate < distances[left][right]:
                        distances[left][right] = candidate
        best = distances[0]
        counts = [0] * n
        counts[0] = 1
        for node in sorted(range(n), key=best.__getitem__):
            if best[node] == float("inf"):
                break
            for neighbor, weight in adjacency[node]:
                if best[node] + weight == best[neighbor]:
                    counts[neighbor] = (counts[neighbor] + counts[node]) % modulus
        return counts[-1]
