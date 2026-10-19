"""## Task

Find the lowest node that is an ancestor of both supplied nodes in a binary tree.
A node counts as its own ancestor, and both targets are guaranteed present.

## Hints

1. A parent map lets you move upward without changing tree nodes.
2. Find the first ancestor of one target that also belongs to the other's chain.

## Approach

### Parent chains

Traverse iteratively until both targets have parent entries. Collect all ancestors
of p, including p. Walk q upward and return its first member of that set.

### Postorder target masks

Process iterative postorder and record a two-bit mask per subtree: one bit for each target
identity. The first completed subtree with both bits identifies the answer. Values are never
used as identities.

## Why it works

### Parent chains

Each node has one path to the root. Their common ancestors form the shared upper
part of those paths. Walking from q upward reaches the deepest shared node first,
which is exactly the lowest common ancestor.

### Postorder target masks

A subtree mask is the union of its children's masks and its own target bits. The first mask
containing both targets belongs to their deepest shared ancestor because both children were
completed first.

## Walkthrough

If root 8 has left child 3 and 3 has child 6, choosing p=3 and q=6 gives
ancestor set {3,8}. Q's walk reaches 3 first, so return that original node.

## Cost and pitfalls

Default approach costs and behavior:

Expected O(n) time and O(n) space; the tree is unchanged. Compare node identity,
not newly constructed nodes with matching values. A target can itself be the
answer. The iterative parent map avoids recursion-limit failures at large depths.

Alternative tradeoff: O(n) time; O(n) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Parent chains
    Time: O(n) expected
    Space: O(n)
    """

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        parent = {root: None}
        stack = [root]
        while p not in parent or q not in parent:
            node = stack.pop()
            for child in (node.left, node.right):
                if child:
                    parent[child] = node
                    stack.append(child)
        ancestors = set()
        while p:
            ancestors.add(p)
            p = parent[p]
        while q not in ancestors:
            q = parent[q]
        return q


class PostorderTargetsSolution:
    """Approach: Postorder target masks
    Time: O(n)
    Space: O(n)
    """

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        masks = {}
        stack = [(root, False)]
        answer = None
        while stack:
            node, expanded = stack.pop()
            if expanded:
                mask = masks.get(node.left, 0) | masks.get(node.right, 0)
                mask |= int(node is p) | (int(node is q) << 1)
                masks[node] = mask
                if mask == 3 and answer is None:
                    answer = node
            else:
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))
        return answer
