"""
## Task

Implement push, pop, top, and getMin without scanning the stack. Operations that
read or remove values are only called when the stack is nonempty.

## Hints

1. Popping should restore the minimum of the remaining prefix.
2. Store the answer for each stack depth alongside the pushed value.

## Approach

### Minimum snapshot per entry

Store pairs of (value, minimum through this depth). A push combines the new value
with the previous minimum. Pop removes both together, so minimum history cannot
fall out of sync with value history.

### Separate minima stack

Store values and a second stack containing only new or tied minima. Popping a minimum also pops
its matching snapshot; equal minima must be recorded separately.

## Why it works

### Minimum snapshot per entry

Inductively, each pair's second item is the minimum of its entire stack prefix.
The top pair therefore contains the current minimum. Removing it exposes the
already-correct minimum for the shorter prefix.

### Separate minima stack

The minima stack contains the nonincreasing sequence of record minima still present. Its top is
therefore exactly the smallest value in the data stack after every push or pop.

## Walkthrough

Push 4, 2, 2 to obtain [(4,4), (2,2), (2,2)]. Pop once and getMin remains 2.
Pop again and getMin becomes 4.

## Cost and pitfalls

Default approach (Minimum snapshot per entry):

Reads and pop take O(1); Python list push takes amortized O(1). Storage is O(n).
The object owns and mutates its private stack. Repeated minima require their own
history entries. Recomputing min after a pop would violate the constant-time goal.

Minimum snapshot per entry: O(1) per operation time; O(n) space.
Separate minima stack: O(1) per operation time; O(n) space. Store values and a second stack
containing only new or tied minima. Popping a minimum also pops its matching snapshot; equal
minima must be recorded separately.
"""


class MinStack:
    """Approach: Minimum snapshot per entry
    Time: O(1) per operation
    Space: O(n)
    """

    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        minimum = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, minimum))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


class MinimaStack:
    """Approach: Separate minima stack
    Time: O(1) per operation
    Space: O(n)
    """

    def __init__(self):
        self.values = []
        self.minima = []

    def push(self, val: int) -> None:
        self.values.append(val)
        if not self.minima or val <= self.minima[-1]:
            self.minima.append(val)

    def pop(self) -> None:
        value = self.values.pop()
        if value == self.minima[-1]:
            self.minima.pop()

    def top(self) -> int:
        return self.values[-1]

    def getMin(self) -> int:
        return self.minima[-1]
