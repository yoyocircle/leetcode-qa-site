"""## Task

Generate every structurally distinct BST containing values 1 through n. Return separate mutable
trees so editing one answer does not change another.

## Hints

1. Choosing a root splits the value interval into independent left and right intervals.
2. Cache immutable subtree descriptions, then allocate fresh nodes for each answer.

## Approach

### Memoized immutable tree shapes

Memoize tuples describing every root/left/right choice for an interval. Materialize each final
description into entirely new TreeNode objects.

### Bottom-up interval tree table

Fill interval tables from shorter to longer intervals. For each root, clone both chosen subtrees
before attaching them to a new node. This uses concrete intermediate trees instead of immutable
templates.

## Why it works

### Memoized immutable tree shapes

Every BST has one root and uniquely determined smaller and larger intervals. Their Cartesian
product enumerates all valid trees without duplicates; fresh materialization prevents
cross-answer aliasing.

### Bottom-up interval tree table

Shorter intervals are complete before use. Combining every possible root and subtree pair gives
all trees for the next interval; cloning ensures no returned answers share mutable nodes.

## Walkthrough

For n=2, the two outputs are root 1 with right child 2, and root 2 with left child 1.

## Cost and pitfalls

Memoized immutable tree shapes: O(n*C_n) loose bound time; O(n*C_n) including output space.
Bottom-up interval tree table: O(n^2*C_n) loose bound time; O(n^2*C_n) loose bound including
output space.
C_n is the nth Catalan number. Output itself is exponential and contains n*C_n nodes. Recursion
is bounded by n<=8. No caller data is mutated; copying is intentional to keep result ownership
independent.
"""

from functools import cache


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Memoized immutable tree shapes
    Time: O(n*C_n) loose bound
    Space: O(n*C_n) including output
    """

    def generateTrees(self, n: int) -> list[TreeNode]:
        @cache
        def shapes(low, high):
            if low > high:
                return (None,)
            return tuple(
                (value, left, right)
                for value in range(low, high + 1)
                for left in shapes(low, value - 1)
                for right in shapes(value + 1, high)
            )

        def materialize(shape):
            if shape is None:
                return None
            value, left, right = shape
            return TreeNode(value, materialize(left), materialize(right))

        return [materialize(shape) for shape in shapes(1, n)]


class BottomUpSolution:
    """Approach: Bottom-up interval tree table
    Time: O(n^2*C_n) loose bound
    Space: O(n^2*C_n) loose bound including output
    """

    def generateTrees(self, n: int) -> list[TreeNode]:
        def clone(node):
            return TreeNode(node.val, clone(node.left), clone(node.right)) if node else None

        table = {(low, low - 1): [None] for low in range(1, n + 2)}
        for length in range(1, n + 1):
            for low in range(1, n - length + 2):
                high = low + length - 1
                table[low, high] = [
                    TreeNode(value, clone(left), clone(right))
                    for value in range(low, high + 1)
                    for left in table[low, value - 1]
                    for right in table[value + 1, high]
                ]
        return table[1, n]
