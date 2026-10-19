"""
## Task

Find the shortest substring of s containing every required character of t,
including repetitions. Return an empty string if none exists.

## Hints

1. Count missing occurrences, not only missing distinct characters.
2. Once a window is valid, shrink it until removing one more character breaks it.

## Approach

### Deficit-count shrinking window

Keep signed remaining counts and a total missing count. Adding a needed occurrence
reduces missing; extra occurrences make their counts negative. While nothing is
missing, record the window and advance left until validity is lost.

### Filtered relevant-position window

Discard text positions whose character is absent from the pattern, then slide over the remaining
(index, character) pairs. This can reduce window bookkeeping when relevant characters are
sparse.

## Why it works

### Deficit-count shrinking window

A window is valid exactly when missing is zero. For each right endpoint, shrinking
examines its shortest valid ending window. A removed prefix cannot produce a
shorter future window than one already recorded with that same left boundary.

### Filtered relevant-position window

A shortest valid window starts and ends at relevant characters, since irrelevant endpoints can
be removed. Deficit counts on the filtered sequence therefore examine every potentially optimal
boundary pair.

## Walkthrough

For s="BAAC" and t="AAC", the whole string first becomes valid. Removing B
keeps it valid, yielding "AAC". Removing its first A makes one A missing.
The answer is "AAC".

## Cost and pitfalls

Default approach (Deficit-count shrinking window):

Expected O(len(s)+len(t)) time and O(alphabet size) auxiliary space, plus the
returned substring. Inputs are unchanged. Store indices and slice only once;
copying every improving window could add quadratic work. Negative counts encode
surplus characters and must not be reset to zero.

Deficit-count shrinking window: O(n+m) expected time; O(alphabet) space.
Filtered relevant-position window: O(n+m) expected time; O(n+alphabet) space. Discard text
positions whose character is absent from the pattern, then slide over the remaining (index,
character) pairs. This can reduce window bookkeeping when relevant characters are sparse.
"""

from collections import Counter


class Solution:
    """Approach: Deficit-count shrinking window
    Time: O(n+m) expected
    Space: O(alphabet)
    """

    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        missing = len(t)
        left = best_start = 0
        best_length = len(s) + 1
        for right, char in enumerate(s):
            if need[char] > 0:
                missing -= 1
            need[char] -= 1
            while missing == 0:
                if right - left + 1 < best_length:
                    best_start, best_length = left, right - left + 1
                outgoing = s[left]
                need[outgoing] += 1
                if need[outgoing] > 0:
                    missing += 1
                left += 1
        return "" if best_length > len(s) else s[best_start : best_start + best_length]


class FilteredSolution:
    """Approach: Filtered relevant-position window
    Time: O(n+m) expected
    Space: O(n+alphabet)
    """

    def minWindow(self, s: str, t: str) -> str:
        need = {}
        for char in t:
            need[char] = need.get(char, 0) + 1
        filtered = [(i, char) for i, char in enumerate(s) if char in need]
        have = {}
        missing = len(t)
        left = 0
        best_start, best_size = 0, len(s) + 1
        for index, char in filtered:
            have[char] = have.get(char, 0) + 1
            if have[char] <= need[char]:
                missing -= 1
            while missing == 0:
                start, outgoing = filtered[left]
                if index - start + 1 < best_size:
                    best_start, best_size = start, index - start + 1
                have[outgoing] -= 1
                if have[outgoing] < need[outgoing]:
                    missing += 1
                left += 1
        return "" if best_size > len(s) else s[best_start : best_start + best_size]
