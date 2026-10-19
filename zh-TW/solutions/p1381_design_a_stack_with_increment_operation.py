"""## Task

Implement a capacity-limited integer stack with push, pop, and increment(k,val), which adds val
to its bottom min(k,size) entries. Empty pop returns -1.

## Hints

1. An increment affects a prefix of the stack.
2. Delay each prefix increment at its top boundary and propagate it when popped.

## Approach

### Lazy boundary increments

Keep parallel value and pending-increment arrays. Record an increment at its highest affected
index. Pop combines its pending amount with the value and passes that amount to the next lower
entry.

### Eager prefix updates

Store actual current values. Increment directly updates each affected list position; push
respects capacity and pop uses the final position.

## Why it works

### Lazy boundary increments

A pending boundary represents an increment owed to every entry below it. Popping its top
consumes that entry's share and transfers the same obligation downward, preserving all future
values.

### Eager prefix updates

Every increment explicitly changes exactly the bottom affected entries, so the stored array
always equals the abstract stack. Other operations directly implement stack behavior.

## Walkthrough

Push 2 and 5, then increment(2,3): pops return 8 and 5. The lazy version records 3 once, then
propagates it.

## Cost and pitfalls

Lazy boundary increments: O(1) per operation time; O(capacity) space.
Eager prefix updates: O(1) push/pop; O(min(k,size)) increment time; O(capacity) space.
Objects own their arrays. Ignored pushes must not create pending state. Python list append/pop
are amortized constant time. Clamp k to the actual size and preserve pending increments when
values above them are removed.
"""


class CustomStack:
    """Approach: Lazy boundary increments
    Time: O(1) per operation
    Space: O(capacity)
    """

    def __init__(self, maxSize: int):
        self.capacity = maxSize
        self.values = []
        self.pending = []

    def push(self, x: int) -> None:
        if len(self.values) < self.capacity:
            self.values.append(x)
            self.pending.append(0)

    def pop(self) -> int:
        if not self.values:
            return -1
        increment = self.pending.pop()
        if self.pending:
            self.pending[-1] += increment
        return self.values.pop() + increment

    def increment(self, k: int, val: int) -> None:
        index = min(k, len(self.values)) - 1
        if index >= 0:
            self.pending[index] += val


class EagerCustomStack:
    """Approach: Eager prefix updates
    Time: O(1) push/pop; O(min(k,size)) increment
    Space: O(capacity)
    """

    def __init__(self, maxSize: int):
        self.capacity = maxSize
        self.values = []

    def push(self, x: int) -> None:
        if len(self.values) < self.capacity:
            self.values.append(x)

    def pop(self) -> int:
        return self.values.pop() if self.values else -1

    def increment(self, k: int, val: int) -> None:
        for index in range(min(k, len(self.values))):
            self.values[index] += val
