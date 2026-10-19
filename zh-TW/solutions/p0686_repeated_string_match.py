"""## Task

Return the fewest repetitions of nonempty string a whose concatenation
contains nonempty string b as a substring. Return -1 when no repetition works.

## Hints

1. A match can always be shifted to start within the first copy of a.
2. Prefix-function or Z-function matching avoids repeated candidate comparisons.

## Approach

### KMP over virtual repetitions

Build b's prefix-function table. Scan a virtual periodic string by reading
a[index % len(a)], keeping the length of the matched prefix of b. A mismatch
falls back along the prefix table. Scan only len(a)+len(b)-1 characters.
When a full match ends, ceil((end+1)/len(a)) is the required repetition count.

### Z-function over a bounded text

Build a repeated text of the same bounded length. Compute Z values for
b + '#' + text, where '#' cannot occur in the lowercase inputs. The first
text position with a Z value at least len(b) starts a complete match. Convert
its ending position to a repetition count.

## Why it works

Any match in an infinite periodic string can be shifted left by whole copies
of a until its start is below len(a). Its end then lies within the bounded
scan. KMP and Z matching both identify exact matches, without hash collisions.
All matches have the same length, so the first ending match minimizes the
number of whole copies needed. Exhausting the bound proves impossibility.

## Walkthrough

For a="abc" and b="cabca", the earliest match starts at position 2 and ends
at position 6 in "abcabcabc". Seven required characters need three copies.
For a="ab" and b="ac", no match exists regardless of the repetition count.

## Cost and pitfalls

With A=len(a), B=len(b), both algorithms take O(A+B) time. KMP uses O(B)
space for its prefix table and never builds repeated text. Z matching uses
O(A+B) space for the materialized text and Z table. Fallbacks and reused
Z intervals give amortized linear comparisons, even on repetitive strings.
Inputs are unchanged. A match may cross a copy boundary; testing only one
copy or exactly ceil(B/A) copies misses valid answers.
"""


class Solution:
    """Approach: KMP over virtual repetitions
    Time: O(A+B)
    Space: O(B)
    """

    def repeatedStringMatch(self, a: str, b: str) -> int:
        prefix = [0] * len(b)
        matched = 0
        for index in range(1, len(b)):
            while matched and b[index] != b[matched]:
                matched = prefix[matched - 1]
            if b[index] == b[matched]:
                matched += 1
            prefix[index] = matched
        matched = 0
        for index in range(len(a) + len(b) - 1):
            char = a[index % len(a)]
            while matched and char != b[matched]:
                matched = prefix[matched - 1]
            if char == b[matched]:
                matched += 1
            if matched == len(b):
                return (index + len(a)) // len(a)
        return -1


class ZSolution:
    """Approach: Z-function over a bounded text
    Time: O(A+B)
    Space: O(A+B)
    """

    def repeatedStringMatch(self, a: str, b: str) -> int:
        length = len(a) + len(b) - 1
        text = (a * ((length + len(a) - 1) // len(a)))[:length]
        combined = b + "#" + text
        offset = len(b) + 1
        z = [0] * len(combined)
        left = right = 0
        for index in range(1, len(combined)):
            if index < right:
                z[index] = min(right - index, z[index - left])
            while (
                index + z[index] < len(combined)
                and combined[z[index]] == combined[index + z[index]]
            ):
                z[index] += 1
            if index + z[index] > right:
                left, right = index, index + z[index]
            if index >= offset and z[index] >= len(b):
                end_exclusive = index - offset + len(b)
                return (end_exclusive + len(a) - 1) // len(a)
        return -1
