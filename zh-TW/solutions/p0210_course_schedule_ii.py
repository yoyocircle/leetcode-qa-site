"""## Task

Return any order that completes all courses while taking each prerequisite
before its dependent. Return an empty list if dependencies contain a cycle.
Course identifiers run from zero to numCourses minus one.

## Hints

1. Start with courses that have no prerequisites.
2. Append a course only when all incoming dependency edges have been removed.

## Approach

### Kahn indegree queue

Apply Kahn's topological sort using prerequisite-to-dependent adjacency lists
and incoming-edge counts. Queue zero-count courses, including isolated courses.
Append each popped course and reduce its dependents' counts. Return the order
only if it contains every course.

### Iterative three-color DFS

Use explicit DFS frames with retained child iterators. White nodes are unseen, gray nodes
are on the active path, and black nodes are finished. A gray edge detects a cycle; finishing
order reversed is topological.

## Why it works

### Kahn indegree queue

When a course is appended, all its prerequisites are already processed, so
every dependency points forward in the order. Removing it exposes dependents
whose last prerequisite just completed. A cycle never exposes its first course:
each member waits for another. If processing stops early, the remaining graph
contains a cycle and no complete ordering exists.

### Iterative three-color DFS

An edge to an active ancestor closes a directed cycle. Without such an edge, every successor
finishes before its predecessor, so reversing finish order places every prerequisite first.

## Walkthrough

For pairs [[2,0],[2,1]] among four courses, the initial ready courses are
0, 1, and 3. Taking 0 and 1 releases 2. Both [0,1,3,2] and [1,0,2,3]
are valid; no single ordering is required.

## Cost and pitfalls

For the default Kahn indegree queue approach:

O(V + E) time and auxiliary space, including the order. Inputs are unchanged.
Keep the full course set rather than just identifiers mentioned in edges.
A partial order must not be returned when another component contains a cycle.

Kahn indegree queue: O(V+E) time; O(V+E) space.
Iterative three-color DFS: O(V+E) time; O(V+E) space.
The explicit stack avoids recursion failure on long dependency chains. Both include
disconnected courses and preserve prerequisites.
"""

from collections import deque


class Solution:
    """Approach: Kahn indegree queue
    Time: O(V+E)
    Space: O(V+E)
    """

    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        dependents = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            dependents[prerequisite].append(course)
            indegree[course] += 1
        queue = deque(course for course, count in enumerate(indegree) if count == 0)
        order = []
        while queue:
            course = queue.popleft()
            order.append(course)
            for dependent in dependents[course]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        return order if len(order) == numCourses else []


class DFSSolution:
    """Approach: Iterative three-color DFS
    Time: O(V+E)
    Space: O(V+E)
    """

    def findOrder(self, numCourses: int, prerequisites: list[list[int]]):
        outgoing = [[] for _ in range(numCourses)]
        for course, prerequisite in prerequisites:
            outgoing[prerequisite].append(course)
        colors = [0] * numCourses
        order = []
        for start in range(numCourses):
            if colors[start]:
                continue
            colors[start] = 1
            stack = [(start, iter(outgoing[start]))]
            while stack:
                node, children = stack[-1]
                child = next(children, None)
                if child is None:
                    stack.pop()
                    colors[node] = 2
                    order.append(node)
                elif colors[child] == 1:
                    return []
                elif colors[child] == 0:
                    colors[child] = 1
                    stack.append((child, iter(outgoing[child])))
        return order[::-1]
