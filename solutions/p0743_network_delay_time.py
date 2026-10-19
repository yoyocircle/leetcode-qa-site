"""## Task

A signal starts at node k and travels along directed edges with nonnegative
travel times. Return the earliest time by which every node receives it, or
-1 when at least one node is unreachable.

## Hints

1. Arrival time at each node is its shortest-path distance from the source.
2. Always expand the smallest currently known arrival time using a min-heap.

## Approach

### Heap Dijkstra arrival times

Run Dijkstra's algorithm on outgoing adjacency lists. Initialize the source
distance to zero and others to infinity. Expand heap entries matching current
best distances, relax outgoing edges, and push improvements. Ignore stale
entries. Return the maximum distance, unless a node remains unreachable.

### Repeated directed-edge relaxation

Relax all directed edges for up to V-1 rounds, stopping when a round changes nothing.
Distances start infinite except the source.

## Why it works

### Heap Dijkstra arrival times

The smallest unsettled distance cannot improve through another unsettled node:
reaching that node already costs at least as much, and edges never decrease
path cost. Its expansion uses the final earliest arrival. Relaxation propagates
improvements along outgoing edges. The maximum earliest arrival is when the
whole network has received the signal.

### Repeated directed-edge relaxation

After r full scans, shortest paths of at most r edges are represented, possibly sooner with
in-place propagation. A nonnegative shortest simple path uses at most V-1 edges, so all
shortest distances are found.

## Walkthrough

For [[1,2,6],[1,3,2],[3,2,1]] from 1, node 3 arrives at time 2 and
improves node 2 from 6 to 3. Return 3 and ignore the stale 6.

## Cost and pitfalls

For the default Heap Dijkstra arrival times approach:

O((V + E) log V) time and O(V + E) space for this graph's distinct directed
edges. Inputs are unchanged. A FIFO BFS cannot handle unequal weights.
Take the maximum shortest distance, not the sum of edge weights or arrivals.

Heap Dijkstra arrival times: O((V+E) log V) time; O(V+E) space.
Repeated directed-edge relaxation: O(V*E) time; O(V) space.
Bellman-Ford avoids a heap and uses only a distance array, but repeats edge scans. The final
distance slice allocates O(V) temporary space. Inputs remain unchanged.
"""

from heapq import heappop, heappush


class Solution:
    """Approach: Heap Dijkstra arrival times
    Time: O((V+E) log V)
    Space: O(V+E)
    """

    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        outgoing = [[] for _ in range(n + 1)]
        for source, target, weight in times:
            outgoing[source].append((target, weight))
        distances = [float("inf")] * (n + 1)
        distances[k] = 0
        queue = [(0, k)]
        while queue:
            distance, node = heappop(queue)
            if distance != distances[node]:
                continue
            for target, weight in outgoing[node]:
                candidate = distance + weight
                if candidate < distances[target]:
                    distances[target] = candidate
                    heappush(queue, (candidate, target))
        delay = max(distances[1:])
        return -1 if delay == float("inf") else int(delay)


class BellmanFordSolution:
    """Approach: Repeated directed-edge relaxation
    Time: O(V*E)
    Space: O(V)
    """

    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        distance = [float("inf")] * (n + 1)
        distance[k] = 0
        for _ in range(n - 1):
            changed = False
            for source, target, weight in times:
                if distance[source] + weight < distance[target]:
                    distance[target] = distance[source] + weight
                    changed = True
            if not changed:
                break
        answer = max(distance[1:])
        return -1 if answer == float("inf") else answer
