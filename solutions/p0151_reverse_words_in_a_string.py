"""## Task

Reverse word order while trimming leading/trailing spaces and reducing every internal run of
spaces to one.

## Hints

1. Splitting without a separator normalizes whitespace.
2. Scanning words from the end can emit the final order directly.

## Approach

### Split reverse and join

Split into nonempty words, iterate those words in reverse, and join them with one space.

### Manual backward word scanner

Skip trailing spaces, identify the preceding maximal word, and append its slice; repeat from
right to left before joining.

## Why it works

### Split reverse and join

Split preserves the original word order and removes separator runs. Reversing word iteration
changes exactly that order, and join supplies exactly one separator.

### Manual backward word scanner

Each maximal non-space run is extracted exactly once in reverse encounter order. Word
contents remain forward because each slice uses increasing indices.

## Walkthrough

"  red   blue " becomes "blue red".

## Cost and pitfalls

Split reverse and join: O(n) time; O(n) space.
Manual backward word scanner: O(n) time; O(n) space.

Inputs contain letters, digits, and ASCII spaces. Both preserve the immutable input and
allocate O(n) word/output text; the manual slices are copies, not views. An in-place O(1)
guarantee cannot apply to Python strings.
"""


class Solution:
    """Approach: Split reverse and join
    Time: O(n)
    Space: O(n)
    """

    def reverseWords(self, s: str) -> str:
        return " ".join(reversed(s.split()))


class BackwardSolution:
    """Approach: Manual backward word scanner
    Time: O(n)
    Space: O(n)
    """

    def reverseWords(self, s: str) -> str:
        words = []
        index = len(s) - 1
        while index >= 0:
            while index >= 0 and s[index] == " ":
                index -= 1
            end = index + 1
            while index >= 0 and s[index] != " ":
                index -= 1
            if end > index + 1:
                words.append(s[index + 1 : end])
        return " ".join(words)
