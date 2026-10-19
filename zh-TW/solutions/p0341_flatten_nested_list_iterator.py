"""## Task

Iterate through integers in an arbitrarily nested list in left-to-right depth-first order.
Repeated hasNext calls must not consume a pending integer.

## Hints

1. A list iterator can remember progress without copying its remaining elements.
2. Cache the next discovered integer so hasNext is idempotent.

## Approach

### Lazy stack of child iterators

Maintain iterators for active nested lists. HasNext descends lists until it finds an integer and
caches it; exhausted iterators pop. Next consumes only the cached integer.

### Eager flattened snapshot

Flatten with an explicit reverse-push stack at construction, then serve values from an array
cursor.

## Why it works

### Lazy stack of child iterators

The iterator stack records exactly the unfinished depth-first traversal. Caching separates
discovery from consumption, so repeated availability checks preserve the next value.

### Eager flattened snapshot

Reverse-pushing children makes stack pops follow the original left-to-right order. Each integer
is appended once, and cursor iteration preserves that sequence.

## Walkthrough

For [1,[2,[],[3]],4], calls yield 1,2,3,4. Empty lists contribute no integer.

## Cost and pitfalls

Lazy stack of child iterators: O(T) total traversal; O(1) next after hasNext time; O(depth)
space.
Eager flattened snapshot: O(T) constructor; O(1) next/hasNext time; O(T) space.
The nested input is unchanged. T includes integers and nested containers. Lazy construction is
constant time; one hasNext may traverse many empty containers. The local NestedInteger helper
mirrors the supplied interview interface for standalone tests.
"""


class NestedInteger:
    """Standalone value container implementing the supplied nested-list interface."""

    def __init__(self, value=None):
        self._integer = value if isinstance(value, int) else None
        self._list = None if isinstance(value, int) else list(value or [])

    def isInteger(self):
        return self._integer is not None

    def getInteger(self):
        return self._integer

    def getList(self):
        return self._list

    def add(self, value):
        self._list.append(value)


class NestedIterator:
    """Approach: Lazy stack of child iterators
    Time: O(T) total traversal; O(1) next after hasNext
    Space: O(depth)
    """

    def __init__(self, nestedList: list["NestedInteger"]):
        self.stack = [iter(nestedList)]
        self.pending = None

    def hasNext(self) -> bool:
        if self.pending is not None:
            return True
        while self.stack:
            try:
                value = next(self.stack[-1])
            except StopIteration:
                self.stack.pop()
                continue
            if value.isInteger():
                self.pending = value.getInteger()
                return True
            self.stack.append(iter(value.getList()))
        return False

    def next(self) -> int:
        if not self.hasNext():
            raise StopIteration
        value, self.pending = self.pending, None
        return value


class EagerNestedIterator:
    """Approach: Eager flattened snapshot
    Time: O(T) constructor; O(1) next/hasNext
    Space: O(T)
    """

    def __init__(self, nestedList: list["NestedInteger"]):
        self.values = []
        self.index = 0
        stack = list(reversed(nestedList))
        while stack:
            value = stack.pop()
            if value.isInteger():
                self.values.append(value.getInteger())
            else:
                stack.extend(reversed(value.getList()))

    def hasNext(self) -> bool:
        return self.index < len(self.values)

    def next(self) -> int:
        value = self.values[self.index]
        self.index += 1
        return value
