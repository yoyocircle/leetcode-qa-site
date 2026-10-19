"""## Task

From a sorted linked list, remove every value that occurs more than once. Retain only nodes
whose value occurs exactly once.

## Hints

1. Sorted duplicates form one consecutive run.
2. Keep the predecessor fixed when discarding an entire duplicate run.

## Approach

### Skip duplicate runs

Scan each maximal equal-value run. Attach its node only when the run has one member; otherwise
bypass the whole run from the previous retained node.

### Count then filter

Count values in a first pass. In a second pass, append only original nodes with count one and
terminate the result. This avoids relying on run boundaries but uses a map.

## Why it works

### Skip duplicate runs

Sorted order guarantees that a value occurs in exactly one run. A singleton run is therefore
exactly a globally unique value, so retaining only those runs is sufficient.

### Count then filter

The frequency predicate directly expresses global uniqueness. Filtering in original order
preserves sorting and includes precisely the nodes required.

## Walkthrough

For [1,2,2,3,4,4], remove both 2 nodes and both 4 nodes, leaving [1,3].

## Cost and pitfalls

Skip duplicate runs: O(n) time; O(1) space.
Count then filter: O(n) expected time; O(n) space.
Both variants mutate next links and reuse retained nodes. Removing only extra copies would solve
a different problem. A repeated prefix may remove the original head.
"""

from collections import Counter


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Skip duplicate runs
    Time: O(n)
    Space: O(1)
    """

    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        dummy = ListNode(next=head)
        before = dummy
        while head:
            end = head.next
            while end and end.val == head.val:
                end = end.next
            if head.next is end:
                before = head
            else:
                before.next = end
            head = end
        return dummy.next


class FrequencySolution:
    """Approach: Count then filter
    Time: O(n) expected
    Space: O(n)
    """

    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        counts = Counter()
        current = head
        while current:
            counts[current.val] += 1
            current = current.next
        dummy = tail = ListNode()
        while head:
            following = head.next
            if counts[head.val] == 1:
                tail.next = head
                tail = head
            head = following
        tail.next = None
        return dummy.next
