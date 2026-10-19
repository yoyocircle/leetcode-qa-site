"""## Task

Choose tree nodes with maximum total value subject to never choosing both endpoints of a
parent-child edge. Return that maximum sum.

## Hints

1. A subtree result depends on whether its root is chosen.
2. A chosen root can combine only the grandchildren or skipped-child states.

## Approach

### Take and skip state pairs

In iterative postorder store (take,skip). Take adds the node and both child skip values; skip
adds each child's better state.

### Best value with grandchild recurrence

Store one best value per subtree. Compare excluding the root and taking child optima against
including it and taking grandchild optima.

## Why it works

### Take and skip state pairs

The only external conflict for a subtree is whether its root is taken. Enumerating those two
states captures every legal choice, and independent child optima can be added.

### Best value with grandchild recurrence

Including a root forbids exactly its children, leaving grandchildren independent. Excluding it
leaves both child problems unrestricted. Their maximum therefore covers all legal choices.

## Walkthrough

For root 4 with children 1 and 2 and a value-5 grandchild under 1, choose 4 and 5 for total 9.

## Cost and pitfalls

Take and skip state pairs: O(n) time; O(n) space.
Best value with grandchild recurrence: O(n) time; O(n) space.
The tree is unchanged. Greedily choosing an entire even or odd level can miss combinations from
different depths. Iterative postorder supports long chains; both state models need completed
descendants first.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Take and skip state pairs
    Time: O(n)
    Space: O(n)
    """

    def rob(self, root: TreeNode | None) -> int:
        values = {None: (0, 0)}
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if expanded:
                left, right = values[node.left], values[node.right]
                values[node] = (node.val + left[1] + right[1], max(left) + max(right))
            else:
                stack.append((node, True))
                for child in (node.left, node.right):
                    if child:
                        stack.append((child, False))
        return max(values[root])


class GrandchildSolution:
    """Approach: Best value with grandchild recurrence
    Time: O(n)
    Space: O(n)
    """

    def rob(self, root: TreeNode | None) -> int:
        best = {None: 0}
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if expanded:
                take = node.val
                for child in (node.left, node.right):
                    if child:
                        take += best[child.left] + best[child.right]
                best[node] = max(take, best[node.left] + best[node.right])
            else:
                stack.append((node, True))
                for child in (node.left, node.right):
                    if child:
                        stack.append((child, False))
        return best[root]
