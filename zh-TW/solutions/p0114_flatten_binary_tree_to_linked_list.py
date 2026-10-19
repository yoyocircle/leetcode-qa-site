"""## Task

Flatten a binary tree in place into a right-child chain in preorder. Every left pointer must
become None and every original node must remain in the chain.

## Hints

1. Preorder fixes the required node order before rewiring.
2. The rightmost node of a left subtree can hold the original right subtree.

## Approach

### Explicit preorder stack

Visit nodes using a stack, saving right and left children before changing the previous node's
links. Connect each visited node after its predecessor.

### In-place subtree splicing

When a node has a left subtree, attach its original right subtree after the left subtree's
rightmost node. Move the left subtree to the right, clear left, and advance right.

## Why it works

### Explicit preorder stack

The stack yields original preorder because children are saved before links change. Connecting
consecutive visits realizes the requested chain without losing any subtree.

### In-place subtree splicing

Preorder visits the left subtree before the original right subtree. Splicing preserves that
order and moves the next preorder node to the current right link. Each predecessor edge is
scanned only a bounded number of times.

## Walkthrough

For root 4 with left subtree 2->right 3 and right leaf 7, the final chain is 4->2->3->7.

## Cost and pitfalls

Explicit preorder stack: O(n) time; O(h) space.
In-place subtree splicing: O(n) time; O(1) space.
Both variants mutate and reuse the tree. Neither creates replacement output nodes. The stack
variant does not meet the constant-space follow-up; splicing does. Save child references before
rewriting links.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Explicit preorder stack
    Time: O(n)
    Space: O(h)
    """

    def flatten(self, root: TreeNode | None) -> None:
        stack = [root] if root else []
        previous = None
        while stack:
            node = stack.pop()
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
            if previous:
                previous.left = None
                previous.right = node
            previous = node
        if previous:
            previous.left = previous.right = None


class SpliceSolution:
    """Approach: In-place subtree splicing
    Time: O(n)
    Space: O(1)
    """

    def flatten(self, root: TreeNode | None) -> None:
        current = root
        while current:
            if current.left:
                last = current.left
                while last.right:
                    last = last.right
                last.right = current.right
                current.right = current.left
                current.left = None
            current = current.right
