"""## Task

Rotate a linked list right by k places. Rotation wraps nodes at the end back to the beginning; k
may greatly exceed the list length.

## Hints

1. Reduce k modulo the length.
2. A temporary cycle lets one cut describe the entire rotation.

## Approach

### Circularize then cut

Find the tail and length. Join tail to head, advance to the new tail at length-k-1, and break
its outgoing link. Return the successor saved before the break.

### Reorder node references

Collect node references, rotate the array using two slices, then rewrite next pointers in the
resulting order.

## Why it works

### Circularize then cut

A rotation preserves cyclic order and changes only the chosen starting point. Cutting
immediately before the last k nodes makes exactly those nodes the new prefix.

### Reorder node references

Array slicing places the last k references first and preserves order within both sections.
Linking that sequence realizes exactly the requested rotation.

## Walkthrough

For [2,4,6,8] and k=6, use k modulo 4 = 2 and return [6,8,2,4].

## Cost and pitfalls

Circularize then cut: O(n) time; O(1) space.
Reorder node references: O(n) time; O(n) space.
Both variants mutate links and retain node identities and values. The buffered version copies
references, not nodes. Handle an empty list before modulo; k=0 needs no rewiring.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Circularize then cut
    Time: O(n)
    Space: O(1)
    """

    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
        if head is None:
            return None
        tail, length = head, 1
        while tail.next:
            tail = tail.next
            length += 1
        k %= length
        if k == 0:
            return head
        tail.next = head
        before = head
        for _ in range(length - k - 1):
            before = before.next
        result = before.next
        before.next = None
        return result


class BufferedSolution:
    """Approach: Reorder node references
    Time: O(n)
    Space: O(n)
    """

    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
        order = []
        while head:
            order.append(head)
            head = head.next
        if not order:
            return None
        k %= len(order)
        order = order[-k:] + order[:-k] if k else order
        for index, node in enumerate(order):
            node.next = order[index + 1] if index + 1 < len(order) else None
        return order[0]
