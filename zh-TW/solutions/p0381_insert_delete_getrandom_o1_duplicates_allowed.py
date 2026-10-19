"""## Task

Maintain a multiset with insert, removal of one occurrence, and random selection proportional to
occurrence count. Insert reports whether the value was previously absent.

## Hints

1. Each stored occurrence needs one dense array slot.
2. Map a value to every index holding that value, updating moved last occurrences carefully.

## Approach

### Dense occurrences and index sets

Store all occurrences in an array and a set of positions per value. Remove one position, move
the final occurrence into its slot, and repair both index sets.

### Frequency map and weighted scan

Store only frequency counts. Pick a uniform integer below total multiplicity and scan cumulative
counts to find the containing value block.

## Why it works

### Dense occurrences and index sets

Every live occurrence owns exactly one slot tracked by its value's set. Moving the final
occurrence preserves this ownership; a uniform slot gives probabilities proportional to
multiplicity.

### Frequency map and weighted scan

A value with c occurrences owns c possible draw integers in the cumulative partition. It is
therefore selected with probability c/total without materializing duplicate slots.

## Walkthrough

After inserting 5,5,8, the probability of 5 is two thirds. Removing one 5 leaves equal
probabilities for 5 and 8.

## Cost and pitfalls

Dense occurrences and index sets: O(1) expected per operation time; O(n) space.
Frequency map and weighted scan: O(1) expected insert/remove; O(u) getRandom; misses required
O(1) time; O(u) space.
Objects own all state. The count baseline saves space with many duplicates but misses the
required constant-time draw and may time out. Removing a value equal to the last slot still
requires consistent index-set updates.
"""

from collections import defaultdict
from random import choice, randrange


class RandomizedCollection:
    """Approach: Dense occurrences and index sets
    Time: O(1) expected per operation
    Space: O(n)
    """

    def __init__(self):
        self.values = []
        self.positions = defaultdict(set)

    def insert(self, val: int) -> bool:
        absent = not self.positions[val]
        self.positions[val].add(len(self.values))
        self.values.append(val)
        return absent

    def remove(self, val: int) -> bool:
        if val not in self.positions:
            return False
        index = self.positions[val].pop()
        last_index = len(self.values) - 1
        last = self.values[-1]
        if index != last_index:
            self.values[index] = last
            self.positions[last].remove(last_index)
            self.positions[last].add(index)
        self.values.pop()
        if not self.positions[val]:
            del self.positions[val]
        return True

    def getRandom(self) -> int:
        return choice(self.values)


class CountedCollection:
    """Approach: Frequency map and weighted scan
    Time: O(1) expected insert/remove; O(u) getRandom; misses required O(1)
    Space: O(u)
    """

    def __init__(self):
        self.counts = {}
        self.total = 0

    def insert(self, val: int) -> bool:
        absent = val not in self.counts
        self.counts[val] = self.counts.get(val, 0) + 1
        self.total += 1
        return absent

    def remove(self, val: int) -> bool:
        if val not in self.counts:
            return False
        self.counts[val] -= 1
        self.total -= 1
        if self.counts[val] == 0:
            del self.counts[val]
        return True

    def getRandom(self) -> int:
        index = randrange(self.total)
        for value, count in self.counts.items():
            if index < count:
                return value
            index -= count
        raise AssertionError("Unreachable for a nonempty collection")
