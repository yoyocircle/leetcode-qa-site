"""## Task

Decide whether a target string can be made by interleaving two source
strings while preserving the character order within each source.

## Hints

1. Track how many characters have been consumed from each source.
2. Their sum fixes the target position, so it is not a third state dimension.

## Approach

### Rolling interleaving states

Reject unequal total lengths first. Put the shorter source in columns.
Let dp[j] record whether the current prefix of the first source and j
characters of the second source form the corresponding target prefix.
Initialize the zero-source row by matching the second source alone. For
each first-source character, visit columns left to right. A state succeeds
through the old state above plus that character, or the updated state to
the left plus the second-source character.

### BFS over consumed-prefix pairs

Traverse only reachable consumed-prefix pairs. From (i,j), consume the next matching
character of either source; a visited set merges routes reaching the same state.

## Why it works

### Rolling interleaving states

The final target character must come from exactly one source. Removing
it gives one of the two smaller prefix states. Each successful transition
preserves the source order and matches the target character, hence creates
a legal interleaving. Conversely, the final source choice of any legal
interleaving is tested. Induction over consumed prefixes proves completeness.

### BFS over consumed-prefix pairs

A transition consumes exactly one source character matching the next target character. Every
legal interleaving follows such transitions, and reaching both source ends establishes a
complete match.

## Walkthrough

For sources "ab" and "ac" with target "aabc", consume a from the first,
a from the second, b from the first, and c from the second. Repeated a
characters make greedy source selection ambiguous; DP retains both possibilities.

## Cost and pitfalls

For the default Rolling interleaving states approach:

O(m*n+m+n) time and O(min(m,n)) space, including empty-source initialization.
Inputs are unchanged. Update left to right and use target index i+j-1.
Character counts alone are insufficient because source order also matters.

Rolling interleaving states: O(m*n+m+n) time; O(min(m,n)+1) space.
BFS over consumed-prefix pairs: O((m+1)*(n+1)) time; O((m+1)*(n+1)) space.
BFS may avoid unreachable table cells but uses a queue and set. The total-length check is
necessary in both models.
"""


class Solution:
    """Approach: Rolling interleaving states
    Time: O(m*n+m+n)
    Space: O(min(m,n)+1)
    """

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        dp = [False] * (len(s2) + 1)
        dp[0] = True
        for column in range(1, len(s2) + 1):
            dp[column] = dp[column - 1] and s2[column - 1] == s3[column - 1]
        for row, first in enumerate(s1, 1):
            dp[0] = dp[0] and first == s3[row - 1]
            for column, second in enumerate(s2, 1):
                target = s3[row + column - 1]
                dp[column] = (dp[column] and first == target) or (
                    dp[column - 1] and second == target
                )
        return dp[-1]


class BFSSolution:
    """Approach: BFS over consumed-prefix pairs
    Time: O((m+1)*(n+1))
    Space: O((m+1)*(n+1))
    """

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        from collections import deque

        if len(s1) + len(s2) != len(s3):
            return False
        queue = deque([(0, 0)])
        seen = {(0, 0)}
        while queue:
            i, j = queue.popleft()
            if i + j == len(s3):
                return True
            for ni, nj, matches in (
                (i + 1, j, i < len(s1) and s1[i] == s3[i + j]),
                (i, j + 1, j < len(s2) and s2[j] == s3[i + j]),
            ):
                if matches and (ni, nj) not in seen:
                    seen.add((ni, nj))
                    queue.append((ni, nj))
        return False
