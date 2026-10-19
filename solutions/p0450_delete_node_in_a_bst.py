"""## Task

Delete the node with a given key from a BST and return a valid remaining BST. If the key is
absent, return the original tree.

## Hints

1. One-child deletion simply promotes that child.
2. For two children, either promote the successor or graft the right tree after the left
   maximum.

## Approach

### Physical successor promotion

Find the node and its parent iteratively. For two children, detach the smallest right-subtree
node and move that original node into the deleted node's position.

### Left-subtree promotion and graft

Promote the target's left subtree when both children exist. Attach the original right subtree as
the right child of the left subtree's maximum node.

## Why it works

### Physical successor promotion

The successor exceeds every left value and is no greater than the remaining right values. Its
old position has no left child, so detaching it preserves order before it replaces the target.

### Left-subtree promotion and graft

Every right-subtree value exceeds the target and hence every left-subtree value. Grafting at the
left maximum preserves all BST bounds and keeps all remaining nodes reachable.

## Walkthrough

Deleting 4 from a tree with left leaf 2 and right subtree rooted at 7 with left child 5 can
promote 5, or promote 2 and attach the right subtree after it.

## Cost and pitfalls

Physical successor promotion: O(h) time; O(1) space.
Left-subtree promotion and graft: O(h) time; O(1) space.
Both variants mutate pointers, preserve remaining node identities and values, and avoid
recursion. Valid output shape need not be unique. Deleting the root requires returning a
possibly different root reference.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Physical successor promotion
    Time: O(h)
    Space: O(1)
    """

    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        parent, node = None, root
        while node and node.val != key:
            parent = node
            node = node.left if key < node.val else node.right
        if node is None:
            return root
        if node.left and node.right:
            successor_parent, successor = node, node.right
            while successor.left:
                successor_parent, successor = successor, successor.left
            if successor_parent is not node:
                successor_parent.left = successor.right
                successor.right = node.right
            successor.left = node.left
            replacement = successor
        else:
            replacement = node.left or node.right
        if parent is None:
            return replacement
        if parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement
        return root


class GraftSolution:
    """Approach: Left-subtree promotion and graft
    Time: O(h)
    Space: O(1)
    """

    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        dummy = TreeNode(right=root)
        parent, node = dummy, root
        while node and node.val != key:
            parent = node
            node = node.left if key < node.val else node.right
        if node is None:
            return root
        replacement = node.right
        if node.left:
            replacement = node.left
            maximum = replacement
            while maximum.right:
                maximum = maximum.right
            maximum.right = node.right
        if parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement
        return dummy.right
