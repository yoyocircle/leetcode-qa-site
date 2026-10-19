"""## Task

Implement a fixed-capacity key-value cache. Get returns a value or -1. Get and
put both mark a present key as recently used; overflow evicts the least recent key.

## Hints

1. You need both direct key lookup and movable recency order.
2. An ordered dictionary provides those operations in the standard library.

## Approach

### Ordered dictionary recency

Keep an OrderedDict from least recent at the front to most recent at the back.
Successful get moves the key to the back. Put writes the value and moves the
key to the back, then removes the front item if capacity is exceeded.

### Hash map and linked recency

Map keys to entries in a circular doubly linked list. The sentinel's next entry is oldest and
previous entry newest. Successful access detaches an entry and appends it before the sentinel;
overflow removes the oldest.

## Why it works

### Ordered dictionary recency

The dictionary order records the order of last successful use: each use removes
the key from its old position and places it newest. The front is consequently
the least recently used key, making eviction exact.

### Hash map and linked recency

The map owns exactly the live entries and the list records their last-use order. Moving an
accessed entry changes only its recency, while removing the oldest entry updates both
representations together.

## Walkthrough

At capacity 2, put (1,10), put (2,20), then get(1). Recency becomes [2,1].
Putting (3,30) evicts 2; get(2) now returns -1.

## Cost and pitfalls

Default approach costs and behavior:

Expected O(1) per operation and O(capacity) space. The object owns all cache
state. Updating an existing key also refreshes recency. A failed get must not
insert anything. If library ordering is disallowed in an interview, implement
the same invariant with a hash map plus doubly linked list.

Alternative tradeoff: O(1) expected per operation time; O(capacity) space.
"""

from collections import OrderedDict


class LRUCache:
    """Approach: Ordered dictionary recency
    Time: O(1) expected per operation
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.values = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        self.values.move_to_end(key)
        return self.values[key]

    def put(self, key: int, value: int) -> None:
        self.values[key] = value
        self.values.move_to_end(key)
        if len(self.values) > self.capacity:
            self.values.popitem(last=False)


class CacheEntry:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.previous = self.next = self


class LinkedLRUCache:
    """Approach: Hash map and linked recency
    Time: O(1) expected per operation
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.entries = {}
        self.root = CacheEntry()

    def _touch(self, entry):
        entry.previous.next = entry.next
        entry.next.previous = entry.previous
        entry.previous = self.root.previous
        entry.next = self.root
        self.root.previous.next = entry
        self.root.previous = entry

    def get(self, key: int) -> int:
        if key not in self.entries:
            return -1
        entry = self.entries[key]
        self._touch(entry)
        return entry.value

    def put(self, key: int, value: int) -> None:
        if key in self.entries:
            entry = self.entries[key]
            entry.value = value
        else:
            entry = CacheEntry(key, value)
            self.entries[key] = entry
        self._touch(entry)
        if len(self.entries) > self.capacity:
            oldest = self.root.next
            self.root.next = oldest.next
            oldest.next.previous = self.root
            del self.entries[oldest.key]
