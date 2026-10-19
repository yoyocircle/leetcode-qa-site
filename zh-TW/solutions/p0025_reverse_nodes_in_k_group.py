"""## Task

Reverse the nodes in each complete group of k. Leave a final group shorter than k in its
original order. Values cannot be exchanged instead of nodes.

## Hints

1. Find the end of a complete group before changing any links.
2. Keep the following group head as the initial reversed tail.

## Approach

### Bounded pointer reversal

Locate the kth node after a group predecessor. Reverse exactly the links before its saved
successor, reconnect the group, and continue from the old group head.

### Per-group node stack

Collect up to k original nodes. Pop or traverse a complete group in reverse order; append an
incomplete final group unchanged.

## Why it works

### Bounded pointer reversal

Knowing the boundary guarantees that only complete groups change. Reversal points the old first
node at the untouched suffix and reconnects the previous prefix to the old last node.

### Per-group node stack

The buffer contains exactly the next k positions or the entire remaining suffix. Reversing only
full buffers matches the contract while retaining each original identity once.

## Walkthrough

For [1,2,3,4,5] and k=2, reverse [1,2] and [3,4], then retain [5], giving [2,1,4,3,5].

## Cost and pitfalls

Bounded pointer reversal: O(n) time; O(1) space.
Per-group node stack: O(n) time; O(k) space.
Both solutions mutate next pointers. The default meets the constant auxiliary-space follow-up;
the stack variant does not. Never partially reverse an undersized final group.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Bounded pointer reversal
    Time: O(n)
    Space: O(1)
    """

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummy = ListNode(next=head)
        before = dummy
        while True:
            end = before
            for _ in range(k):
                end = end.next
                if end is None:
                    return dummy.next
            following = end.next
            current = before.next
            previous = following
            while current is not following:
                saved = current.next
                current.next = previous
                previous, current = current, saved
            old_first = before.next
            before.next = end
            before = old_first


class GroupStackSolution:
    """Approach: Per-group node stack
    Time: O(n)
    Space: O(k)
    """

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummy = tail = ListNode()
        current = head
        while current:
            group = []
            while current and len(group) < k:
                group.append(current)
                current = current.next
            if len(group) < k:
                tail.next = group[0]
                break
            while group:
                tail.next = group.pop()
                tail = tail.next
            tail.next = current
        return dummy.next
