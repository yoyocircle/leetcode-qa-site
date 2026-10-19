"""## Task

Decide whether every course can be completed. A prerequisite pair [course,
prerequisite] means the prerequisite must be taken first. A directed dependency
cycle makes completing all courses impossible.

## Hints

1. Courses with no unfinished prerequisites can be taken immediately.
2. Track remaining prerequisite counts and remove ready courses one at a time.

## Approach

### Kahn indegree queue

Build prerequisite-to-dependent edges and indegree counts for every course,
including isolated courses. Queue all zero-indegree courses. Taking a course
decrements its dependents' counts; enqueue a dependent when its count becomes
zero. Compare the number taken with numCourses.

### Iterative three-color DFS

Use explicit DFS frames with retained child iterators. White nodes are unseen, gray nodes
are on the active path, and black nodes are finished. A gray edge detects a cycle; finishing
order reversed is topological.

## Why it works

### Kahn indegree queue

A queued course has no remaining prerequisites, so taking it respects every
dependency. If the queue empties early, every remaining course has a remaining
predecessor. Following predecessors must repeat a course, revealing a cycle.
Conversely, no cycle member can be released first. All courses are therefore
processed exactly when the graph is acyclic.

### Iterative three-color DFS

An edge to an active ancestor closes a directed cycle. Without such an edge, every successor
finishes before its predecessor, so reversing finish order places every prerequisite first.

## Walkthrough

For four courses and pairs [[1,0],[2,0],[3,2]], course 0 unlocks 1 and 2;
course 2 unlocks 3. All four complete. Adding [0,3] leaves a cycle and fails.

## Cost and pitfalls

For the default Kahn indegree queue approach:

O(V + E) time and auxiliary space. The prerequisite list is unchanged.
Reversing just the adjacency direction while keeping the old indegrees breaks
the model. Checking only one connected component can miss a separate cycle.

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

    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        dependents = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            dependents[prerequisite].append(course)
            indegree[course] += 1
        queue = deque(course for course, count in enumerate(indegree) if count == 0)
        completed = 0
        while queue:
            course = queue.popleft()
            completed += 1
            for dependent in dependents[course]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        return completed == numCourses


class DFSSolution:
    """Approach: Iterative three-color DFS
    Time: O(V+E)
    Space: O(V+E)
    """

    def canFinish(self, numCourses: int, prerequisites: list[list[int]]):
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
                    return False
                elif colors[child] == 0:
                    colors[child] = 1
                    stack.append((child, iter(outgoing[child])))
        return True
