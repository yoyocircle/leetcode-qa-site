"""## Task

Return the leftmost node value on the deepest level of a nonempty binary tree.

## Hints

1. Keep tree depth explicit in traversal state.
2. A queue groups levels; a stack needs an array or remembered deepest depth.

## Approach

### Breadth-first row processing

Use fixed-size BFS levels and retain the first queued node of each new level.

### Depth-indexed iterative DFS

Use left-first DFS with explicit depths. Update the answer only on the first visit to a depth
greater than all previous depths.

## Why it works

### Breadth-first row processing

BFS queues exactly one row at a time in left-to-right order. Processing its fixed starting size
therefore derives the requested value from precisely that row.

### Depth-indexed iterative DFS

Each stack entry carries its exact depth. DFS visits every node once; its depth-specific update
therefore includes all and only nodes in that row. Left-first order also makes the first deepest
visit the leftmost one.

## Walkthrough

Root 4 has left leaf 2 and right child 7 whose left leaf is 6. The deepest row contains only 6,
so return 6.

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

    def findBottomLeftValue(self, root: TreeNode) -> int:
        queue = deque([root])
        answer = root.val
        while queue:
            answer = queue[0].val
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return answer


class DepthFirstSolution:
    """Approach: Depth-indexed iterative DFS
    Time: O(n)
    Space: O(h) auxiliary plus output
    """

    def findBottomLeftValue(self, root: TreeNode) -> int:
        stack = [(root, 0)]
        deepest = -1
        answer = root.val
        while stack:
            node, depth = stack.pop()
            if depth > deepest:
                deepest, answer = depth, node.val
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))
        return answer
