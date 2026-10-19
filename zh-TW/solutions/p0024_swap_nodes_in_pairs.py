"""## Task

Swap each adjacent pair of list nodes and return the new head. Rewire nodes rather than swapping
their values; an unmatched final node stays last.

## Hints

1. Keep a predecessor for the pair being changed.
2. A dummy predecessor also covers swapping the original head.

## Approach

### Local pair rewiring

Walk pairs after a dummy node. Save the first and second nodes, bypass the second, then link
second before first. Advance the predecessor to the old first.

### Buffered positional order

Collect node identities, exchange neighboring array entries, and rebuild links from that order.
This spends linear storage to make output positions explicit.

## Why it works

### Local pair rewiring

Each step exchanges exactly one adjacent pair and leaves the already processed prefix attached
to the untouched suffix.

### Buffered positional order

The array permutation exchanges precisely indices 0/1, 2/3, and so on. Reconnecting those
original identities preserves every value and node.

## Walkthrough

For [4,7,2], exchange 4 and 7, leaving the unmatched 2: [7,4,2].

## Cost and pitfalls

Local pair rewiring: O(n) time; O(1) space.
Buffered positional order: O(n) time; O(n) space.
Both variants mutate links and reuse original nodes. Terminate the final node to prevent stale
links. Empty and one-node lists are unchanged.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Local pair rewiring
    Time: O(n)
    Space: O(1)
    """

    def swapPairs(self, head: ListNode | None) -> ListNode | None:
        dummy = ListNode(next=head)
        before = dummy
        while before.next and before.next.next:
            first = before.next
            second = first.next
            first.next = second.next
            second.next = first
            before.next = second
            before = first
        return dummy.next


class BufferedSolution:
    """Approach: Buffered positional order
    Time: O(n)
    Space: O(n)
    """

    def swapPairs(self, head: ListNode | None) -> ListNode | None:
        order = []
        while head:
            order.append(head)
            head = head.next
        for index in range(0, len(order) - 1, 2):
            order[index], order[index + 1] = order[index + 1], order[index]
        for index, node in enumerate(order):
            node.next = order[index + 1] if index + 1 < len(order) else None
        return order[0] if order else None
