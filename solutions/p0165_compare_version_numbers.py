"""## Task

Compare dotted nonnegative version revisions numerically, ignoring leading zeros and
treating missing trailing revisions as zero.

## Hints

1. Compare revisions from left to right and stop at the first unequal pair.
2. Revision numbers can be accumulated while scanning without allocating pieces.

## Approach

### Split numeric revisions

Split both versions into revision strings, pair them with zero fill, and compare parsed
integers.

### Streaming revision accumulators

Advance independent pointers through digits to the next dot, accumulating one revision from
each input. A finished input naturally contributes zero.

## Why it works

### Split numeric revisions

The first unequal revision decides lexicographic revision order. Numeric parsing removes
leading-zero differences, and zero fill implements absent trailing revisions.

### Streaming revision accumulators

Each accumulator equals its current decimal revision. Equal revisions may be discarded, so
the first unequal pair determines the final order without retaining earlier text.

## Walkthrough

"1.002.0" equals "1.2"; "1.10" is greater than "1.2".

## Cost and pitfalls

Split numeric revisions: O(n+m) time; O(n+m) space.
Streaming revision accumulators: O(n+m) time; O(1) space.

Inputs remain unchanged. Revisions fit the problem's integer bound, so constant-number
storage applies to streaming accumulators. Splitting allocates all substrings; numeric
comparison differs from string lexicographic comparison.
"""


class Solution:
    """Approach: Split numeric revisions
    Time: O(n+m)
    Space: O(n+m)
    """

    def compareVersion(self, version1: str, version2: str) -> int:
        from itertools import zip_longest

        first = version1.split(".")
        second = version2.split(".")
        for a, b in zip_longest(first, second, fillvalue="0"):
            left, right = int(a), int(b)
            if left != right:
                return 1 if left > right else -1
        return 0


class StreamingSolution:
    """Approach: Streaming revision accumulators
    Time: O(n+m)
    Space: O(1)
    """

    def compareVersion(self, version1: str, version2: str) -> int:
        i = j = 0
        while i < len(version1) or j < len(version2):
            first = second = 0
            while i < len(version1) and version1[i] != ".":
                first = first * 10 + ord(version1[i]) - ord("0")
                i += 1
            while j < len(version2) and version2[j] != ".":
                second = second * 10 + ord(version2[j]) - ord("0")
                j += 1
            if first != second:
                return 1 if first > second else -1
            i += 1
            j += 1
        return 0
