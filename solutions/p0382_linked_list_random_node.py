"""## Task

Given a nonempty linked list, return a uniformly random node value on every getRandom call
without changing the list.

## Hints

1. The length need not be known before the draw.
2. At the ith visited node, replace the current sample with probability 1/i.

## Approach

### Reservoir sampling

Retain the head and scan it for each draw. Replace the sampled value with the ith value when
randrange(i) is zero.

### Value snapshot and random indexing

Copy values to a dense array during construction and choose a uniform position for each draw.

## Why it works

### Reservoir sampling

Node i is selected with probability 1/i and survives each later replacement with probability
(j-1)/j. The product telescopes to 1/n for every node.

### Value snapshot and random indexing

Each original node contributes one array position, including equal values at distinct nodes.
Uniform index selection therefore gives every node equal probability.

## Walkthrough

For list [3,3,9], each node has probability one third, so the returned value is 3 with
probability two thirds.

## Cost and pitfalls

Reservoir sampling: O(1) constructor; O(n) getRandom time; O(1) space.
Value snapshot and random indexing: O(n) constructor; O(1) getRandom time; O(n) space.
The input list is unchanged and assumed stable after construction. The snapshot intentionally
copies values. Reservoir sampling meets the unknown-length, constant-extra-space follow-up; the
snapshot does not.
"""

from random import choice, randrange


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Reservoir sampling
    Time: O(1) constructor; O(n) getRandom
    Space: O(1)
    """

    def __init__(self, head: ListNode):
        self.head = head

    def getRandom(self) -> int:
        current = self.head
        count = 0
        selected = current.val
        while current:
            count += 1
            if randrange(count) == 0:
                selected = current.val
            current = current.next
        return selected


class SnapshotSolution:
    """Approach: Value snapshot and random indexing
    Time: O(n) constructor; O(1) getRandom
    Space: O(n)
    """

    def __init__(self, head: ListNode):
        self.values = []
        while head:
            self.values.append(head.val)
            head = head.next

    def getRandom(self) -> int:
        return choice(self.values)
