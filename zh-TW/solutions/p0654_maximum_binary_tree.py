"""## Task

Construct a tree from distinct array values: its root is the maximum, and its left and right
subtrees come from the values before and after that maximum.

## Hints

1. A newly encountered larger value becomes an ancestor of smaller recent values.
2. Maintain a decreasing stack of the unfinished right spine.

## Approach

### Decreasing Cartesian-tree stack

For each value create one node. Pop smaller stack nodes, assigning the last popped subtree as
its left child. If a larger stack ancestor remains, link its right child to the new node.

### Repeated interval maxima

Use explicit interval tasks. Scan each interval for its maximum, create its root, and schedule
the left and right intervals. This simple baseline repeats scans on ordered arrays.

## Why it works

### Decreasing Cartesian-tree stack

The stack is the processed tree's decreasing right spine. Popped suffix values lie before the
new maximum and become its left subtree; the remaining larger ancestor still bounds the new
right descendant.

### Repeated interval maxima

Selecting the interval maximum is exactly the recursive definition. The two remaining intervals
partition all other values and preserve their relative positions, so induction constructs the
required tree.

## Walkthrough

For [3,1,4,2], root 4 has left subtree rooted at 3 with right child 1, and right leaf 2.

## Cost and pitfalls

Decreasing Cartesian-tree stack: O(n) time; O(n) auxiliary and output space.
Repeated interval maxima: O(n^2) worst time; O(h) auxiliary; O(n) output space.
The input array is unchanged. The scanning baseline may be slow on large ordered inputs; the
default is linear because each node is pushed and popped once. Both avoid deep recursion.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Decreasing Cartesian-tree stack
    Time: O(n)
    Space: O(n) auxiliary and output
    """

    def constructMaximumBinaryTree(self, nums: list[int]) -> TreeNode:
        stack = []
        for value in nums:
            node = TreeNode(value)
            while stack and stack[-1].val < value:
                node.left = stack.pop()
            if stack:
                stack[-1].right = node
            stack.append(node)
        return stack[0]


class IntervalMaximumSolution:
    """Approach: Repeated interval maxima
    Time: O(n^2) worst
    Space: O(h) auxiliary; O(n) output
    """

    def constructMaximumBinaryTree(self, nums: list[int]) -> TreeNode:
        dummy = TreeNode()
        stack = [(0, len(nums), dummy, "left")]
        while stack:
            low, high, parent, side = stack.pop()
            if low == high:
                continue
            middle = max(range(low, high), key=nums.__getitem__)
            node = TreeNode(nums[middle])
            setattr(parent, side, node)
            stack.extend(((middle + 1, high, node, "right"), (low, middle, node, "left")))
        return dummy.left
