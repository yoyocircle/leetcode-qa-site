"""## Task

Count the ways to choose positions from a source string so their characters
form a target string in order. Choices with different positions count
separately even when the selected characters are identical.

## Hints

1. A source character can either be skipped or used for the next target character.
2. Count target prefixes, and update backward to avoid using a source character twice.

## Approach

### Backward target-prefix counts

Let dp[j] count matches of the first j target characters using the processed
source prefix. Initialize dp[0]=1: there is one way to choose nothing.
All other counts begin at zero. For each source character, scan target
positions from right to left. If it matches target[j-1], add dp[j-1]
to dp[j]. Otherwise keep the existing count, which represents skipping it.

### Counts indexed by matching source positions

Transpose the counting table: rows consume target characters and columns consume source
prefixes. The empty target has one match in every source prefix; a nonempty target has zero
matches in an empty source.

## Why it works

### Backward target-prefix counts

Every match either excludes the current source position or includes it.
These groups are disjoint. Excluding it preserves the previous count;
including it extends any previous match of the target prefix one character
shorter, provided the characters agree. Backward updates ensure that both
counts refer to the preceding source prefix. Thus each valid position
selection is counted once and no source position is reused.

### Counts indexed by matching source positions

At each source endpoint, matches either skip that endpoint or use it to extend a match of
the preceding target prefix. These disjoint groups yield current[left]+previous[diagonal].

## Walkthrough

For source "aaaa" and target "aa", the count rows are [1,1,0], [1,2,1],
[1,3,3], and [1,4,6]. The result is six choices of two positions.

## Cost and pitfalls

For the default Backward target-prefix counts approach:

O(source_length*target_length) additions and O(target_length) integer entries;
inputs are unchanged. Python integers prevent overflow, but intermediate
counts can be large, so arithmetic and storage depend on their bit lengths.
Left-to-right updates would let one source character contribute multiple times.
Deduplicating identical resulting strings would solve a different counting task.

Backward target-prefix counts: O(m*n) additions time; O(n) integer entries space.
Counts indexed by matching source positions: O(m*n) additions time; O(m) integer entries space.
The alternate row orientation uses O(source length) storage and forward updates into a fresh
row. Intermediate arbitrary-precision counts affect bit cost in both variants.
"""


class Solution:
    """Approach: Backward target-prefix counts
    Time: O(m*n) additions
    Space: O(n) integer entries
    """

    def numDistinct(self, s: str, t: str) -> int:
        dp = [0] * (len(t) + 1)
        dp[0] = 1
        for character in s:
            for end in range(len(t), 0, -1):
                if character == t[end - 1]:
                    dp[end] += dp[end - 1]
        return dp[-1]


class PositionSolution:
    """Approach: Counts indexed by matching source positions
    Time: O(m*n) additions
    Space: O(m) integer entries
    """

    def numDistinct(self, s: str, t: str) -> int:
        previous = [1] * (len(s) + 1)
        for target in t:
            current = [0] * (len(s) + 1)
            for end, character in enumerate(s, 1):
                current[end] = current[end - 1]
                if character == target:
                    current[end] += previous[end - 1]
            previous = current
        return previous[-1]
