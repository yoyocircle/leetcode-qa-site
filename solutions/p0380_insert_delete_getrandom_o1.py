"""## Task

Support insert, remove, and uniform random selection from distinct stored integers. Insert and
remove report whether membership changed; getRandom is called only when nonempty.

## Hints

1. Random indexing needs dense positions.
2. Swap the last element into a removed slot and update its map entry.

## Approach

### Dense array and index map

Map each value to its array index. Insert appends; remove fills the hole with the last value;
random selection chooses a uniform array index.

### Set with random snapshots

Keep only a set and turn it into a tuple for each random query. This simple baseline avoids
maintaining positions but copies all values on every draw.

## Why it works

### Dense array and index map

The array and map remain a bijection between live values and dense positions. A uniform position
therefore selects each live value with equal probability.

### Set with random snapshots

Set membership directly implements uniqueness. A uniform tuple index is uniform over the set
because each live value appears once in the snapshot.

## Walkthrough

Insert 4 and 9, then remove 4. Every subsequent draw must return 9; removing 4 again returns
false.

## Cost and pitfalls

Dense array and index map: O(1) expected per operation time; O(n) space.
Set with random snapshots: O(1) expected insert/remove; O(n) getRandom; misses required O(1)
time; O(n) space.
Objects own their storage. The snapshot baseline misses the mandated constant-time random query
and may time out. Random support and broad frequency checks are appropriate tests; exact
sequences depend on implementation order.
"""

from random import choice


class RandomizedSet:
    """Approach: Dense array and index map
    Time: O(1) expected per operation
    Space: O(n)
    """

    def __init__(self):
        self.values = []
        self.indices = {}

    def insert(self, val: int) -> bool:
        if val in self.indices:
            return False
        self.indices[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.indices:
            return False
        index = self.indices[val]
        last = self.values[-1]
        self.values[index] = last
        self.indices[last] = index
        self.values.pop()
        del self.indices[val]
        return True

    def getRandom(self) -> int:
        return choice(self.values)


class SnapshotRandomizedSet:
    """Approach: Set with random snapshots
    Time: O(1) expected insert/remove; O(n) getRandom; misses required O(1)
    Space: O(n)
    """

    def __init__(self):
        self.values = set()

    def insert(self, val: int) -> bool:
        if val in self.values:
            return False
        self.values.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.values:
            return False
        self.values.remove(val)
        return True

    def getRandom(self) -> int:
        return choice(tuple(self.values))
