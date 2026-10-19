"""## Task

For each ordered course query [a,b], decide whether a is a direct or indirect prerequisite of b.
The directed prerequisite graph is acyclic.

## Hints

1. Process a course only after all its prerequisites have contributed their ancestor sets.
2. Repeated queries from one source can share a reachability traversal.

## Approach

### Topological ancestor bitsets

Store one integer ancestor mask per course. In topological order, propagate a course's own bit
and inherited ancestor mask into every dependent. Answer with a bit test.

### Cached per-source reachability

On the first query from a source, traverse all outgoing prerequisite edges and cache the
reachable set. Reuse that set for later queries from the same source.

## Why it works

### Topological ancestor bitsets

When a course leaves the zero-indegree queue, all incoming predecessors have already propagated
their complete ancestors. The union is therefore precisely its transitive prerequisite set.

### Cached per-source reachability

A traversal reaches exactly courses with a directed dependency path from its source. Cached
membership therefore answers the same transitive prerequisite relation without depending on
query order.

## Walkthrough

With prerequisites 0->1 and 1->2, query [0,2] is true, [2,0] false, and [0,1] true.

## Cost and pitfalls

Topological ancestor bitsets: O((V+E+Q)*B), B=words per V-bit mask time; O(V+E) references and
O(V^2) ancestor bits space.
Cached per-source reachability: O(V*(V+E)+Q) worst time; O(V^2+E) space.
Inputs are unchanged. B accounts for Python integer bit operations rather than assuming
arbitrarily large masks are constant size. The bitset approach exploits the DAG contract; the
cached-search approach uses more explicit sets.
"""

from collections import deque


class Solution:
    """Approach: Topological ancestor bitsets
    Time: O((V+E+Q)*B), B=words per V-bit mask
    Space: O(V+E) references and O(V^2) ancestor bits
    """

    def checkIfPrerequisite(
        self, numCourses: int, prerequisites: list[list[int]], queries: list[list[int]]
    ) -> list[bool]:
        adjacency = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for source, target in prerequisites:
            adjacency[source].append(target)
            indegree[target] += 1
        ancestors = [0] * numCourses
        queue = deque(node for node, count in enumerate(indegree) if count == 0)
        while queue:
            node = queue.popleft()
            inherited = ancestors[node] | (1 << node)
            for dependent in adjacency[node]:
                ancestors[dependent] |= inherited
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        return [bool(ancestors[target] & (1 << source)) for source, target in queries]


class CachedSearchSolution:
    """Approach: Cached per-source reachability
    Time: O(V*(V+E)+Q) worst
    Space: O(V^2+E)
    """

    def checkIfPrerequisite(
        self, numCourses: int, prerequisites: list[list[int]], queries: list[list[int]]
    ) -> list[bool]:
        adjacency = [[] for _ in range(numCourses)]
        for source, target in prerequisites:
            adjacency[source].append(target)
        cache = {}
        result = []
        for source, target in queries:
            if source not in cache:
                seen = set()
                stack = list(adjacency[source])
                while stack:
                    node = stack.pop()
                    if node in seen:
                        continue
                    seen.add(node)
                    stack.extend(adjacency[node])
                cache[source] = seen
            result.append(target in cache[source])
        return result
