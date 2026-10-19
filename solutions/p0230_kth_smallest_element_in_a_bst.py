"""## Task

Return the kth smallest value in a valid BST, counting k from 1. The tree is
nonempty and k is within its node count.

## Hints

1. Inorder traversal yields values in sorted order.
2. Stop at the kth visited node instead of building the entire sorted list.

## Approach

### Early inorder traversal

Use an explicit stack to walk inorder. Each pop visits the next smallest value;
decrement k and return when it reaches zero.

### Restored Morris threads

Use temporary predecessor-to-ancestor threads to perform inorder traversal without a stack.
Record the kth value but continue to the end so every temporary link is removed. The tree is
restored before returning.

## Why it works

### Early inorder traversal

All nodes in a left subtree precede their parent, and all nodes in its right
subtree follow it. BST ordering makes this exactly ascending value order.
Therefore the kth visited value has the requested rank.

### Restored Morris threads

A thread returns control to a node after its left subtree. Visiting only when no left child
exists or when removing its thread yields exact inorder order. Completing traversal removes
every introduced pointer.

## Walkthrough

For a BST with root 4, left subtree [2 with children 1 and 3], and right
child 6, inorder begins 1,2,3. For k=3, return 3 before visiting 4 or 6.

## Cost and pitfalls

Default approach costs and behavior:

O(h+k) time, bounded by O(n), and O(h) auxiliary space. The tree is unchanged.
Count visited nodes, not traversal stack pushes. An iterative traversal handles
deep trees safely. For frequent updates and rank queries, an augmented BST with
subtree sizes is a different design; this static problem does not need it.

Alternative tradeoff: O(n) time; O(1) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Early inorder traversal
    Time: O(h+k)
    Space: O(h)
    """

    def kthSmallest(self, root: TreeNode, k: int) -> int:
        stack = []
        current = root
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            k -= 1
            if k == 0:
                return current.val
            current = current.right
        raise ValueError("k must be within the node count")


class MorrisTraversalSolution:
    """Approach: Restored Morris threads
    Time: O(n)
    Space: O(1)
    """

    def kthSmallest(self, root: TreeNode, k: int) -> int:
        current = root
        answer = None
        while current:
            if current.left:
                predecessor = current.left
                while predecessor.right and predecessor.right is not current:
                    predecessor = predecessor.right
                if predecessor.right is None:
                    predecessor.right = current
                    current = current.left
                    continue
                predecessor.right = None
            k -= 1
            if k == 0:
                answer = current.val
            current = current.right
        return answer
