"""## Task

Reconstruct a binary tree from consistent inorder and postorder traversals with distinct values.

## Hints

1. The last postorder value is the root.
2. Reading postorder backward visits root, right, then left.

## Approach

### Reversed ancestor stack

Read postorder backward. Attach right children until the stack top matches the next
reversed-inorder value; pop completed ancestors and attach the next value as the last popped
node's left child.

### Indexed interval tasks

Map values to inorder indices. Consume reversed postorder while processing explicit subtree
intervals, pushing left tasks before right tasks.

## Why it works

### Reversed ancestor stack

Reversed postorder fixes the next root. Reversed inorder identifies exactly when its right
ancestry is complete, locating the parent whose left subtree starts next.

### Indexed interval tasks

Each root splits its inorder interval uniquely. Processing the right interval first matches
reversed postorder, so the resulting subtree partitions satisfy both traversals.

## Walkthrough

Inorder [2,4,5] and postorder [2,5,4] give root 4, left child 2, and right child 5.

## Cost and pitfalls

Reversed ancestor stack: O(n) time; O(h) auxiliary; O(n) output space.
Indexed interval tasks: O(n) time; O(n) space.
Inputs are unchanged. Both variants avoid recursion and traversal slices. The interval map costs
linear storage even for a shallow tree; the ancestor stack uses only its height.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Reversed ancestor stack
    Time: O(n)
    Space: O(h) auxiliary; O(n) output
    """

    def buildTree(self, inorder: list[int], postorder: list[int]) -> TreeNode:
        values = iter(reversed(postorder))
        root = TreeNode(next(values))
        stack, index = [root], len(inorder) - 1
        for value in values:
            node = stack[-1]
            child = TreeNode(value)
            if node.val != inorder[index]:
                node.right = child
            else:
                while stack and stack[-1].val == inorder[index]:
                    node = stack.pop()
                    index -= 1
                node.left = child
            stack.append(child)
        return root


class IntervalTasksSolution:
    """Approach: Indexed interval tasks
    Time: O(n)
    Space: O(n)
    """

    def buildTree(self, inorder: list[int], postorder: list[int]) -> TreeNode:
        positions = {value: index for index, value in enumerate(inorder)}
        dummy = TreeNode()
        values = iter(reversed(postorder))
        stack = [(0, len(inorder), dummy, "left")]
        while stack:
            low, high, parent, side = stack.pop()
            if low == high:
                continue
            node = TreeNode(next(values))
            setattr(parent, side, node)
            middle = positions[node.val]
            stack.append((low, middle, node, "left"))
            stack.append((middle + 1, high, node, "right"))
        return dummy.left
