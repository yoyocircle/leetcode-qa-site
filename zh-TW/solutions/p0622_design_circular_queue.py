"""## Task

Implement a fixed-capacity FIFO queue with enqueue/dequeue status, front/rear queries, and
empty/full checks. Empty front or rear queries return -1.

## Hints

1. Distinguish an empty queue from a full queue explicitly.
2. A size count makes wrapped head and tail positions unambiguous.

## Approach

### Fixed circular buffer

Allocate k slots and track head plus size. Enqueue writes at (head+size) modulo k; dequeue
advances head modulo k.

### Capacity-limited linked queue

Track a singly linked head and tail plus size. Append a new owned node on enqueue and remove the
head on dequeue; enforce capacity before allocation.

## Why it works

### Fixed circular buffer

The live entries occupy exactly size consecutive cyclic positions from head. Inserting at the
first free position or removing the first live one preserves FIFO order and capacity.

### Capacity-limited linked queue

The chain stores entries in insertion order. Removing only its head implements FIFO, while
maintaining size enforces the same fixed-capacity abstract contract without a physical ring.

## Walkthrough

At capacity two, enqueue 4 and 7 fills the queue. Dequeue removes 4; enqueue 9 then makes front
7 and rear 9.

## Cost and pitfalls

Fixed circular buffer: O(1) per operation time; O(k) space.
Capacity-limited linked queue: O(1) per operation time; O(k) space.
Objects own all storage. The linked alternative exposes the same queue API but is not physically
circular. After removing its last node, clear both head and tail. The array version uses all k
slots because size distinguishes full from empty.
"""


class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class MyCircularQueue:
    """Approach: Fixed circular buffer
    Time: O(1) per operation
    Space: O(k)
    """

    def __init__(self, k: int):
        self.values = [0] * k
        self.capacity = k
        self.head = 0
        self.size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.values[(self.head + self.size) % self.capacity] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        return self.values[self.head] if self.size else -1

    def Rear(self) -> int:
        return self.values[(self.head + self.size - 1) % self.capacity] if self.size else -1

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity


class LinkedCircularQueue:
    """Approach: Capacity-limited linked queue
    Time: O(1) per operation
    Space: O(k)
    """

    def __init__(self, k: int):
        self.capacity = k
        self.size = 0
        self.head = self.tail = None

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        node = QueueNode(value)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = self.head.next
        self.size -= 1
        if self.head is None:
            self.tail = None
        return True

    def Front(self) -> int:
        return self.head.value if self.head else -1

    def Rear(self) -> int:
        return self.tail.value if self.tail else -1

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
