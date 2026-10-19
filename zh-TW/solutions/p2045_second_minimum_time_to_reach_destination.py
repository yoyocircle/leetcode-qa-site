"""## Task

Find the second distinct arrival time from vertex 1 to vertex n in a connected undirected graph.
Each edge takes time units. All signals alternate green/red every change units, starting green;
leave immediately on green and wait on red.

## Hints

1. Because travel times and signals are identical, arrival time depends only on the number of
   edges walked.
2. Keep two distinct labels per vertex; equal-time routes do not form a second minimum.

## Approach

### Two hop distances then signal simulation

BFS the two smallest distinct edge counts to every vertex. When the second destination count is
popped, simulate that many departures, waiting to the next green boundary on red.

### Two-arrival time-dependent Dijkstra

Maintain two distinct arrival labels per vertex in a min-heap. Before traversing an edge, apply
its compulsory signal wait, then relax the new arrival. Return the second destination label when
popped.

## Why it works

### Two hop distances then signal simulation

All walks of h edges have the same arrival T(h), and T(h+1)>T(h). Thus the second distinct hop
count yields the second distinct time. Two-label BFS enumerates the two smallest distances; an
undirected backtrack guarantees a second walk.

### Two-arrival time-dependent Dijkstra

Signal waiting is FIFO: arriving later cannot permit an earlier departure. Here the shared
timing recurrence also strictly orders realizable hop-count arrivals, so retaining two distinct
labels suffices. Heap extraction finalizes those labels in increasing time.

## Walkthrough

For a single edge, time=1 and change=2, the first arrival is 1. The next walk is 1->2->1->2:
arrive back at time 2, wait until 4, then reach 2 at time 5.

## Cost and pitfalls

Two hop distances then signal simulation: O(V+E) time; O(V+E) space.
Two-arrival time-dependent Dijkstra: O((V+E) log(V+1)) time; O(V+E) space.
Inputs are unchanged. Routes may revisit vertices, including the destination. A time exactly
divisible by change begins the next signal phase. Wait before departures, never after the final
arrival. Equal first-arrival routes still count as one time.
"""

from collections import deque
from heapq import heappop, heappush


class Solution:
    """Approach: Two hop distances then signal simulation
    Time: O(V+E)
    Space: O(V+E)
    """

    def secondMinimum(self, n: int, edges: list[list[int]], time: int, change: int) -> int:
        adjacency = [[] for _ in range(n + 1)]
        for left, right in edges:
            adjacency[left].append(right)
            adjacency[right].append(left)
        distances = [[float("inf")] * 2 for _ in range(n + 1)]
        distances[1][0] = 0
        queue = deque([(1, 0)])
        while queue:
            node, hops = queue.popleft()
            if node == n and hops == distances[n][1]:
                arrival = 0
                for _ in range(hops):
                    phase = arrival // change
                    if phase % 2:
                        arrival = (phase + 1) * change
                    arrival += time
                return arrival
            for neighbor in adjacency[node]:
                candidate = hops + 1
                if candidate < distances[neighbor][0]:
                    distances[neighbor][1] = distances[neighbor][0]
                    distances[neighbor][0] = candidate
                    queue.append((neighbor, candidate))
                elif distances[neighbor][0] < candidate < distances[neighbor][1]:
                    distances[neighbor][1] = candidate
                    queue.append((neighbor, candidate))
        raise AssertionError("Connected undirected graphs admit a second walk")


class ArrivalHeapSolution:
    """Approach: Two-arrival time-dependent Dijkstra
    Time: O((V+E) log(V+1))
    Space: O(V+E)
    """

    def secondMinimum(self, n: int, edges: list[list[int]], time: int, change: int) -> int:
        adjacency = [[] for _ in range(n + 1)]
        for left, right in edges:
            adjacency[left].append(right)
            adjacency[right].append(left)
        arrivals = [[float("inf")] * 2 for _ in range(n + 1)]
        arrivals[1][0] = 0
        heap = [(0, 1)]
        while heap:
            arrival, node = heappop(heap)
            if arrival > arrivals[node][1]:
                continue
            if node == n and arrival == arrivals[n][1]:
                return arrival
            phase = arrival // change
            departure = (phase + 1) * change if phase % 2 else arrival
            candidate = departure + time
            for neighbor in adjacency[node]:
                if candidate < arrivals[neighbor][0]:
                    arrivals[neighbor][1] = arrivals[neighbor][0]
                    arrivals[neighbor][0] = candidate
                    heappush(heap, (candidate, neighbor))
                elif arrivals[neighbor][0] < candidate < arrivals[neighbor][1]:
                    arrivals[neighbor][1] = candidate
                    heappush(heap, (candidate, neighbor))
        raise AssertionError("Connected undirected graphs admit a second walk")
