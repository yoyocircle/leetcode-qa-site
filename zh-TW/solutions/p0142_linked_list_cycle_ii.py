"""## Task

Return the original node where a singly linked list cycle begins, or None when no cycle exists.
The list must remain unchanged.

## Hints

1. A slow and fast pointer meet inside any reachable cycle.
2. After meeting, move one pointer back to the head and advance both one step at a time.

## Approach

### Floyd meeting and entry recovery

Detect a meeting with one-step and two-step pointers. Restart one pointer at head and walk both
equally until they coincide at the cycle entrance.

### First repeated node identity

Record visited node objects while following next links. Return the first node encountered a
second time.

## Why it works

### Floyd meeting and entry recovery

If the noncyclic prefix has length a and cycle length c, the meeting displacement is congruent
to -a modulo c. Advancing both by a steps from head and meeting therefore reaches the entrance
simultaneously.

### First repeated node identity

Before repetition the traversal has followed the unique prefix and one pass through the cycle.
Its first repeated identity is precisely the entry, independently of repeated node values.

## Walkthrough

For A->B->C->D->B, Floyd eventually meets inside B,C,D. Entry recovery returns the original B,
not a new node with its value.

## Cost and pitfalls

Floyd meeting and entry recovery: O(n) time; O(1) space.
First repeated node identity: O(n) expected time; O(n) space.
Neither solution mutates links or values. Empty and one-node acyclic lists return None; a
self-loop returns that node. Comparing values would misidentify repeated values in an acyclic
list.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Floyd meeting and entry recovery
    Time: O(n)
    Space: O(1)
    """

    def detectCycle(self, head: ListNode | None) -> ListNode | None:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                entry = head
                while entry is not slow:
                    entry = entry.next
                    slow = slow.next
                return entry
        return None


class IdentitySetSolution:
    """Approach: First repeated node identity
    Time: O(n) expected
    Space: O(n)
    """

    def detectCycle(self, head: ListNode | None) -> ListNode | None:
        seen = set()
        while head:
            if head in seen:
                return head
            seen.add(head)
            head = head.next
        return None
