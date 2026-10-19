"""## Task

In an arbitrary binary tree, link each node to the immediate node on its right at the same
depth. Missing children must not interrupt the level chain.

## Hints

1. A completed level can act as its own traversal queue.
2. Build the next level while walking the current one.

## Approach

### Next-level chain builder

Walk the current level through next pointers. Append each existing left and right child after a
dummy next-level head, then advance to that newly built level.

### Breadth-first level linking

Process each fixed queue layer, linking the previously popped node to the current node.
Terminate the final node's next and enqueue children for the next layer.

## Why it works

### Next-level chain builder

The current chain orders parents left to right. Appending their existing children in left-right
order creates precisely the next level, including gaps, and a final null terminates it.

### Breadth-first level linking

BFS visits exactly one level left to right. Connecting consecutive visits therefore links
precisely immediate neighbors, and terminating after its fixed size prevents cross-level links.

## Walkthrough

For root 1 with children 2 and 3, set 2.next=3 and 3.next=None. The root's next remains None.

## Cost and pitfalls

Next-level chain builder: O(n) time; O(1) space.
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
    """Approach: Next-level chain builder
    Time: O(n)
    Space: O(1)
    """

    def connect(self, root: Node | None) -> Node | None:
        if root:
            root.next = None
        level = root
        while level:
            dummy = tail = Node()
            current = level
            while current:
                for child in (current.left, current.right):
                    if child:
                        tail.next = child
                        tail = child
                current = current.next
            tail.next = None
            level = dummy.next
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
