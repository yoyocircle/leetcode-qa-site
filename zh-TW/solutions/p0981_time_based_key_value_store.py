"""
## Task

Store timestamped values for each key. A lookup returns the value at the greatest
stored timestamp no later than its query, or an empty string if none exists.
Set timestamps arrive in strictly increasing order.

## Hints

1. The timestamp guarantee means each key's history is already sorted.
2. Find the first stored timestamp strictly greater than the query, then step back.

## Approach

### Bisect timestamp histories

Each key owns a list of (timestamp, value) records. Set appends one record.
Get uses bisect_right with a timestamp key, then reads the preceding record.
A single record list keeps timestamps and values paired.

### Manual binary search with parallel arrays

Store timestamps and values in parallel arrays per key and implement upper-bound binary search
directly. This avoids tuple keys and makes the predecessor boundary explicit.

## Why it works

### Bisect timestamp histories

Append order preserves sorted history. Binary search partitions it into timestamps
at most the query and timestamps greater than it. The last entry in the first
part is exactly the requested version.

### Manual binary search with parallel arrays

The globally increasing set timestamps make every per-key timestamp array sorted. Upper bound
separates timestamps at most the query from larger timestamps, so the preceding value is the
latest eligible write.

## Walkthrough

Set ("color","red",2) and ("color","blue",5). Get at 1 returns "", at 4
returns "red", and at 5 returns "blue".

## Cost and pitfalls

Default approach (Bisect timestamp histories):

Set is amortized O(1); get is O(log v) for v versions of the key. Storage is
O(total versions), excluding string content already supplied. Get does not create
missing keys. bisect's key parameter requires Python 3.10+, as used here.

Bisect timestamp histories: O(1) set; O(log m) get time; O(N) space.
Manual binary search with parallel arrays: O(1) set; O(log m) get time; O(N) space. Store
timestamps and values in parallel arrays per key and implement upper-bound binary search
directly. This avoids tuple keys and makes the predecessor boundary explicit.
"""

from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    """Approach: Bisect timestamp histories
    Time: O(1) set; O(log m) get
    Space: O(N)
    """

    def __init__(self):
        self.history = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.history[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        history = self.history.get(key, [])
        index = bisect_right(history, timestamp, key=lambda item: item[0])
        return history[index - 1][1] if index else ""


class ParallelTimeMap:
    """Approach: Manual binary search with parallel arrays
    Time: O(1) set; O(log m) get
    Space: O(N)
    """

    def __init__(self):
        self.history = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        times, values = self.history.setdefault(key, ([], []))
        times.append(timestamp)
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        times, values = self.history.get(key, ([], []))
        low, high = 0, len(times)
        while low < high:
            middle = (low + high) // 2
            if times[middle] <= timestamp:
                low = middle + 1
            else:
                high = middle
        return values[low - 1] if low else ""
