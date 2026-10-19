"""## Task

In a perfect binary tree, set each node's next pointer to its immediate right neighbor on the
same level, or None at the level end.

## Hints

1. A completed level can act as its own traversal queue.
2. Build the next level while walking the current one.

## Approach

### Perfect-tree neighbor links

Walk each level through next pointers already established above. Link a parent's left child to
its right, then its right child to the next parent's left child.

### Breadth-first level linking

Process each fixed queue layer, linking the previously popped node to the current node.
Terminate the final node's next and enqueue children for the next layer.

## Why it works

### Perfect-tree neighbor links

Every perfect-tree level has both children for every parent. These two link types connect every
consecutive pair in the next level, preserving the level-chain invariant.

### Breadth-first level linking

BFS visits exactly one level left to right. Connecting consecutive visits therefore links
precisely immediate neighbors, and terminating after its fixed size prevents cross-level links.

## Walkthrough

For root 1 with children 2 and 3, set 2.next=3 and 3.next=None. The root's next remains None.

## Cost and pitfalls

Perfect-tree neighbor links: O(n) time; O(1) space.
Breadth-first level linking: O(n) time; O(w) space.
Both mutate only next pointers, retain node identities, and return the original root. Left and
right edges are unchanged. The queue alternative misses the constant-space follow-up. Empty
trees return None.
"""

from collections import deque


class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val, self.left, self.right, self.next = val, left, right, next


class Solution:
    """Approach: Perfect-tree neighbor links
    Time: O(n)
    Space: O(1)
    """

    def connect(self, root: Node | None) -> Node | None:
        if root is None:
            return None
        root.next = None
        level = root
        while level.left:
            parent = level
            while parent:
                parent.left.next = parent.right
                parent.right.next = parent.next.left if parent.next else None
                parent = parent.next
            level = level.left
        return root


class QueueSolution:
    """Approach: Breadth-first level linking
    Time: O(n)
    Space: O(w)
    """

    def connect(self, root: Node | None) -> Node | None:
        queue = deque([root]) if root else deque()
        while queue:
            previous = None
            for _ in range(len(queue)):
                node = queue.popleft()
                if previous:
                    previous.next = node
                previous = node
                for child in (node.left, node.right):
                    if child:
                        queue.append(child)
            previous.next = None
        return root
