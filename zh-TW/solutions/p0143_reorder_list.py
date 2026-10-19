"""## Task

Rewire a list into alternating first, last, second, second-last order. Change the
existing links in place, preserve node values, and return nothing.

## Hints

1. Split the list near its middle.
2. Reverse the second half, then weave the two halves together.

## Approach

### Split reverse weave

Slow and fast pointers find the first half's last node. Detach its successor,
reverse that second half iteratively, then alternate one node from each half.
The first half is at least as long, simplifying the final merge.

### Node deque

Collect original nodes in a deque. Repeatedly attach its first and last remaining nodes, then
terminate the final tail. Buffering makes the requested positional order explicit at the cost of
extra storage.

## Why it works

### Split reverse weave

The first half supplies original nodes in forward order and the reversed half
supplies the remaining nodes in backward order. Alternating them creates exactly
the required sequence. Detaching before reversal prevents links between the two
working chains.

### Node deque

Each deque removal chooses the next required first or last unused original position. Removing
each node once preserves all identities; terminating the tail removes any stale link that could
make a cycle.

## Walkthrough

For [1,2,3,4,5], split into [1,2,3] and [4,5], reverse the latter to
[5,4], then weave to obtain [1,5,2,4,3].

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(1) auxiliary space. Mutates links and reuses every original node;
values are unchanged. Save next pointers before rewiring. Forgetting to detach
the halves can create a cycle. Odd and even lengths need separate mental traces.

Alternative tradeoff: O(n) time; O(n) space.
"""

from collections import deque


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Split reverse weave
    Time: O(n)
    Space: O(1)
    """

    def reorderList(self, head: ListNode) -> None:
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        current = slow.next
        slow.next = None
        second = None
        while current:
            following = current.next
            current.next = second
            second, current = current, following
        first = head
        while second:
            first_next, second_next = first.next, second.next
            first.next = second
            second.next = first_next
            first, second = first_next, second_next


class BufferedNodesSolution:
    """Approach: Node deque
    Time: O(n)
    Space: O(n)
    """

    def reorderList(self, head: ListNode) -> None:
        remaining = deque()
        current = head
        while current:
            remaining.append(current)
            current = current.next
        tail = ListNode()
        while remaining:
            tail.next = remaining.popleft()
            tail = tail.next
            if remaining:
                tail.next = remaining.pop()
                tail = tail.next
        tail.next = None
