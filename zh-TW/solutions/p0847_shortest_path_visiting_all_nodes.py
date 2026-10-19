"""## Task

Find the shortest walk visiting every vertex of a connected undirected graph; revisits and
any starting vertex are allowed.

## Hints

1. The state needs both current vertex and the set already visited.
2. All-pairs shortest distances can compress walks between selected visit-order endpoints.

## Approach

### Multi-source visited-mask BFS

Seed one state per possible start. Traverse unit edges while OR-ing the destination bit into
the visited mask.

### Metric closure and subset endpoint DP

BFS from each vertex computes metric distances. A subset DP chooses an order for visiting
distinguished vertices, charging shortest distances between consecutive endpoints.

## Why it works

### Multi-source visited-mask BFS

The expanded state includes every fact affecting future progress. BFS gives the shortest
walk from any start, and a full mask identifies exactly walks visiting all vertices.

### Metric closure and subset endpoint DP

Every chosen order expands into a legal walk visiting its endpoints. Conversely, first-visit
order in any optimal walk gives metric transitions no longer than its segments. These two
inequalities establish equal optimal costs even when metric paths pass through extra
vertices.

## Walkthrough

For a star with center 0 and leaves 1,2,3, a shortest walk such as 1,0,2,0,3 has four edges.

## Cost and pitfalls

Multi-source visited-mask BFS: O((V+E)*2^V) time; O(V*2^V) space.
Metric closure and subset endpoint DP: O(V*(V+E)+V^2*2^V) time; O(V*2^V+V^2) space.

Inputs remain unchanged. The exponential dependence is appropriate because V is at most 12.
Marking only vertices rather than vertex-mask pairs loses necessary revisit states.
"""


class Solution:
    """Approach: Multi-source visited-mask BFS
    Time: O((V+E)*2^V)
    Space: O(V*2^V)
    """

    def shortestPathLength(self, graph: list[list[int]]) -> int:
        from collections import deque

        full = (1 << len(graph)) - 1
        queue = deque((node, 1 << node, 0) for node in range(len(graph)))
        seen = {(node, 1 << node) for node in range(len(graph))}
        while queue:
            node, mask, steps = queue.popleft()
            if mask == full:
                return steps
            for other in graph[node]:
                following = mask | (1 << other)
                if (other, following) not in seen:
                    seen.add((other, following))
                    queue.append((other, following, steps + 1))
        return -1


class MetricDPSolution:
    """Approach: Metric closure and subset endpoint DP
    Time: O(V*(V+E)+V^2*2^V)
    Space: O(V*2^V+V^2)
    """

    def shortestPathLength(self, graph: list[list[int]]) -> int:
        from collections import deque

        n = len(graph)
        distance = [[n] * n for _ in graph]
        for start in range(n):
            distance[start][start] = 0
            queue = deque([start])
            while queue:
                node = queue.popleft()
                for other in graph[node]:
                    if distance[start][other] == n:
                        distance[start][other] = distance[start][node] + 1
                        queue.append(other)
        dp = [[float("inf")] * n for _ in range(1 << n)]
        for node in range(n):
            dp[1 << node][node] = 0
        for mask in range(1, 1 << n):
            for last in range(n):
                if not mask & (1 << last):
                    continue
                for other in range(n):
                    if not mask & (1 << other):
                        following = mask | (1 << other)
                        dp[following][other] = min(
                            dp[following][other], dp[mask][last] + distance[last][other]
                        )
        return min(dp[-1])
