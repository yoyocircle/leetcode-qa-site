"""## Task

Merge k ascending linked lists into one ascending list. Some or all input lists
may be empty.

## Hints

1. The smallest unmerged node must be at the head of one remaining list.
2. A heap can maintain those k candidates without repeatedly scanning them.

## Approach

### Heap of list heads

Heapify one head per nonempty list. Pop the smallest node, append it to the
result, and push its successor from the same list. Heap entries include the
source list index to break equal-value ties without comparing node objects.

### Pairwise merging

Copy the head array and merge adjacent pairs of sorted chains in rounds. Each round halves the
number of chains. Rewire original nodes, while leaving the caller's list-of-heads array
unchanged.

## Why it works

### Heap of list heads

Each heap entry is its list's smallest remaining node. Their minimum is therefore
the global smallest unmerged node. Replacing it with its successor restores the
invariant, so repeated extraction builds a sorted list containing every node.

### Pairwise merging

Two-way merging always chooses the smaller front node and preserves every node. By induction
each round produces sorted unions of disjoint input groups; after logarithmically many rounds
the single chain contains all nodes.

## Walkthrough

For [1,4], [1,3], and [2], heap heads begin as 1,1,2. After extracting
the two 1s, their successors 4 and 3 join 2. Output is [1,1,2,3,4].

## Cost and pitfalls

Default approach costs and behavior:

O(k + N log(k+1)) time and O(k) space for N total nodes. Reuses nodes and
mutates their next links; this is not a persistent copy. Heap tuples containing
only (value,node) fail on duplicate values because nodes are not orderable.

Alternative tradeoff: O(k + N log(k+1)) time; O(k) space.
"""

from heapq import heapify, heappop, heappush


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Heap of list heads
    Time: O(k + N log(k+1))
    Space: O(k)
    """

    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
        heapify(heap)
        dummy = tail = ListNode()
        while heap:
            _, i, node = heappop(heap)
            tail.next = node
            tail = node
            if node.next:
                heappush(heap, (node.next.val, i, node.next))
        return dummy.next


class PairwiseMergeSolution:
    """Approach: Pairwise merging
    Time: O(k + N log(k+1))
    Space: O(k)
    """

    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        current = list(lists)
        while len(current) > 1:
            merged = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else None
                dummy = tail = ListNode()
                while left and right:
                    if left.val <= right.val:
                        tail.next, left = left, left.next
                    else:
                        tail.next, right = right, right.next
                    tail = tail.next
                tail.next = left if left else right
                merged.append(dummy.next)
            current = merged
        return current[0] if current else None
