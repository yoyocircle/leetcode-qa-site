"""## Task

Return all root-to-leaf value paths whose sum is targetSum. A path must end at a leaf; negative
values are allowed.

## Hints

1. A matching partial sum at an internal node is insufficient.
2. Copy a path only when it is a complete matching answer.

## Approach

### Explicit DFS undo frames

Use enter and exit frames with a shared path. Entering appends the value and updates the sum;
the exit frame removes it after both subtrees finish.

### Breadth-first sums and parent map

BFS tracks cumulative sums and parent identities. For each matching leaf, reconstruct its path
by following parents backward, then reverse the collected values.

## Why it works

### Explicit DFS undo frames

The shared path always equals the root-to-current route because each entry has one matching
exit. Recording only matching leaves therefore produces exactly the accepted root-to-leaf paths.

### Breadth-first sums and parent map

Each node has one root path, so its parent map and accumulated sum describe that path uniquely.
Reconstruction is performed only for leaves that meet the sum condition.

## Walkthrough

For root 2 with left leaf 5 and right child -1 whose left leaf is 6, target 7 accepts [2,5] and
[2,-1,6].

## Cost and pitfalls

Explicit DFS undo frames: O(n + output size) time; O(h) auxiliary plus output space.
Breadth-first sums and parent map: O(n + output size) time; O(n) auxiliary plus output space.
The tree is unchanged. Output path copies count toward time and space. Negative values prevent
pruning merely because a running sum exceeds the target. Iterative traversal supports skewed
trees.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Explicit DFS undo frames
    Time: O(n + output size)
    Space: O(h) auxiliary plus output
    """

    def pathSum(self, root: TreeNode | None, targetSum: int) -> list[list[int]]:
        result, path = [], []
        stack = [(root, 0, False)] if root else []
        while stack:
            node, total, exiting = stack.pop()
            if exiting:
                path.pop()
                continue
            total += node.val
            path.append(node.val)
            stack.append((node, total, True))
            if node.left is None and node.right is None and total == targetSum:
                result.append(path.copy())
            if node.right:
                stack.append((node.right, total, False))
            if node.left:
                stack.append((node.left, total, False))
        return result


class ParentMapSolution:
    """Approach: Breadth-first sums and parent map
    Time: O(n + output size)
    Space: O(n) auxiliary plus output
    """

    def pathSum(self, root: TreeNode | None, targetSum: int) -> list[list[int]]:
        if root is None:
            return []
        parents = {root: None}
        queue = deque([(root, root.val)])
        result = []
        while queue:
            node, total = queue.popleft()
            if node.left is None and node.right is None and total == targetSum:
                path, current = [], node
                while current:
                    path.append(current.val)
                    current = parents[current]
                result.append(path[::-1])
            for child in (node.left, node.right):
                if child:
                    parents[child] = node
                    queue.append((child, total + child.val))
        return result
