"""## Task

Flatten a multilevel doubly linked list in place. Visit a node's entire child list before its
original next node, clear every child link, and maintain reciprocal prev/next links.

## Hints

1. The required order is depth-first preorder.
2. Save the original next chain before descending into a child.

## Approach

### Explicit deferred-next stack

Use a preorder stack, pushing next before child. Append each popped original node to a new
traversal chain by rewriting next and prev, and clear child.

### Splice child lists in place

When a child exists, find the last node of that still-unflattened child-level chain. Attach the
saved next chain after it, move the child after its parent, clear child, and continue through
next.

## Why it works

### Explicit deferred-next stack

The stack visits children before saved siblings. Linking consecutive visits gives exactly the
required flattened order while preserving every original identity and reciprocal adjacency.

### Splice child lists in place

Splicing places the whole child chain before the original suffix. Later child splices refine its
interior in the same preorder. Each original same-level edge is scanned in at most one
child-tail search, giving linear total work.

## Walkthrough

For 1<->2<->3 with 2.child pointing to 4<->5, flatten to 1<->2<->4<->5<->3, with all child
pointers None.

## Cost and pitfalls

Explicit deferred-next stack: O(n) time; O(n) worst space.
Splice child lists in place: O(n) amortized time; O(1) space.
Both mutate and reuse all nodes, including prev links. The returned head has prev=None and the
final tail has next=None. Iteration supports deep child nesting without recursion.
"""


class Node:
    def __init__(self, val=0, prev=None, next=None, child=None):
        self.val, self.prev, self.next, self.child = val, prev, next, child


class Solution:
    """Approach: Explicit deferred-next stack
    Time: O(n)
    Space: O(n) worst
    """

    def flatten(self, head: "Node | None") -> "Node | None":
        stack = [head] if head else []
        previous = None
        while stack:
            node = stack.pop()
            if node.next:
                stack.append(node.next)
            if node.child:
                stack.append(node.child)
            node.prev = previous
            if previous:
                previous.next = node
            node.child = None
            previous = node
        if previous:
            previous.next = None
        return head


class SpliceSolution:
    """Approach: Splice child lists in place
    Time: O(n) amortized
    Space: O(1)
    """

    def flatten(self, head: "Node | None") -> "Node | None":
        if head:
            head.prev = None
        current = head
        while current:
            if current.child:
                first = current.child
                last = first
                while last.next:
                    last = last.next
                last.next = current.next
                if current.next:
                    current.next.prev = last
                current.next = first
                first.prev = current
                current.child = None
            current = current.next
        return head
