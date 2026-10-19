"""## Task

Return a binary tree's values grouped by depth, ordered left to right within
each group. An empty tree produces an empty list.

## Hints

1. A FIFO queue processes nodes in increasing depth.
2. Freeze the current queue size before adding the next level's children.

## Approach

### Breadth-first levels

Use breadth-first search. At each outer iteration, process exactly the number
of nodes currently in the queue. Collect their values and enqueue each left
child before its right child.

### Depth-indexed DFS

Walk iteratively with (node,depth) entries. Append a new output row on the first visit to a
depth. Push the right child before the left so traversal records each depth left to right.

## Why it works

### Breadth-first levels

Initially the queue contains only the root level. Processing its fixed starting
size removes exactly that level and appends exactly the next level in left-to-right
order. Induction gives the required grouping at every depth.

### Depth-indexed DFS

DFS still visits all nodes at a fixed depth in left-to-right order when left subtrees precede
right subtrees. The explicit depth routes each value to exactly its level without a
breadth-first queue.

## Walkthrough

For root 8 with children 3 and 10, where 3 has right child 6, the successive
queue layers are [8], [3,10], and [6]. Return [[8],[3,10],[6]].

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(w) auxiliary queue space for maximum width w, plus O(n) output.
The tree is unchanged. Use deque.popleft rather than list.pop(0), which shifts
elements. Do not iterate until the queue empties inside a level: children added
during that loop belong to the next level.

Alternative tradeoff: O(n) time; O(h) auxiliary; O(n) output space.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Breadth-first levels
    Time: O(n)
    Space: O(w) auxiliary; O(n) output
    """

    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        queue = deque([root])
        result = []
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result


class DepthFirstSolution:
    """Approach: Depth-indexed DFS
    Time: O(n)
    Space: O(h) auxiliary; O(n) output
    """

    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
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
        return result
