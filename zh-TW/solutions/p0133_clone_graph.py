"""## Task

Make a deep copy of the connected undirected graph reachable from a supplied
node. Every copied node and neighbor list must be separate from the originals.

## Hints

1. A cycle means the same original node can appear through several paths.
2. Map original node objects to clones before exploring their neighbors.

## Approach

### Breadth-first identity map

Use breadth-first search and map original nodes to copies. Create the starting
clone immediately. For each original, create and enqueue unseen neighbor clones.
Append each neighbor's mapped clone to the current copy's list. Return the
starting clone, or None for an empty graph.

### Two-pass stack clone

First discover nodes with an explicit DFS stack and allocate identity-mapped clones. Only
after all nodes exist, fill every clone adjacency list in a second pass.

## Why it works

### Breadth-first identity map

The dictionary pairs each original with exactly one new object. Recording a
clone before visiting its edges breaks cycles: later paths reuse that clone.
Processing every adjacency list copies all edges and their order. Copied edges
always point to dictionary clones, never original nodes.

### Two-pass stack clone

The first pass creates exactly one clone per reachable original. The second maps every edge
endpoint through that complete dictionary, preserving order and cycles without ever
referencing original nodes in copied edges.

## Walkthrough

In a triangle 1--2--3--1, create clone 1, then clones 2 and 3 while processing
its neighbors. When processing 2, its edges reuse clones 1 and 3. The copied
triangle has the same connections with entirely new node identities.

## Cost and pitfalls

For the default Breadth-first identity map approach:

O(V + E) time, O(V) traversal and mapping space, and O(V + E) output space.
The original graph is unchanged. Key the dictionary by node identity.
Copying only neighbor lists would still share the original nodes.

Breadth-first identity map: O(V+E) time; O(V+E) including output space.
Two-pass stack clone: O(V+E) time; O(V+E) including output space.
The stack may hold O(E) pending references; the two-pass structure avoids wiring partially
explored nodes. Original nodes and neighbor lists remain unchanged.
"""

from collections import deque


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = [] if neighbors is None else neighbors


class Solution:
    """Approach: Breadth-first identity map
    Time: O(V+E)
    Space: O(V+E) including output
    """

    def cloneGraph(self, node: Node | None) -> Node | None:
        if node is None:
            return None
        copies = {node: Node(node.val)}
        queue = deque([node])
        while queue:
            original = queue.popleft()
            for neighbor in original.neighbors:
                if neighbor not in copies:
                    copies[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)
                copies[original].neighbors.append(copies[neighbor])
        return copies[node]


class StackSolution:
    """Approach: Two-pass stack clone
    Time: O(V+E)
    Space: O(V+E) including output
    """

    def cloneGraph(self, node: Node | None) -> Node | None:
        if node is None:
            return None
        copies = {}
        stack = [node]
        while stack:
            original = stack.pop()
            if original in copies:
                continue
            copies[original] = Node(original.val)
            stack.extend(neighbor for neighbor in original.neighbors if neighbor not in copies)
        for original, clone in copies.items():
            clone.neighbors = [copies[neighbor] for neighbor in original.neighbors]
        return copies[node]
