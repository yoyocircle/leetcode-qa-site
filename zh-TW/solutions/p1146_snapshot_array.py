"""## Task

Maintain an initially zero array with set(index,val), snap() returning an increasing snapshot
ID, and get(index,snap_id) reading the value in that completed snapshot.

## Hints

1. Only changes matter; most indices need no full copy for a snapshot.
2. Coalesce repeated writes within one current snapshot ID.

## Approach

### Per-index change histories

Store sorted (snapshot_id,value) histories per index. Replace the final entry on another write
in the same current version. Snap only advances the version; get binary-searches the final
change no later than its requested ID.

### Full array copies

Keep the current array and append a fresh copy on every snap. Read completed versions directly
by snapshot ID.

## Why it works

### Per-index change histories

An index keeps its latest assigned value until the next change. The last historical assignment
at or before a snapshot therefore equals that snapshot's value. Coalescing current writes
discards only states that were never snapped.

### Full array copies

Each stored copy captures every current position at exactly its snap call. Later writes affect
only the live array, so completed snapshots remain immutable.

## Walkthrough

Set index 1 to 4, snap returning 0, then set it to 9. get(1,0) stays 4; a second snapshot
records 9.

## Cost and pitfalls

Per-index change histories: O(length) constructor; O(1) amortized set/snap; O(log h) get time;
O(length+stored changes) space.
Full array copies: O(length) constructor/snap; O(1) set/get time; O(length*(snapshots+1)); may
use excessive memory space.
Objects own all arrays and histories. h is changes at the queried index. Full copies are an
educational baseline that can exceed time or memory limits with many large snapshots.
Unsnapshotted later writes must never leak into old reads.
"""

from bisect import bisect_right


class SnapshotArray:
    """Approach: Per-index change histories
    Time: O(length) constructor; O(1) amortized set/snap; O(log h) get
    Space: O(length+stored changes)
    """

    def __init__(self, length: int):
        self.histories = [[(0, 0)] for _ in range(length)]
        self.current = 0

    def set(self, index: int, val: int) -> None:
        history = self.histories[index]
        if history[-1][0] == self.current:
            history[-1] = (self.current, val)
        else:
            history.append((self.current, val))

    def snap(self) -> int:
        result = self.current
        self.current += 1
        return result

    def get(self, index: int, snap_id: int) -> int:
        history = self.histories[index]
        position = bisect_right(history, (snap_id, float("inf"))) - 1
        return history[position][1]


class CopySnapshotArray:
    """Approach: Full array copies
    Time: O(length) constructor/snap; O(1) set/get
    Space: O(length*(snapshots+1)); may use excessive memory
    """

    def __init__(self, length: int):
        self.values = [0] * length
        self.snapshots = []

    def set(self, index: int, val: int) -> None:
        self.values[index] = val

    def snap(self) -> int:
        self.snapshots.append(self.values.copy())
        return len(self.snapshots) - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.snapshots[snap_id][index]
