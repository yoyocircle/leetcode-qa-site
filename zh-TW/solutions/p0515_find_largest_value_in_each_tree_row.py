"""## Task

Return the maximum node value in each binary-tree row, ordered from the root downward. An empty
tree yields an empty list.

## Hints

1. Keep tree depth explicit in traversal state.
2. A queue groups levels; a stack needs an array or remembered deepest depth.

## Approach

### Breadth-first row processing

Process each BFS level separately and take its maximum, initializing from a real value rather
than zero.

### Depth-indexed iterative DFS

Use DFS depth labels and a result array. The first node at a depth creates an entry; later nodes
update that entry with the greater value.

## Why it works

### Breadth-first row processing

BFS queues exactly one row at a time in left-to-right order. Processing its fixed starting size
therefore derives the requested value from precisely that row.

### Depth-indexed iterative DFS

Each stack entry carries its exact depth. DFS visits every node once; its depth-specific update
therefore includes all and only nodes in that row. Left-first order also makes the first deepest
visit the leftmost one.

## Walkthrough

For root -4 with children -8 and -2, return [-4,-2]; initializing a maximum to zero would be
wrong.

## Cost and pitfalls

Breadth-first row processing: O(n) time; O(w) auxiliary plus output space.
Depth-indexed iterative DFS: O(n) time; O(h) auxiliary plus output space.
Neither variant changes the tree. n is node count, h height, and w maximum occupied width. Both
are iterative, so a deep chain does not exceed Python recursion depth. Negative values remain
valid.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Breadth-first row processing
    Time: O(n)
    Space: O(w) auxiliary plus output
    """

    def largestValues(self, root: TreeNode | None) -> list[int]:
        result = []
        queue = deque([root]) if root else deque()
        while queue:
            maximum = float("-inf")
            for _ in range(len(queue)):
                node = queue.popleft()
                maximum = max(maximum, node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(maximum)
        return result


class DepthFirstSolution:
    """Approach: Depth-indexed iterative DFS
    Time: O(n)
    Space: O(h) auxiliary plus output
    """

    def largestValues(self, root: TreeNode | None) -> list[int]:
        result = []
        stack = [(root, 0)] if root else []
        while stack:
            node, depth = stack.pop()
            if depth == len(result):
                result.append(node.val)
            else:
                result[depth] = max(result[depth], node.val)
            for child in (node.left, node.right):
                if child:
                    stack.append((child, depth + 1))
        return result
