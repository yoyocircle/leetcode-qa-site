"""## Task

Count downward paths with sum targetSum. A path may begin and end at any nodes, but must always
follow parent-to-child edges.

## Hints

1. A path sum is the difference of two root-prefix sums.
2. Only prefixes on the current ancestor path may contribute.

## Approach

### Active prefix frequencies

Maintain frequencies of root-prefix sums using iterative enter/exit frames. Count prefix-target
matches before adding the current prefix; remove it when leaving the subtree.

### Enumerate downward starts

Start a sum traversal at each node, counting matching descendant endpoints. This educational
baseline avoids prefix maps but repeats descendant work.

## Why it works

### Active prefix frequencies

Each active prefix identifies one permissible start just below an ancestor. Its difference from
the current sum equals the downward path sum. Undo prevents counting paths across sibling
subtrees.

### Enumerate downward starts

Every downward path has a unique start and endpoint. The outer traversal chooses its start once,
and that start's inner traversal reaches its endpoint once.

## Walkthrough

For a chain [1,1,1] and target 2, the top-middle and middle-bottom paths match, giving 2.

## Cost and pitfalls

Active prefix frequencies: O(n) expected time; O(h) space.
Enumerate downward starts: O(n*h), O(n^2) worst time; O(h) space.
The tree is unchanged. Seed prefix zero with frequency one so paths starting at the root count.
Frequencies, rather than a set, are needed when zero-sum prefixes repeat. The baseline is slower
on deep chains.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Active prefix frequencies
    Time: O(n) expected
    Space: O(h)
    """

    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:
        counts = {0: 1}
        result = 0
        stack = [(root, 0, False)] if root else []
        while stack:
            node, prefix, exiting = stack.pop()
            if exiting:
                counts[prefix] -= 1
                if counts[prefix] == 0:
                    del counts[prefix]
                continue
            prefix += node.val
            result += counts.get(prefix - targetSum, 0)
            counts[prefix] = counts.get(prefix, 0) + 1
            stack.append((node, prefix, True))
            if node.right:
                stack.append((node.right, prefix, False))
            if node.left:
                stack.append((node.left, prefix, False))
        return result


class StartEveryNodeSolution:
    """Approach: Enumerate downward starts
    Time: O(n*h), O(n^2) worst
    Space: O(h)
    """

    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:
        result = 0
        starts = [root] if root else []
        while starts:
            start = starts.pop()
            if start.left:
                starts.append(start.left)
            if start.right:
                starts.append(start.right)
            pending = [(start, 0)]
            while pending:
                node, total = pending.pop()
                total += node.val
                result += total == targetSum
                for child in (node.left, node.right):
                    if child:
                        pending.append((child, total))
        return result
