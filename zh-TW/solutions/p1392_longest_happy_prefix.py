"""## Task

Return the longest nonempty prefix that is also a suffix, excluding the entire string;
return empty if none exists.

## Hints

1. A prefix-function value records the longest proper border of each prefix.
2. A Z value records how much of the whole-string prefix matches at a later position.

## Approach

### KMP prefix function

Build proper-border lengths left to right. On mismatch, fall back through shorter borders
until the next character can extend one.

### Z-function prefix matches

Maintain a rightmost prefix-matching interval and reuse mirrored Z values inside it. A match
extending exactly to the string end is a border candidate.

## Why it works

### KMP prefix function

Every candidate shorter border of the preceding prefix lies on its prefix-function fallback
chain. Testing that chain finds the longest extendable border. Total fallback decreases are
bounded by total increases, giving linear work.

### Z-function prefix matches

Z[index] equals the longest prefix matching from that index. Reaching the end makes that
match a suffix, and excluding index zero keeps it proper. Each new comparison outside the
known interval advances its right endpoint.

## Walkthrough

For "ababab", prefix and suffix "abab" coincide, so return "abab".

## Cost and pitfalls

KMP prefix function: O(n) time; O(n) space.
Z-function prefix matches: O(n) time; O(n) space.

Both are deterministic and preserve s; final output slicing costs O(border length) time and
space within the stated bounds. Neither uses rolling hashes or risks hash collisions.
Repeated characters and overlapping borders are valid.
"""


class Solution:
    """Approach: KMP prefix function
    Time: O(n)
    Space: O(n)
    """

    def longestPrefix(self, s: str) -> str:
        prefix = [0] * len(s)
        for index in range(1, len(s)):
            length = prefix[index - 1]
            while length and s[index] != s[length]:
                length = prefix[length - 1]
            if s[index] == s[length]:
                length += 1
            prefix[index] = length
        return s[: prefix[-1]]


class ZSolution:
    """Approach: Z-function prefix matches
    Time: O(n)
    Space: O(n)
    """

    def longestPrefix(self, s: str) -> str:
        z = [0] * len(s)
        left = right = 0
        best = 0
        for index in range(1, len(s)):
            if index <= right:
                z[index] = min(right - index + 1, z[index - left])
            while index + z[index] < len(s) and s[z[index]] == s[index + z[index]]:
                z[index] += 1
            if index + z[index] - 1 > right:
                left, right = index, index + z[index] - 1
            if index + z[index] == len(s):
                best = max(best, z[index])
        return s[:best]
