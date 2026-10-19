"""## Task

Implement a capacity-limited cache that evicts the least frequently used key. Break
equal-frequency ties by least recent use. Successful gets and updates both increase frequency.

## Hints

1. Group keys by their current usage frequency.
2. Within each frequency keep keys ordered by recency and track the minimum live frequency.

## Approach

### Frequency buckets with ordered recency

Map keys to value/frequency pairs and maintain OrderedDict buckets. Touch moves a key to the
next frequency's newest end. Evict the oldest key in the minimum bucket.

### Timestamped entries and eviction scan

Store value, frequency, and last-use timestamp per key. When full, scan for the
lexicographically smallest (frequency,timestamp) victim.

## Why it works

### Frequency buckets with ordered recency

Buckets partition live keys by exact frequency; their order records tie-breaking last use.
Moving a touched key updates both invariants, and minimum-frequency oldest eviction follows the
required policy.

### Timestamped entries and eviction scan

Every successful use increments frequency and stamps newest recency. Minimizing the stored pair
therefore implements the same eviction rule directly, at linear eviction cost.

## Walkthrough

At capacity two, insert 1 and 2, then get(1). Inserting 3 evicts 2. If 1 and 3 later tie in
frequency, the older use loses.

## Cost and pitfalls

Frequency buckets with ordered recency: O(1) expected per operation time; O(capacity) space.
Timestamped entries and eviction scan: O(1) get/update; O(capacity) eviction; misses required
O(1) time; O(capacity) space.
Objects own all state. A failed get does not change frequency. New keys start at frequency one.
The scan baseline may time out at full operation limits and misses the average constant-time
requirement.
"""

from collections import OrderedDict


class LFUCache:
    """Approach: Frequency buckets with ordered recency
    Time: O(1) expected per operation
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.values = {}
        self.buckets = {}
        self.minimum = 0

    def _touch(self, key):
        value, frequency = self.values[key]
        bucket = self.buckets[frequency]
        del bucket[key]
        if not bucket:
            del self.buckets[frequency]
            if self.minimum == frequency:
                self.minimum += 1
        frequency += 1
        self.values[key] = (value, frequency)
        self.buckets.setdefault(frequency, OrderedDict())[key] = None
        return value

    def get(self, key: int) -> int:
        return self._touch(key) if key in self.values else -1

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.values:
            self.values[key] = (value, self.values[key][1])
            self._touch(key)
            return
        if len(self.values) == self.capacity:
            bucket = self.buckets[self.minimum]
            victim, _ = bucket.popitem(last=False)
            del self.values[victim]
            if not bucket:
                del self.buckets[self.minimum]
        self.values[key] = (value, 1)
        self.buckets.setdefault(1, OrderedDict())[key] = None
        self.minimum = 1


class ScanLFUCache:
    """Approach: Timestamped entries and eviction scan
    Time: O(1) get/update; O(capacity) eviction; misses required O(1)
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.clock = 0
        self.entries = {}

    def get(self, key: int) -> int:
        if key not in self.entries:
            return -1
        self.clock += 1
        value, frequency, _ = self.entries[key]
        self.entries[key] = (value, frequency + 1, self.clock)
        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        self.clock += 1
        if key in self.entries:
            frequency = self.entries[key][1] + 1
        else:
            frequency = 1
            if len(self.entries) == self.capacity:
                victim = min(self.entries, key=lambda candidate: self.entries[candidate][1:])
                del self.entries[victim]
        self.entries[key] = (value, frequency, self.clock)
