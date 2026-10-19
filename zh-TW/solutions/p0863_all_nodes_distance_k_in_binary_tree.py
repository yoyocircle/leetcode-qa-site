"""## Task

Return values of all original tree nodes at edge distance k from a supplied target node. Result
order is arbitrary and the target is identified by object identity.

## Hints

1. Adding parent links turns the tree into an undirected traversal problem.
2. Alternatively split answers across ancestors of the target and their off-path subtrees.

## Approach

### Parent map and distance BFS

Build a parent map iteratively, then BFS outward from target through left, right, and parent
links. Stop after k layers.

### Ancestor path and excluded-branch searches

Find the root-to-target path with explicit DFS enter/exit frames. For each ancestor distance d
upward, search depth k-d downward while excluding the child leading back toward target.

## Why it works

### Parent map and distance BFS

The augmented graph contains exactly the original undirected tree edges. BFS reaches nodes in
increasing edge distance, so the kth frontier is precisely the required set.

### Ancestor path and excluded-branch searches

Every node's route from target has one highest ancestor on that path. Its off-path subtree is
searched only for that ancestor, so branches partition possible answers without duplication.

## Walkthrough

For root 5 with children 2 and 8 and target 2, k=1 returns values 5 and any children of 2. For
k=0 return only 2.

## Cost and pitfalls

Parent map and distance BFS: O(n) time; O(n) space.
Ancestor path and excluded-branch searches: O(n) time; O(h) auxiliary plus output space.
The tree is unchanged. Value equality cannot substitute for target identity. The ancestor
variant avoids a full parent map; excluded subtree regions are disjoint, keeping total work
linear. A distance beyond the tree diameter yields no values.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Parent map and distance BFS
    Time: O(n)
    Space: O(n)
    """

    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        parents = {root: None}
        stack = [root]
        while stack:
            node = stack.pop()
            for child in (node.left, node.right):
                if child:
                    parents[child] = node
                    stack.append(child)
        queue = deque([target])
        seen = {target}
        for _ in range(k):
            if not queue:
                return []
            for _ in range(len(queue)):
                node = queue.popleft()
                for neighbor in (node.left, node.right, parents[node]):
                    if neighbor and neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
        return [node.val for node in queue]


class AncestorBranchesSolution:
    """Approach: Ancestor path and excluded-branch searches
    Time: O(n)
    Space: O(h) auxiliary plus output
    """

    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        path = []
        stack = [(root, False)]
        while stack:
            node, exiting = stack.pop()
            if exiting:
                path.pop()
                continue
            path.append(node)
            if node is target:
                break
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
        result = []
        excluded = None
        for upward, ancestor in enumerate(reversed(path)):
            remaining = k - upward
            if remaining < 0:
                break
            pending = [(ancestor, remaining)]
            while pending:
                node, depth = pending.pop()
                if depth == 0:
                    result.append(node.val)
                    continue
                for child in (node.left, node.right):
                    if child and child is not excluded:
                        pending.append((child, depth - 1))
            excluded = ancestor
        return result
