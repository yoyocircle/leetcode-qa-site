"""## Task

Decide whether a binary tree is complete: all levels except possibly the last are full, and the
last level is filled from left to right.

## Hints

1. In level order, no real node may occur after the first missing child.
2. Alternatively summarize whether each subtree is perfect, complete, and how tall it is.

## Approach

### Breadth-first first-gap rule

Queue both real and missing child slots. After encountering None, reject any later real node.

### Bottom-up structural states

Compute height, perfectness, and completeness in iterative postorder. A complete root has either
equal child heights with a perfect left side, or a left side one taller and a perfect right
side.

## Why it works

### Breadth-first first-gap rule

Complete-tree occupied slots form one prefix of breadth-first positions. A real node after a
missing slot is exactly a hole before an occupied position.

### Bottom-up structural states

These are exactly the two ways the last incomplete level can sit: in the right subtree after a
full left, or in the left subtree above a shorter full right. Requiring the remaining subtree
complete closes the induction.

## Walkthrough

A root with only a left child is complete. A root with only a right child has a missing slot
before an occupied one and is not complete.

## Cost and pitfalls

Breadth-first first-gap rule: O(n) time; O(w) space.
Bottom-up structural states: O(n) time; O(n) space.
The tree is unchanged. The empty tree is complete. Counting nodes at a level alone misses
misplaced gaps. Explicit structural traversal avoids large positional integers and
recursion-depth limits.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Breadth-first first-gap rule
    Time: O(n)
    Space: O(w)
    """

    def isCompleteTree(self, root: TreeNode | None) -> bool:
        queue = deque([root])
        gap = False
        while queue:
            node = queue.popleft()
            if node is None:
                gap = True
            else:
                if gap:
                    return False
                queue.extend((node.left, node.right))
        return True


class SubtreeStateSolution:
    """Approach: Bottom-up structural states
    Time: O(n)
    Space: O(n)
    """

    def isCompleteTree(self, root: TreeNode | None) -> bool:
        states = {None: (0, True, True)}
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if not expanded:
                stack.append((node, True))
                for child in (node.left, node.right):
                    if child:
                        stack.append((child, False))
                continue
            lh, lp, lc = states[node.left]
            rh, rp, rc = states[node.right]
            perfect = lp and rp and lh == rh
            complete = (lp and rc and lh == rh) or (lc and rp and lh == rh + 1)
            states[node] = (1 + max(lh, rh), perfect, complete)
        return states[root][2]
