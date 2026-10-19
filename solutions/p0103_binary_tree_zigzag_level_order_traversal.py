"""## Task

Return tree values grouped by depth, alternating left-to-right and right-to-left order starting
with left-to-right at the root.

## Hints

1. Group nodes by depth before deciding row order.
2. Keep child discovery order stable and reverse only the relevant value rows.

## Approach

### Breadth-first alternating rows

Process fixed-size queue layers left to right. Reverse the collected values on odd depths;
always enqueue left children before right.

### Depth-indexed DFS

Use iterative left-first DFS to append values to depth-indexed rows, then reverse odd rows after
traversal.

## Why it works

### Breadth-first alternating rows

BFS supplies each depth in physical left-to-right order. Reversing exactly the odd rows applies
the required zigzag without changing later discovery order.

### Depth-indexed DFS

Left-first DFS visits nodes at any fixed depth in left-to-right order. Depth indexing yields the
same rows as BFS, and the final reversal provides the alternating direction.

## Walkthrough

For root 5 with children 2 and 8 and grandchildren 1,3,7,9, return [[5],[8,2],[1,3,7,9]].

## Cost and pitfalls

Breadth-first alternating rows: O(n) time; O(w) auxiliary; O(n) output space.
Depth-indexed DFS: O(n) time; O(h) auxiliary; O(n) output space.
The tree is unchanged. Reversing the queue as well as output can accidentally reverse the next
layer twice. Empty trees yield an empty list.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Breadth-first alternating rows
    Time: O(n)
    Space: O(w) auxiliary; O(n) output
    """

    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        result = []
        queue = deque([root]) if root else deque()
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            if len(result) % 2:
                level.reverse()
            result.append(level)
        return result


class DepthFirstSolution:
    """Approach: Depth-indexed DFS
    Time: O(n)
    Space: O(h) auxiliary; O(n) output
    """

    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        result = []
        stack = [(root, 0)] if root else []
        while stack:
            node, depth = stack.pop()
            if depth == len(result):
                result.append([])
            result[depth].append(node.val)
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))
        for depth in range(1, len(result), 2):
            result[depth].reverse()
        return result
