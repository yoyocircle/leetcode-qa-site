"""## Task

Group nodes at odd one-based positions before nodes at even positions, preserving order within
both groups. Positions, not node values, determine parity.

## Hints

1. The first and second nodes start two interleaved chains.
2. Save the even head so the completed odd tail can reconnect to it.

## Approach

### Split interleaved position chains

Advance odd and even tails by bypassing alternating nodes. After the even chain ends, append its
saved head after the odd tail.

### Position-indexed reference groups

Enumerate original nodes into odd/even reference arrays, concatenate them, and reconnect their
next pointers.

## Why it works

### Split interleaved position chains

Every bypass connects consecutive nodes of the same positional parity. Thus the two chains
contain exactly the odd and even original positions in their original order.

### Position-indexed reference groups

The enumeration index directly expresses the required parity. Stable collection and
concatenation yield the requested permutation of original identities.

## Walkthrough

For [8,3,7,2,9], odd positions hold [8,7,9] and even positions [3,2], giving [8,7,9,3,2].

## Cost and pitfalls

Split interleaved position chains: O(n) time; O(1) space.
Position-indexed reference groups: O(n) time; O(n) space.
Both mutate links and preserve values and identities. The buffered variant misses the
constant-space requirement and is an educational alternative. Empty and one-node lists need no
reordering.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Split interleaved position chains
    Time: O(n)
    Space: O(1)
    """

    def oddEvenList(self, head: ListNode | None) -> ListNode | None:
        if head is None:
            return None
        odd, even = head, head.next
        even_head = even
        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        odd.next = even_head
        return head


class BufferedSolution:
    """Approach: Position-indexed reference groups
    Time: O(n)
    Space: O(n)
    """

    def oddEvenList(self, head: ListNode | None) -> ListNode | None:
        groups = [[], []]
        index = 0
        while head:
            groups[index % 2].append(head)
            head = head.next
            index += 1
        ordered = groups[0] + groups[1]
        for index, node in enumerate(ordered):
            node.next = ordered[index + 1] if index + 1 < len(ordered) else None
        return ordered[0] if ordered else None
