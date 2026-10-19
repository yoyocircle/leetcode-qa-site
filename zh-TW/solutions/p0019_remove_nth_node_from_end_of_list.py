"""## Task

Remove the nth node counting backward from a singly linked list's end, and return
the resulting head. The supplied n is valid.

## Hints

1. Keep a gap of n nodes between two pointers.
2. A dummy node makes removing the original head an ordinary link update.

## Approach

### Fixed pointer gap

Start fast and slow at a dummy predecessor. Advance fast n times, then move both
until fast is the last node. Slow now precedes the node to remove; bypass it
and return dummy.next.

### Count then unlink

Count the list length, then walk length-n links from a dummy predecessor and bypass the
following node. This uses two passes instead of maintaining a moving gap.

## Why it works

### Fixed pointer gap

The distance between fast and slow stays n. When fast reaches the last node,
slow is therefore exactly n positions before it, which is the predecessor of
the nth-from-end node. Bypassing one link removes precisely that node.

### Count then unlink

The nth node from the end has zero-based index length-n from the head. Walking that many
predecessor links from the dummy locates exactly its incoming link.

## Walkthrough

For [4,5,6] and n=3, fast reaches 6 before the paired walk starts.
Slow remains at dummy, so bypass 4 and return [5,6].

## Cost and pitfalls

Default approach costs and behavior:

O(length) time and O(1) space. The original list's links are modified; remaining
nodes are reused. Advancing n versus n+1 steps depends on the chosen stopping
condition. Here the paired loop checks fast.next, not fast. A single-node list
with n=1 returns None.

Alternative tradeoff: O(n) time; O(1) space.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Fixed pointer gap
    Time: O(n)
    Space: O(1)
    """

    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode | None:
        dummy = ListNode(next=head)
        slow = fast = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return dummy.next


class LengthPassSolution:
    """Approach: Count then unlink
    Time: O(n)
    Space: O(1)
    """

    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode | None:
        length = 0
        current = head
        while current:
            length += 1
            current = current.next
        dummy = ListNode(next=head)
        before = dummy
        for _ in range(length - n):
            before = before.next
        before.next = before.next.next
        return dummy.next
