"""## Task

Reconstruct the unique binary tree from its preorder and inorder traversals.
Values are distinct, and the two traversals are guaranteed consistent.

## Hints

1. Preorder introduces each root before its children.
2. Inorder tells you when a node's entire left side has been completed.

## Approach

### Ancestor-stack reconstruction

Use a stack of the current preorder ancestor path and an index into inorder.
A new preorder value becomes the top node's left child until that top matches
the next inorder value. Pop all matching completed ancestors; attach the new
value as the last popped node's right child.

### Indexed interval tasks

Index inorder positions and consume preorder roots using explicit subtree-interval tasks. Each
task attaches a new node to a known parent. Push right before left so preorder consumption
remains root-left-right.

## Why it works

### Ancestor-stack reconstruction

Preorder fixes the next node to create. Before an ancestor appears in inorder,
that next node belongs on its unfinished left descent. Matching inorder values
close those left descents; the last closed ancestor is exactly whose right
subtree starts next. Distinct values make these matches unambiguous.

### Indexed interval tasks

The next preorder value is the root of the pending subtree. Its inorder index uniquely splits
that interval into left and right descendants. Induction on interval size reconstructs the
specified tree without recursion or slices.

## Walkthrough

Preorder [4,2,3,6], inorder [2,3,4,6]: attach 2 left of 4. Seeing 2
in inorder closes its left side, so 3 becomes its right child. Then 3 and 4
close in order, and 6 becomes 4's right child.

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(h) auxiliary stack space, plus O(n) output nodes. Inputs are
unchanged. Each node enters and leaves the stack once. This avoids recursive
slices and recursion-depth failures on skewed trees.

Alternative tradeoff: O(n) time; O(n) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Ancestor-stack reconstruction
    Time: O(n)
    Space: O(h) auxiliary; O(n) output
    """

    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode:
        values = iter(preorder)
        root = TreeNode(next(values))
        stack = [root]
        index = 0
        for value in values:
            node = stack[-1]
            child = TreeNode(value)
            if node.val != inorder[index]:
                node.left = child
            else:
                while stack and stack[-1].val == inorder[index]:
                    node = stack.pop()
                    index += 1
                node.right = child
            stack.append(child)
        return root


class IntervalTasksSolution:
    """Approach: Indexed interval tasks
    Time: O(n)
    Space: O(n)
    """

    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode:
        positions = {value: index for index, value in enumerate(inorder)}
        dummy = TreeNode()
        tasks = [(0, len(inorder), dummy, "left")]
        values = iter(preorder)
        while tasks:
            low, high, parent, side = tasks.pop()
            if low == high:
                continue
            node = TreeNode(next(values))
            setattr(parent, side, node)
            middle = positions[node.val]
            tasks.append((middle + 1, high, node, "right"))
            tasks.append((low, middle, node, "left"))
        return dummy.left
