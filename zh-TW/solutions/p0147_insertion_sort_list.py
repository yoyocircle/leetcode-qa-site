"""## Task

Sort a linked list in ascending order using insertion sort. Move original nodes rather than
replacing their values or allocating a copied output list.

## Hints

1. Insert the next unsorted node into an already sorted prefix.
2. An array can binary-search insertion positions, although Python insertion still shifts
   references.

## Approach

### Linked sorted-prefix insertion

Detach each next input node, scan a dummy-headed sorted chain to its insertion point, and splice
it there. Insert after existing equals for stability.

### Binary insertion of node references

Maintain a sorted node-reference array. Binary-search each value's upper insertion boundary,
insert its reference, and finally reconnect the array order.

## Why it works

### Linked sorted-prefix insertion

The prefix starts empty and remains sorted after inserting at the first greater value. Each
original node enters once, so the final chain is a stable sorted permutation.

### Binary insertion of node references

The upper boundary places each node after earlier equal nodes and before greater values.
Induction maintains sorted stable order; final relinking preserves all node identities.

## Walkthrough

For values [4,2,3], insert 4 into empty, then 2 before 4, then 3 between them, giving [2,3,4].

## Cost and pitfalls

Linked sorted-prefix insertion: O(n^2) worst time; O(1) space.
Binary insertion of node references: O(n^2) worst time; O(n) space.
Both mutate next pointers and preserve values. The array variant reduces comparison search to
logarithmic work but not total insertion cost, because list.insert shifts references. Its final
tail must point to None.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Linked sorted-prefix insertion
    Time: O(n^2) worst
    Space: O(1)
    """

    def insertionSortList(self, head: ListNode | None) -> ListNode | None:
        dummy = ListNode()
        while head:
            following = head.next
            before = dummy
            while before.next and before.next.val <= head.val:
                before = before.next
            head.next = before.next
            before.next = head
            head = following
        return dummy.next


class BinaryInsertionSolution:
    """Approach: Binary insertion of node references
    Time: O(n^2) worst
    Space: O(n)
    """

    def insertionSortList(self, head: ListNode | None) -> ListNode | None:
        ordered = []
        while head:
            low, high = 0, len(ordered)
            while low < high:
                middle = (low + high) // 2
                if ordered[middle].val <= head.val:
                    low = middle + 1
                else:
                    high = middle
            ordered.insert(low, head)
            head = head.next
        for index, node in enumerate(ordered):
            node.next = ordered[index + 1] if index + 1 < len(ordered) else None
        return ordered[0] if ordered else None
