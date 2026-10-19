"""## Task

Return the length of the longest subsequence shared by two strings.
Characters can be skipped, but their order must remain unchanged in each string.

## Hints

1. Compare the final characters of the two prefixes under consideration.
2. Matching characters extend the diagonal state; otherwise skip a character.

## Approach

### Compressed prefix lengths

Use the shorter string for columns. Initialize a zero row for empty-prefix
comparisons. For each character in the longer string, visit columns from
left to right. Save the old dp[column] before overwriting it. If the
characters match, use the old diagonal plus one; otherwise use the maximum
of the old entry above and the updated entry to the left. Carry the saved
old entry forward as the next diagonal.

### Increasing match positions

Index occurrences in the second string. For each first-string character, feed matching
second-string positions in descending order into a strictly increasing subsequence tracker.
Here r is the number of matching position pairs.

## Why it works

### Compressed prefix lengths

When final characters differ, a shared subsequence must omit at least one
of them, so skipping either character covers every possibility. When they
match, an optimum can end with that shared character after an optimum of
the shorter prefixes, giving diagonal+1. The compressed row preserves all
three predecessor values before each transition, so it computes the same
states as a full two-dimensional table.

### Increasing match positions

An increasing sequence of positions corresponds to shared characters in order. Descending
positions for one source character prevent using it twice. Conversely, every common
subsequence appears as an increasing match sequence.

## Walkthrough

For "axb" and "ab", the rows are [0,1,1] after a, unchanged after x,
and [0,1,2] after b. The common subsequence "ab" has length 2.

## Cost and pitfalls

For the default Compressed prefix lengths approach:

O(m*n) time and O(min(m,n)) space; strings are unchanged and never sliced.
Save the diagonal before replacement. A common substring requires consecutive
characters and is a different task. This method computes length, not the
actual character sequence; reconstruction needs additional retained information.

Compressed prefix lengths: O(m*n) time; O(min(m,n)) space.
Increasing match positions: O(m+n+r log n) time; O(n) space.
Position matching is attractive for sparse matches but can be slower on repeated letters. It
streams the r matching-position events rather than storing them, keeping actual auxiliary
storage O(n).
"""


class Solution:
    """Approach: Compressed prefix lengths
    Time: O(m*n)
    Space: O(min(m,n))
    """

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text1) < len(text2):
            text1, text2 = text2, text1
        dp = [0] * (len(text2) + 1)
        for first in text1:
            diagonal = 0
            for column, second in enumerate(text2, 1):
                above = dp[column]
                dp[column] = diagonal + 1 if first == second else max(above, dp[column - 1])
                diagonal = above
        return dp[-1]


class MatchPositionsSolution:
    """Approach: Increasing match positions
    Time: O(m+n+r log n)
    Space: O(n)
    """

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        from bisect import bisect_left

        positions = {}
        for index, character in enumerate(text2):
            positions.setdefault(character, []).append(index)
        tails = []
        for character in text1:
            for position in reversed(positions.get(character, ())):
                place = bisect_left(tails, position)
                if place == len(tails):
                    tails.append(position)
                else:
                    tails[place] = position
        return len(tails)
