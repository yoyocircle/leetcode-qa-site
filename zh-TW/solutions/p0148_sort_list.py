"""## Task

Sort a singly linked list in ascending order. Reuse original nodes and provide an O(n log n)
default with constant auxiliary space.

## Hints

1. Merging two sorted chains requires only link changes.
2. Bottom-up merge sizes 1,2,4,... avoid recursive stack space.

## Approach

### Bottom-up linked merge sort

Count nodes, then merge adjacent fixed-width runs in repeated passes. Split runs by cutting
links and reconnect each merged run through a tail pointer.

### Sort buffered node references

Collect nodes, use Python's stable comparison sort on their values, then rebuild the next chain
in that order.

## Why it works

### Bottom-up linked merge sort

At the start of a width-w pass, every run of at most w nodes is sorted. Stable two-way merging
makes sorted runs of at most 2w; doubling eventually covers the whole list.

### Sort buffered node references

The sorted reference array is a stable ascending permutation of the original nodes. Reconnecting
it produces a sorted list without changing node values.

## Walkthrough

For [4,1,3,2], width-one merges give [1,4] and [2,3]. The width-two merge gives [1,2,3,4].

## Cost and pitfalls

Bottom-up linked merge sort: O(n log(n+1)) time; O(1) auxiliary space.
Sort buffered node references: O(n log(n+1)) time; O(n) space.
Both mutate links and preserve every original node and value. Only the default meets the
constant-space follow-up. Python sorting and node buffering require linear auxiliary references.
Iteration handles lists beyond recursion limits.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Bottom-up linked merge sort
    Time: O(n log(n+1))
    Space: O(1) auxiliary
    """

    def sortList(self, head: ListNode | None) -> ListNode | None:
        def split(first, width):
            if first is None:
                return None
            for _ in range(width - 1):
                if first.next is None:
                    break
                first = first.next
            following = first.next
            first.next = None
            return following

        length, current = 0, head
        while current:
            length += 1
            current = current.next
        dummy = ListNode(next=head)
        width = 1
        while width < length:
            tail, current = dummy, dummy.next
            while current:
                left = current
                right = split(left, width)
                current = split(right, width)
                while left and right:
                    if left.val <= right.val:
                        tail.next, left = left, left.next
                    else:
                        tail.next, right = right, right.next
                    tail = tail.next
                tail.next = left or right
                while tail.next:
                    tail = tail.next
            width *= 2
        return dummy.next


class BufferedSortSolution:
    """Approach: Sort buffered node references
    Time: O(n log(n+1))
    Space: O(n)
    """

    def sortList(self, head: ListNode | None) -> ListNode | None:
        ordered = []
        while head:
            ordered.append(head)
            head = head.next
        ordered.sort(key=lambda node: node.val)
        for index, node in enumerate(ordered):
            node.next = ordered[index + 1] if index + 1 < len(ordered) else None
        return ordered[0] if ordered else None
