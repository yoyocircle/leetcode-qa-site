"""## Task

Implement an iterator returning BST values in ascending order through next() and reporting
whether another value exists with hasNext(). Calls to next are valid.

## Hints

1. Inorder traversal is sorted for a BST.
2. Save just the unfinished left descent to support lazy iteration.

## Approach

### Lazy inorder stack

Push the root's left chain initially. Next pops one node, then pushes its right subtree's left
chain. HasNext checks whether the stack is nonempty.

### Materialized inorder snapshot

Collect an iterative inorder array at construction and advance an index for subsequent
operations. This spends more startup work and storage for constant-time individual queries.

## Why it works

### Lazy inorder stack

The stack top is always the smallest unvisited node. Its left descendants are complete; after
visiting it, the right subtree's left chain supplies the next candidates.

### Materialized inorder snapshot

The snapshot stores every node value in exact inorder once. Reading consecutive indices
therefore yields precisely the ascending iteration sequence.

## Walkthrough

A BST containing [1,3,6] in sorted order returns 1, then 3, then 6. HasNext becomes false after
the third next.

## Cost and pitfalls

Lazy inorder stack: O(h) constructor; O(1) amortized next; O(1) hasNext time; O(h) space.
Materialized inorder snapshot: O(n) constructor; O(1) next and hasNext time; O(n) space.
The tree is unchanged and is assumed stable during iteration. The snapshot variant misses the
O(h)-space follow-up. Lazy next is amortized constant time, not worst-case constant for a single
call.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    """Approach: Lazy inorder stack
    Time: O(h) constructor; O(1) amortized next; O(1) hasNext
    Space: O(h)
    """

    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


class SnapshotBSTIterator:
    """Approach: Materialized inorder snapshot
    Time: O(n) constructor; O(1) next and hasNext
    Space: O(n)
    """

    def __init__(self, root: TreeNode):
        self.values = []
        stack, current = [], root
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            self.values.append(current.val)
            current = current.right
        self.index = 0

    def next(self) -> int:
        value = self.values[self.index]
        self.index += 1
        return value

    def hasNext(self) -> bool:
        return self.index < len(self.values)
