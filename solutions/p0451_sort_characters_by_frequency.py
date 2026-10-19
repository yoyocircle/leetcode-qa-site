"""## Task

Reorder a string so characters with larger frequencies appear first, with all
copies of each character together. Ties may appear in any order.

## Hints

1. Count each distinct character before arranging output.
2. Frequencies lie between one and n, so they can serve as bucket indices.

## Approach

### Frequency buckets

Count characters, place each distinct character into the bucket indexed by
its count, then read buckets from n down to one. Emit each character repeated
by its bucket index.

### Sorted frequency entries

Sort the distinct (character, count) pairs by descending count. Emit one block
per sorted entry. This avoids n bucket objects when only a few symbols occur.

## Why it works

Each character is counted once and emitted exactly that many times, preserving
the input multiset. Descending bucket indices and descending sorted counts
both ensure that no lower-frequency block precedes a higher-frequency block.
Tie order does not affect validity, so no secondary comparison is necessary.

## Walkthrough

For "banana", the counts are a:3, n:2, b:1. Both versions return "aaannb".
For equal counts, several results are valid; tests should check the contract
rather than requiring a particular incidental dictionary order.

## Cost and pitfalls

Let n be input length and u distinct symbols. Buckets take O(n+u) time and
O(n+u) space. Sorting entries takes O(n+u log u) time and O(n+u) space including
output. Its non-output storage is O(u), unlike the O(n+u) bucket allocation.
The given alphabet bounds u, but retaining u makes the tradeoff explicit.
Joining prebuilt blocks is linear in output size. The input string is unchanged.
"""

from collections import Counter


class Solution:
    """Approach: Frequency buckets
    Time: O(n+u)
    Space: O(n+u), including output
    """

    def frequencySort(self, s: str) -> str:
        counts = Counter(s)
        buckets = [[] for _ in range(len(s) + 1)]
        for char, count in counts.items():
            buckets[count].append(char)
        return "".join(char * count for count in range(len(s), 0, -1) for char in buckets[count])


class SortedCountsSolution:
    """Approach: Sorted frequency entries
    Time: O(n+u log u)
    Space: O(n+u) including output; O(u) other storage
    """

    def frequencySort(self, s: str) -> str:
        entries = sorted(Counter(s).items(), key=lambda item: -item[1])
        return "".join(char * count for char, count in entries)
