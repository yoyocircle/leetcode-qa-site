"""## Task

Find the greatest sum of a nonempty simple path in a binary tree. The path may
begin and end anywhere, and values can all be negative.

## Hints

1. Distinguish a complete path through a node from a branch extendable to its parent.
2. A returned branch may use at most one child, but a complete path may use two.

## Approach

### Downward gain DP

Process nodes in iterative postorder. Save each node's best downward gain.
Clamp child gains at zero. Update the global answer with node+left+right,
but save only node+max(left,right) as the gain available to its parent.

### Enumerate all path starts

Build undirected tree adjacency, then walk from every starting node while accumulating sums.
This directly enumerates all simple paths and is useful as an oracle. Its quadratic time may
time out at full constraints.

## Why it works

### Downward gain DP

Every simple path has a unique highest node. At that node it consists of at
most one branch from each child, so the global update considers its best form.
Returning both branches upward would create a fork, which is not a simple path.

### Enumerate all path starts

A tree has one simple path between each pair of vertices. Traversing from every start therefore
considers every nonempty path, while avoiding the previous vertex prevents retracing an edge.

## Walkthrough

For root -5 with children 4 and 7, the complete path through the root sums
to 6. The best individual branch is 7, so return 7. An all-negative tree
returns its largest node value.

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(n) auxiliary storage for gains and traversal state. The tree is
unchanged. Initialize the global best to negative infinity, not zero. Iterative
postorder handles chains beyond Python's recursion limit.

Alternative tradeoff: O(n^2); educational baseline may time out time; O(n) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Downward gain DP
    Time: O(n)
    Space: O(n)
    """

    def maxPathSum(self, root: TreeNode) -> int:
        gains = {}
        stack = [(root, False)]
        best = float("-inf")
        while stack:
            node, expanded = stack.pop()
            if expanded:
                left = max(0, gains.get(node.left, 0))
                right = max(0, gains.get(node.right, 0))
                best = max(best, node.val + left + right)
                gains[node] = node.val + max(left, right)
                continue
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
        return int(best)


class EnumeratePathsSolution:
    """Approach: Enumerate all path starts
    Time: O(n^2); educational baseline may time out
    Space: O(n)
    """

    def maxPathSum(self, root: TreeNode) -> int:
        adjacency = {}
        stack = [root]
        while stack:
            node = stack.pop()
            adjacency.setdefault(node, [])
            for child in (node.left, node.right):
                if child:
                    adjacency[node].append(child)
                    adjacency.setdefault(child, []).append(node)
                    stack.append(child)
        best = float("-inf")
        for start in adjacency:
            pending = [(start, None, 0)]
            while pending:
                node, previous, total = pending.pop()
                total += node.val
                best = max(best, total)
                pending.extend(
                    (child, node, total) for child in adjacency[node] if child is not previous
                )
        return int(best)
