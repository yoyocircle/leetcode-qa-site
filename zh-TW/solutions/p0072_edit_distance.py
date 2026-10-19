"""## Task

Find the fewest single-character insertions, deletions, and replacements
needed to turn one string into another. Each operation costs one.

## Hints

1. Define a state for transforming one prefix into another prefix.
2. Its last operation depends on the above, left, or diagonal prefix state.

## Approach

### Rolling edit-distance row

Use the shorter string as columns because edit distance is symmetric.
Initialize dp[j]=j: transforming an empty source into j characters requires
j insertions. For source row i, set dp[0]=i for deletions. Visit columns
left to right while saving the old diagonal. Matching characters reuse that
diagonal. Otherwise use one plus the minimum of above, left, and diagonal,
which respectively represent deletion, insertion, and replacement.

### Full prefix edit table

Retain all prefix-pair distances. Initialize the top row as insertion counts and first
column as deletion counts; fill matching diagonals or the cheapest edit predecessor.

## Why it works

### Rolling edit-distance row

Any optimal transformation either matches the two final characters or ends
with one of the three allowed edits. Removing that final action leaves
a transformation between one of the predecessor prefix pairs. Choosing its
optimal cost cannot worsen the result. Trying all final actions finds the
minimum, while each transition constructs a valid transformation. Boundary
initialization covers empty prefixes, so induction proves the table correct.

### Full prefix edit table

Each predecessor corresponds to exactly one legal final edit, and a match consumes equal
characters for free. The minimum covers every transformation; retaining the full table
preserves the same recurrence without overwriting dependencies.

## Walkthrough

For "cat" to "cut", matching c costs zero, replacing a with u costs one,
and matching t adds nothing. The final distance is 1. From "cat" to the
empty string, initialization records three deletions.

## Cost and pitfalls

For the default Rolling edit-distance row approach:

O(m*n+m+n) time and O(min(m,n)+1) space; strings are unchanged. Save the old
above value before overwriting it so the next diagonal remains available.
Matching characters cost zero. Transposition is not one of the allowed
operations, so swapping two letters does not automatically cost one.

Rolling edit-distance row: O(m*n+m+n) time; O(min(m,n)+1) space.
Full prefix edit table: O((m+1)*(n+1)) time; O((m+1)*(n+1)) space.
The full table makes edit reconstruction possible with an added backward walk; this
implementation returns only the cost. Both support empty strings and preserve them.
"""


class Solution:
    """Approach: Rolling edit-distance row
    Time: O(m*n+m+n)
    Space: O(min(m,n)+1)
    """

    def minDistance(self, word1: str, word2: str) -> int:
        if len(word1) < len(word2):
            word1, word2 = word2, word1
        dp = list(range(len(word2) + 1))
        for row, first in enumerate(word1, 1):
            diagonal = dp[0]
            dp[0] = row
            for column, second in enumerate(word2, 1):
                above = dp[column]
                dp[column] = (
                    diagonal if first == second else 1 + min(above, dp[column - 1], diagonal)
                )
                diagonal = above
        return dp[-1]


class TableSolution:
    """Approach: Full prefix edit table
    Time: O((m+1)*(n+1))
    Space: O((m+1)*(n+1))
    """

    def minDistance(self, word1: str, word2: str) -> int:
        table = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]
        for i in range(len(word1) + 1):
            table[i][0] = i
        for j in range(len(word2) + 1):
            table[0][j] = j
        for i, first in enumerate(word1, 1):
            for j, second in enumerate(word2, 1):
                table[i][j] = (
                    table[i - 1][j - 1]
                    if first == second
                    else 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
                )
        return table[-1][-1]
