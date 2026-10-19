"""## Task

Implement a capacity-limited deque supporting insertion and deletion at both ends, front/rear
queries, and empty/full checks. Empty queries return -1.

## Hints

1. A ring buffer can move either end with modular indices.
2. Sentinel linked nodes make empty-end updates ordinary link operations.

## Approach

### Head-indexed circular array

Track head and size over k fixed slots. Front insertion decrements head; rear insertion writes
at head+size. End deletions update head or size.

### Sentinel doubly linked deque

Maintain two sentinels and a live-node count. Insert between the appropriate sentinel and
neighbor; delete that end's live node by repairing reciprocal links.

## Why it works

### Head-indexed circular array

The logical deque always occupies size cyclic slots starting at head. Each operation changes
exactly its specified end while capacity and emptiness remain explicit.

### Sentinel doubly linked deque

The sentinel chain preserves front-to-rear order. Local insertion/deletion changes only the
requested end, and the count enforces the same bounded deque contract.

## Walkthrough

At capacity two, insertLast(4), insertFront(2) gives [2,4]. A further insertion fails until
deleting one end.

## Cost and pitfalls

Head-indexed circular array: O(1) per operation time; O(k) space.
Sentinel doubly linked deque: O(1) per operation time; O(k) space.
Objects own storage. All operations return status rather than overwrite on overflow. The linked
variant implements the same API but is not physically circular. Its empty sentinel chain must
remain reciprocal.
"""


class DequeEntry:
    def __init__(self, value=0):
        self.value = value
        self.previous = self.next = None


class MyCircularDeque:
    """Approach: Head-indexed circular array
    Time: O(1) per operation
    Space: O(k)
    """

    def __init__(self, k: int):
        self.values = [0] * k
        self.capacity, self.head, self.size = k, 0, 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        self.head = (self.head - 1) % self.capacity
        self.values[self.head] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        self.values[(self.head + self.size) % self.capacity] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        self.size -= 1
        return True

    def getFront(self) -> int:
        return self.values[self.head] if self.size else -1

    def getRear(self) -> int:
        return self.values[(self.head + self.size - 1) % self.capacity] if self.size else -1

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity


class LinkedCircularDeque:
    """Approach: Sentinel doubly linked deque
    Time: O(1) per operation
    Space: O(k)
    """

    def __init__(self, k: int):
        self.capacity, self.size = k, 0
        self.left, self.right = DequeEntry(), DequeEntry()
        self.left.next = self.right
        self.right.previous = self.left

    def _insert(self, before, after, value):
        node = DequeEntry(value)
        node.previous, node.next = before, after
        before.next = after.previous = node
        self.size += 1
        return True

    def _delete(self, node):
        node.previous.next = node.next
        node.next.previous = node.previous
        self.size -= 1
        return True

    def insertFront(self, value: int) -> bool:
        return False if self.isFull() else self._insert(self.left, self.left.next, value)

    def insertLast(self, value: int) -> bool:
        return False if self.isFull() else self._insert(self.right.previous, self.right, value)

    def deleteFront(self) -> bool:
        return False if self.isEmpty() else self._delete(self.left.next)

    def deleteLast(self) -> bool:
        return False if self.isEmpty() else self._delete(self.right.previous)

    def getFront(self) -> int:
        return self.left.next.value if self.size else -1

    def getRear(self) -> int:
        return self.right.previous.value if self.size else -1

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
