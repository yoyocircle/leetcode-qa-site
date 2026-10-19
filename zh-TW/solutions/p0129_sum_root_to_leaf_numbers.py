"""## Task

Each tree node stores a decimal digit. Interpret each root-to-leaf path as a number and return
the sum of those numbers.

## Hints

1. Extending a path appends a decimal digit: number*10+digit.
2. A threaded traversal can recover path numbers when returning from a subtree.

## Approach

### Stack of partial numbers

Traverse with (node,number-before-node) states. Append the current digit and add the number only
at leaves. Push each child with that same updated prefix.

### Morris decimal backtracking

Create temporary predecessor threads. Track the current number; on returning through a thread,
remove the digits introduced along that completed left descent. Detect its leaf at the
predecessor.

## Why it works

### Stack of partial numbers

Induction on depth makes the stored number exactly the path prefix. Every leaf contributes its
complete represented number once.

### Morris decimal backtracking

Thread return restores the ancestor context. The counted predecessor-path length tells exactly
how many decimal digits to remove. Each original leaf contributes once, and all temporary links
are removed.

## Walkthrough

For root 3 with leaves 1 and 4, the represented numbers are 31 and 34, totaling 65.

## Cost and pitfalls

Stack of partial numbers: O(n) time; O(h) space.
Morris decimal backtracking: O(n) time; O(1) space.
The stack variant leaves links untouched. Morris temporarily mutates and restores them. The
stated costs use the problem's bounded numerical results; arbitrary unbounded path integers
require additional bit-operation costs.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Stack of partial numbers
    Time: O(n)
    Space: O(h)
    """

    def sumNumbers(self, root: TreeNode | None) -> int:
        total = 0
        stack = [(root, 0)] if root else []
        while stack:
            node, prefix = stack.pop()
            number = prefix * 10 + node.val
            if node.left is None and node.right is None:
                total += number
            for child in (node.left, node.right):
                if child:
                    stack.append((child, number))
        return total


class MorrisSolution:
    """Approach: Morris decimal backtracking
    Time: O(n)
    Space: O(1)
    """

    def sumNumbers(self, root: TreeNode | None) -> int:
        total = number = 0
        current = root
        while current:
            if current.left:
                predecessor, steps = current.left, 1
                while predecessor.right and predecessor.right is not current:
                    predecessor = predecessor.right
                    steps += 1
                if predecessor.right is None:
                    number = number * 10 + current.val
                    predecessor.right = current
                    current = current.left
                    continue
                if predecessor.left is None:
                    total += number
                for _ in range(steps):
                    number //= 10
                predecessor.right = None
            else:
                number = number * 10 + current.val
                if current.right is None:
                    total += number
            current = current.right
        return total
