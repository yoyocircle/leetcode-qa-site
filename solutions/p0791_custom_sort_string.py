"""## Task

Reorder s so characters present in the distinct-character order string respect
that order. Characters absent from order may occur anywhere.

## Hints

1. Emit the requested characters in order using their multiplicities.
2. Alternatively, turn the custom order into numeric sort keys.

## Approach

### Frequency emission

Count s. For each character in order, remove its count from the map and emit
that many copies. Then emit all leftover characters. Removing used keys keeps
the final pass from duplicating them.

### Rank-key sorting

Map each ordered character to its index, assigning absent characters a common
rank after all listed characters. Sort s by that key and join. Stability
preserves the original relative order of unlisted characters, though the
problem does not require this property.

## Why it works

Frequency emission preserves every count and emits constrained characters in
the required order. The remaining characters have no constraints. Rank sorting
preserves the input multiset and ensures every earlier rank precedes every
later rank, which is precisely the custom ordering condition.

## Walkthrough

With order="cba" and s="abcdab", emit c once, b twice, a twice, then d.
One answer is "cbbaad". Moving d elsewhere would also be valid.

## Cost and pitfalls

Let n=len(s), r=len(order), and u be the number of distinct characters in s.
Frequency emission takes O(n+r) expected time and O(n+u) space including output.
Rank sorting takes O(r+n log n) time and O(r+n) space including keys and output.
The lowercase alphabet bounds r and u, but n remains variable. Both leave
their inputs unchanged. Do not drop characters absent from order or invent
an unnecessary lexicographic tie requirement.
"""

from collections import Counter


class Solution:
    """Approach: Frequency emission
    Time: O(n+r) expected
    Space: O(n+u), including output
    """

    def customSortString(self, order: str, s: str) -> str:
        counts = Counter(s)
        pieces = []
        for char in order:
            count = counts.pop(char, 0)
            if count:
                pieces.append(char * count)
        pieces.extend(char * count for char, count in counts.items())
        return "".join(pieces)


class RankSortSolution:
    """Approach: Rank-key sorting
    Time: O(r+n log n)
    Space: O(r+n), including output
    """

    def customSortString(self, order: str, s: str) -> str:
        rank = {char: index for index, char in enumerate(order)}
        return "".join(sorted(s, key=lambda char: rank.get(char, len(order))))
