"""## Task

Use every flight ticket exactly once to construct an itinerary starting at
JFK. A valid itinerary is guaranteed. Among valid itineraries, return the
lexicographically smallest airport sequence. Repeated tickets are separate edges.

## Hints

1. This asks for an Eulerian trail over tickets, not a visit to each airport once.
2. Consume smaller destinations first, but append airports only after their outgoing edges end.

## Approach

### Sorted-list Hierholzer traversal

Run iterative Hierholzer traversal. Store destinations descending so popping
consumes the smallest. Keep the active route on a stack. Follow unused edges;
when the top has none, pop that airport into a reversed result. Reverse it.

### Heap-adjacency Hierholzer traversal

Store each airport's outgoing ticket destinations in a min-heap. Consume the smallest edge
and append airports only when their outgoing heap is exhausted, then reverse the finish
sequence.

## Why it works

### Sorted-list Hierholzer traversal

Each ticket is removed exactly once. Reverse finishing order splices discovered
cycles into one complete Eulerian trail. A branch ending the trip is placed
after the remaining branches. Sorted consumption makes the first feasible
differing destination smallest, giving the lexicographically smallest complete
trail under the guaranteed-existence contract.

### Heap-adjacency Hierholzer traversal

Hierholzer postorder splices all ticket edges into an Eulerian trail, including branches
that would strand a forward greedy walk. Minimum-edge consumption gives the smallest
feasible lexicographic trail under the existence guarantee.

## Walkthrough

With JFK->AAA, JFK->BBB, and BBB->JFK, visiting AAA first reaches a dead end.
Reverse finishing order places that endpoint last. Return
["JFK","BBB","JFK","AAA"], which uses all three tickets.

## Cost and pitfalls

For the default Sorted-list Hierholzer traversal approach:

O(E log E) sorting time and O(E) traversal and storage. Tickets are unchanged.
Do not deduplicate destinations or use a vertex-visited set. A forward greedy
walk alone can stop early even when a complete itinerary exists.

Sorted-list Hierholzer traversal: O(E log E) time; O(E) space.
Heap-adjacency Hierholzer traversal: O(E log E) time; O(E) space.
Heaps avoid globally sorting tickets but require a logarithmic pop for each edge. Lists sort
once and then pop in O(1). Both preserve duplicate tickets and original inputs.
"""

from collections import defaultdict


class Solution:
    """Approach: Sorted-list Hierholzer traversal
    Time: O(E log E)
    Space: O(E)
    """

    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        outgoing = defaultdict(list)
        for source, target in sorted(tickets, reverse=True):
            outgoing[source].append(target)
        stack = ["JFK"]
        reverse_route = []
        while stack:
            airport = stack[-1]
            if outgoing[airport]:
                stack.append(outgoing[airport].pop())
            else:
                reverse_route.append(stack.pop())
        return reverse_route[::-1]


class HeapSolution:
    """Approach: Heap-adjacency Hierholzer traversal
    Time: O(E log E)
    Space: O(E)
    """

    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        from heapq import heappop, heappush

        outgoing = {}
        for source, target in tickets:
            heappush(outgoing.setdefault(source, []), target)
        stack, route = ["JFK"], []
        while stack:
            edges = outgoing.get(stack[-1])
            if edges:
                stack.append(heappop(edges))
            else:
                route.append(stack.pop())
        route.reverse()
        return route
