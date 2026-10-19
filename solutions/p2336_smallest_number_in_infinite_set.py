"""## Task

Model the set of every positive integer. popSmallest removes and returns its smallest present
number; addBack restores a positive integer if it was removed.

## Hints

1. Numbers beyond the next never-popped frontier are implicitly present.
2. Only restored values below that frontier need explicit priority storage.

## Approach

### Implicit frontier and restored min-heap

Keep a frontier starting at one plus a heap and membership set of restored smaller numbers. Pop
the heap first, otherwise consume the frontier. AddBack inserts only removed-frontier-side
values not already queued.

### Finite removed-set complement

Store only currently removed integers. To pop, scan positive integers from one until finding one
absent from that set; addBack discards its argument from the removed set.

## Why it works

### Implicit frontier and restored min-heap

All values at least the frontier remain present, while all smaller present values are exactly
the restoration heap. Its minimum, or the frontier when empty, is therefore the global minimum.

### Finite removed-set complement

The represented infinite set is exactly the complement of the finite removed set among positive
integers. The first absent removed-set member is precisely its smallest present number.

## Walkthrough

Pop 1, then 2, restore 1, and pop again: the result is 1. The following pop returns 3 because 2
remains removed.

## Cost and pitfalls

Implicit frontier and restored min-heap: O(log(a+1)) expected amortized pop/addBack; O(1)
frontier pop time; O(a) space.
Finite removed-set complement: O(r+1) expected popSmallest; O(1) expected addBack time; O(r)
space.
Objects own finite state; neither approach invents a fixed upper universe bound. a and r are
peak stored restored-set and removed-set sizes; Python sets can retain capacity after deletions.
Repeated addBack is idempotent. The scan baseline trades simpler representation for repeated
prefix scans.
"""

from heapq import heappop, heappush


class SmallestInfiniteSet:
    """Approach: Implicit frontier and restored min-heap
    Time: O(log(a+1)) expected amortized pop/addBack; O(1) frontier pop
    Space: O(a)
    """

    def __init__(self):
        self.frontier = 1
        self.restored = []
        self.queued = set()

    def popSmallest(self) -> int:
        if self.restored:
            value = heappop(self.restored)
            self.queued.remove(value)
            return value
        value = self.frontier
        self.frontier += 1
        return value

    def addBack(self, num: int) -> None:
        if num < self.frontier and num not in self.queued:
            self.queued.add(num)
            heappush(self.restored, num)


class RemovedSetInfiniteSet:
    """Approach: Finite removed-set complement
    Time: O(r+1) expected popSmallest; O(1) expected addBack
    Space: O(r)
    """

    def __init__(self):
        self.removed = set()

    def popSmallest(self) -> int:
        candidate = 1
        while candidate in self.removed:
            candidate += 1
        self.removed.add(candidate)
        return candidate

    def addBack(self, num: int) -> None:
        self.removed.discard(num)
