"""## Task

Return the rightmost visible node value at each depth of a binary tree,
ordered from root downward.

## Hints

1. A level-order traversal already groups nodes by depth.
2. With children enqueued left before right, which processed node is visible?

## Approach

### Breadth-first rightmost values

Run breadth-first search one level at a time. Save the value of the last
processed node in each fixed-size level.

### Right-first DFS

Walk a stack of nodes and depths, visiting right children first. Record only the first node seen
at each new depth; it is the visible one.

## Why it works

### Breadth-first rightmost values

The queue orders a level from left to right because each parent's left child
is enqueued before its right child, and parents themselves have that order.
The last node in each level is therefore its rightmost visible node.

### Right-first DFS

All nodes in a right subtree precede equal-depth nodes in its left sibling subtree. The first
visit at a depth is therefore its rightmost node even when it lies under a left ancestor.

## Walkthrough

Root 1 has children 2 and 3; node 2 has right child 5, while 3 has no
children. Levels are [1], [2,3], [5], giving the view [1,3,5].

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(w) auxiliary queue space for maximum width w, plus O(h) output.
The tree is unchanged. The view is not just the root's right-child chain:
a deeper left-subtree node can be visible when no right-subtree node shares
its depth. An empty tree yields an empty list.

Alternative tradeoff: O(n) time; O(h) space.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Breadth-first rightmost values
    Time: O(n)
    Space: O(w) auxiliary; O(h) output
    """

    def rightSideView(self, root: TreeNode | None) -> list[int]:
        if root is None:
            return []
        queue = deque([root])
        result = []
        while queue:
            width = len(queue)
            for i in range(width):
                node = queue.popleft()
                if i == width - 1:
                    result.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result


class RightFirstDFSSolution:
    """Approach: Right-first DFS
    Time: O(n)
    Space: O(h)
    """

    def rightSideView(self, root: TreeNode | None) -> list[int]:
        result = []
        stack = [(root, 0)] if root else []
        while stack:
            node, depth = stack.pop()
            if depth == len(result):
                result.append(node.val)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        return result
