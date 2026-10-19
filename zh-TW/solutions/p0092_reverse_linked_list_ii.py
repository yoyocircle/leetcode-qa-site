"""## Task

Reverse only the inclusive one-based positions left through right in a linked list and return
its head. Bounds identify an existing nonempty segment.

## Hints

1. Locate the node just before the segment.
2. Repeatedly move the next segment node to its front.

## Approach

### Front insertion within segment

Walk a dummy predecessor to position left-1. Keep the original segment head as its tail and move
each following segment node immediately after the predecessor.

### Reverse reference slice

Collect all original nodes, reverse the selected array slice, then reconnect the entire
reference sequence. Python slice reversal copies references.

## Why it works

### Front insertion within segment

After each insertion, the processed prefix of the segment is reversed and the original first
node remains its tail. Exactly right-left moves reverse the full designated segment.

### Reverse reference slice

Only indices left-1 through right-1 change positions. Linking the resulting sequence preserves
every outside position and reverses exactly the chosen interval.

## Walkthrough

For [1,3,5,7,9] and bounds 2..4, move 5 then 7 to the segment front, obtaining [1,7,5,3,9].

## Cost and pitfalls

Front insertion within segment: O(right) time; O(1) space.
Reverse reference slice: O(n) time; O(n) space.
Both variants mutate links without changing values or creating replacement result nodes. A dummy
makes left=1 ordinary. The buffered alternative scans the whole list even for a short prefix
segment.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Front insertion within segment
    Time: O(right)
    Space: O(1)
    """

    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        dummy = ListNode(next=head)
        before = dummy
        for _ in range(left - 1):
            before = before.next
        tail = before.next
        for _ in range(right - left):
            moved = tail.next
            tail.next = moved.next
            moved.next = before.next
            before.next = moved
        return dummy.next


class BufferedSolution:
    """Approach: Reverse reference slice
    Time: O(n)
    Space: O(n)
    """

    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        order = []
        while head:
            order.append(head)
            head = head.next
        order[left - 1 : right] = order[left - 1 : right][::-1]
        for index, node in enumerate(order):
            node.next = order[index + 1] if index + 1 < len(order) else None
        return order[0]
