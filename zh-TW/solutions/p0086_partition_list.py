"""## Task

Stably partition a linked list around x: nodes with values below x precede all others,
preserving original relative order within both groups.

## Hints

1. Build one chain for each side of the comparison.
2. Save each next pointer before rewiring, then terminate the second chain.

## Approach

### Two stable linked chains

Append original nodes to small and large chains behind dummy heads. Connect the small tail to
the large head after the scan.

### Stable node-reference partition

Collect references into two arrays according to the comparison, concatenate them, and reconnect
consecutive nodes.

## Why it works

### Two stable linked chains

Each chain receives its eligible nodes in original scan order. Concatenation therefore satisfies
both the partition predicate and stability without changing identities.

### Stable node-reference partition

Filtering preserves order within each array. Relinking their concatenation realizes exactly the
desired stable partition with every original node once.

## Walkthrough

For [3,1,4,2,3] and x=3, return [1,2,3,4,3], retaining the two original 3 nodes in their
original order.

## Cost and pitfalls

Two stable linked chains: O(n) time; O(1) space.
Stable node-reference partition: O(n) time; O(n) space.
Both variants mutate next pointers and reuse every original node. Values do not change. Clear
the final tail link; otherwise an old link from the large group can create a cycle.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Two stable linked chains
    Time: O(n)
    Space: O(1)
    """

    def partition(self, head: ListNode | None, x: int) -> ListNode | None:
        small = small_tail = ListNode()
        large = large_tail = ListNode()
        while head:
            following = head.next
            if head.val < x:
                small_tail.next = head
                small_tail = head
            else:
                large_tail.next = head
                large_tail = head
            head = following
        large_tail.next = None
        small_tail.next = large.next
        return small.next


class BufferedSolution:
    """Approach: Stable node-reference partition
    Time: O(n)
    Space: O(n)
    """

    def partition(self, head: ListNode | None, x: int) -> ListNode | None:
        small, large = [], []
        while head:
            (small if head.val < x else large).append(head)
            head = head.next
        ordered = small + large
        for index, node in enumerate(ordered):
            node.next = ordered[index + 1] if index + 1 < len(ordered) else None
        return ordered[0] if ordered else None
