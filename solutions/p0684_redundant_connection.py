"""## Task

An undirected graph was formed by adding one edge to a tree. Return an edge
whose removal restores a tree. When several edges qualify, choose the one
that occurs latest in the input.

## Hints

1. Adding an edge creates a cycle exactly when its endpoints are already connected.
2. Process edges in order while maintaining connected components with union-find.

## Approach

### Size-weighted union-find

Start with every vertex in its own disjoint set. Find each edge's endpoint
roots. Equal roots identify the redundant edge. Otherwise join the smaller
component under the larger root. Compress paths during searches to speed
future root lookups.
The linked Union find template also shows union by rank: compare root ranks,
attach the lower rank, and increment only after merging equal-rank roots.
Rank bounds historical tree height; size counts vertices. Either heuristic with
path compression gives the same amortized bound for this problem.

### Check reachability before each insertion

Maintain the accepted forest explicitly. Before adding an edge, traverse from its first
endpoint; an already-reachable second endpoint means the edge closes a cycle.

## Why it works

### Size-weighted union-find

Accepted edges form a forest. The sets describe its connected components
because every accepted edge merges its endpoint components. An edge within
one component closes a cycle. The promised graph has only one cycle, so its
last encountered edge is the first rejected edge and the latest eligible removal.

### Check reachability before each insertion

A forest gains a cycle exactly when an inserted edge connects vertices already connected by
a path. Input order makes the rejected edge the last edge of the unique cycle, satisfying
the requested tie rule.

## Walkthrough

For [[1,2],[2,3],[1,3]], the first two edges combine all three vertices.
The final edge joins vertices already connected by 1--2--3. Return [1,3].

## Cost and pitfalls

For the default Size-weighted union-find approach:

O(E * alpha(V)) amortized time and O(V) space, where alpha is the inverse
Ackermann function. Inputs are unchanged. The vertex labels fit 1 through E
under the tree-plus-one-edge contract. Joining endpoints directly without
first finding their roots would break the component representation.

Size-weighted union-find: O(E*alpha(V)) time; O(V) space.
Check reachability before each insertion: O(E*(V+E)) time; O(V+E) space.
Repeated traversal is a slower educational baseline, though the problem has at most 1000
edges. Both preserve edge order and contents.
"""


class Solution:
    """Approach: Size-weighted union-find
    Time: O(E*alpha(V))
    Space: O(V)
    """

    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        parent = list(range(len(edges) + 1))
        size = [1] * len(parent)

        def find(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for left, right in edges:
            left_root, right_root = find(left), find(right)
            if left_root == right_root:
                return [left, right]
            if size[left_root] < size[right_root]:
                left_root, right_root = right_root, left_root
            parent[right_root] = left_root
            size[left_root] += size[right_root]
        return []


class SearchSolution:
    """Approach: Check reachability before each insertion
    Time: O(E*(V+E))
    Space: O(V+E)
    """

    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        graph = [[] for _ in range(len(edges) + 1)]
        for left, right in edges:
            seen = {left}
            stack = [left]
            while stack:
                node = stack.pop()
                for other in graph[node]:
                    if other not in seen:
                        seen.add(other)
                        stack.append(other)
            if right in seen:
                return [left, right]
            graph[left].append(right)
            graph[right].append(left)
        return []
