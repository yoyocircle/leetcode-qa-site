"""## Task

Find the cheapest directed flight route using at most k intermediate stops; return -1 if absent.

## Hints

1. At most k stops permits at most k+1 edges.
2. Cost and remaining flight budget jointly determine a state.

## Approach

### Bounded-edge Bellman-Ford rows

Copy the preceding distance row before each full edge relaxation. A row permits one
additional flight, and copying retains routes with fewer flights.

### Dijkstra on node and flights-used states

Use a heap of cost, city, and flights-used states, relaxing an edge only while budget
remains. Keep separate best costs for each budget state.

## Why it works

### Bounded-edge Bellman-Ford rows

Transitions read only the old row, so no round can chain multiple new edges. Induction makes
row r exactly the best route cost with at most r edges.

### Dijkstra on node and flights-used states

Positive prices permit Dijkstra finalization on this expanded state graph. A cheap arrival
with no remaining budget must not erase a costlier arrival that can still continue.

## Walkthrough

For 0->1 costing 4, 1->2 costing 4, and 0->2 costing 12, k=0 gives 12 and k=1 gives 8.

## Cost and pitfalls

Bounded-edge Bellman-Ford rows: O((k+1)*(V+E)) time; O(V) space.
Dijkstra on node and flights-used states: O((k+1)*(V+E)*log((k+1)*V+1)) time; O((k+1)*(V+E))
space.

Inputs remain unchanged. Bellman-Ford copies cost O(V) per round, included above. A single
cost per city is insufficient when routes use different numbers of flights.
"""


class Solution:
    """Approach: Bounded-edge Bellman-Ford rows
    Time: O((k+1)*(V+E))
    Space: O(V)
    """

    def findCheapestPrice(
        self, n: int, flights: list[list[int]], src: int, dst: int, k: int
    ) -> int:
        costs = [float("inf")] * n
        costs[src] = 0
        for _ in range(k + 1):
            following = costs.copy()
            for a, b, price in flights:
                following[b] = min(following[b], costs[a] + price)
            costs = following
        return -1 if costs[dst] == float("inf") else costs[dst]


class DijkstraSolution:
    """Approach: Dijkstra on node and flights-used states
    Time: O((k+1)*(V+E)*log((k+1)*V+1))
    Space: O((k+1)*(V+E))
    """

    def findCheapestPrice(
        self, n: int, flights: list[list[int]], src: int, dst: int, k: int
    ) -> int:
        from heapq import heappop, heappush

        graph = [[] for _ in range(n)]
        for a, b, price in flights:
            graph[a].append((b, price))
        best = {(src, 0): 0}
        heap = [(0, src, 0)]
        while heap:
            cost, node, used = heappop(heap)
            if best[(node, used)] != cost:
                continue
            if node == dst:
                return cost
            if used == k + 1:
                continue
            for other, price in graph[node]:
                candidate = cost + price
                if candidate < best.get((other, used + 1), float("inf")):
                    best[(other, used + 1)] = candidate
                    heappush(heap, (candidate, other, used + 1))
        return -1
