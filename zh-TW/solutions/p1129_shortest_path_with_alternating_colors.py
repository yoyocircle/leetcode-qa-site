"""## Task

In a directed graph with red and blue edges, return each vertex's shortest distance from zero
using paths whose edge colors strictly alternate. Unreachable vertices have distance -1.

## Hints

1. Current vertex alone is insufficient state; remember the last edge color.
2. The expanded two-color state graph has ordinary unit-cost edges.

## Approach

### BFS on vertex and last color

Create separate red/blue adjacency lists and distances by last color. Seed vertex zero in both
imaginary last-color states so either first edge is allowed.

### Two-color Bellman-Ford relaxation

Keep two distances per vertex. Repeatedly relax red edges from blue-ending states and blue edges
from red-ending states until no changes or 2V-1 passes.

## Why it works

### BFS on vertex and last color

The expanded graph permits exactly edges of the opposite color. BFS distances in it therefore
equal shortest alternating-path lengths; the smaller terminal color gives each vertex's answer.

### Two-color Bellman-Ford relaxation

Every relaxation extends a legal alternating path. A shortest path needs no repeated expanded
state, hence at most 2V-1 edges; enough passes discover every shortest distance.

## Walkthrough

With red edges 0->1 and 1->2 and no blue edges, distances are [0,1,-1]. Adding blue 1->2 makes
the last distance 2.

## Cost and pitfalls

BFS on vertex and last color: O(V+E) time; O(V+E) space.
Two-color Bellman-Ford relaxation: O(V*E) time; O(V) space.
Inputs are unchanged. Directed and self edges retain their specified colors. The relaxation
variant scans more edges but avoids a queue and separate adjacency copies. Never mark a vertex
globally visited without its color.
"""

from collections import deque


class Solution:
    """Approach: BFS on vertex and last color
    Time: O(V+E)
    Space: O(V+E)
    """

    def shortestAlternatingPaths(
        self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]
    ) -> list[int]:
        adjacency = [[[] for _ in range(n)] for _ in range(2)]
        for color, edges in enumerate((redEdges, blueEdges)):
            for source, target in edges:
                adjacency[color][source].append(target)
        distances = [[float("inf")] * 2 for _ in range(n)]
        distances[0] = [0, 0]
        queue = deque([(0, 0), (0, 1)])
        while queue:
            node, last = queue.popleft()
            color = 1 - last
            for neighbor in adjacency[color][node]:
                if distances[neighbor][color] == float("inf"):
                    distances[neighbor][color] = distances[node][last] + 1
                    queue.append((neighbor, color))
        return [-1 if min(pair) == float("inf") else min(pair) for pair in distances]


class RelaxationSolution:
    """Approach: Two-color Bellman-Ford relaxation
    Time: O(V*E)
    Space: O(V)
    """

    def shortestAlternatingPaths(
        self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]
    ) -> list[int]:
        distances = [[float("inf")] * 2 for _ in range(n)]
        distances[0] = [0, 0]
        for _ in range(2 * n - 1):
            changed = False
            for color, edges in enumerate((redEdges, blueEdges)):
                for source, target in edges:
                    candidate = distances[source][1 - color] + 1
                    if candidate < distances[target][color]:
                        distances[target][color] = candidate
                        changed = True
            if not changed:
                break
        return [-1 if min(pair) == float("inf") else min(pair) for pair in distances]
