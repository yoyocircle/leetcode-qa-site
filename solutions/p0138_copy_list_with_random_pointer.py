"""## Task

Deep-copy a linked list whose nodes have next and random pointers. A random
pointer may refer to any node in the list, including itself, or to None.

## Hints

1. Every original node needs one stable corresponding copy.
2. Allocate all copies before wiring references that may point forward.

## Approach

### Identity map

Use a dictionary from original node identity to copied node, including None
mapping to None. The first pass allocates nodes; the second connects copied next
and random references by dictionary lookup.

### Interleaved copies

Insert each clone directly after its original. A random target's next link now identifies its
clone. Wire random links, then separate the alternating chains and restore every original next
pointer. This temporarily mutates the input during the call.

## Why it works

### Identity map

The map is a one-to-one correspondence between original and new nodes. Translating
each edge through that map preserves the entire pointer structure while ensuring
every non-null returned reference belongs to the copy.

### Interleaved copies

Alternation supplies the original-to-copy correspondence without a dictionary. All random edges
are translated before separation; restoring alternate next links recovers the original chain and
leaves a disjoint copied chain.

## Walkthrough

Let A(value 4) point next to B(value 4), with A.random=B and B.random=A.
Create distinct A' and B', then set A'.next=B', A'.random=B', B'.random=A'.
Equal values do not make A and B the same node.

## Cost and pitfalls

Default approach costs and behavior:

Expected O(n) time and O(n) map space, plus O(n) output nodes. Input pointers are
unchanged. Key by object identity, not value. A shallow copy that reuses original
random targets violates the deep-copy contract. An empty list returns None.

Alternative tradeoff: O(n) time; O(1) auxiliary; O(n) output space.
"""


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


class Solution:
    """Approach: Identity map
    Time: O(n) expected
    Space: O(n) auxiliary and output
    """

    def copyRandomList(self, head: Node | None) -> Node | None:
        copies = {None: None}
        current = head
        while current:
            copies[current] = Node(current.val)
            current = current.next
        current = head
        while current:
            copies[current].next = copies[current.next]
            copies[current].random = copies[current.random]
            current = current.next
        return copies[head]


class InterleavedCopiesSolution:
    """Approach: Interleaved copies
    Time: O(n)
    Space: O(1) auxiliary; O(n) output
    """

    def copyRandomList(self, head: Node | None) -> Node | None:
        current = head
        while current:
            current.next = Node(current.val, current.next)
            current = current.next.next
        current = head
        while current:
            current.next.random = current.random.next if current.random else None
            current = current.next.next
        dummy = tail = Node()
        current = head
        while current:
            copy = current.next
            current.next = copy.next
            tail.next = copy
            tail = copy
            current = current.next
        tail.next = None
        return dummy.next
