"""## Task

Decide whether every node satisfies the strict binary-search-tree ordering:
all left-subtree values are smaller, and all right-subtree values are larger.

## Hints

1. Comparing only a parent and its direct children misses deeper violations.
2. What should an inorder traversal of a valid BST look like?

## Approach

### Increasing inorder

Perform iterative inorder traversal with an explicit stack. Compare each visited
value with the previous inorder value; any non-increase makes the tree invalid.

### Ancestor bounds

Carry an open lower and upper bound with each iterative traversal entry. A left child inherits
the lower bound and receives its parent as upper bound; a right child receives the symmetric
interval.

## Why it works

### Increasing inorder

Inorder lists the entire left subtree, then the node, then its entire right
subtree. Strict increase therefore enforces every required ancestor ordering,
not just adjacent parent-child relations. Conversely, a valid BST's inorder
sequence is strictly increasing.

### Ancestor bounds

Each interval intersects all ancestor restrictions for that subtree. Every node inside its
interval satisfies all required ancestor comparisons. A failed strict bound witnesses a BST
violation, including duplicate values.

## Walkthrough

Root 5 has left child 1 and right child 7, with 7.left=4. Local edges may look
plausible, but inorder is [1,5,4,7]. The decrease from 5 to 4 rejects the tree.

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(h) stack space for height h; the tree is unchanged. Equal values
are invalid. Iteration avoids recursion failure on a long chain. Use a separate
None state for the missing previous value instead of an arbitrary numeric bound.

Alternative tradeoff: O(n) time; O(h) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Increasing inorder
    Time: O(n)
    Space: O(h)
    """

    def isValidBST(self, root: TreeNode | None) -> bool:
        stack = []
        current = root
        previous = None
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            if previous is not None and current.val <= previous:
                return False
            previous = current.val
            current = current.right
        return True


class AncestorBoundsSolution:
    """Approach: Ancestor bounds
    Time: O(n)
    Space: O(h)
    """

    def isValidBST(self, root: TreeNode | None) -> bool:
        stack = [(root, float("-inf"), float("inf"))] if root else []
        while stack:
            node, low, high = stack.pop()
            if not low < node.val < high:
                return False
            if node.right:
                stack.append((node.right, node.val, high))
            if node.left:
                stack.append((node.left, low, node.val))
        return True
