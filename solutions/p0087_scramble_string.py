"""## Task

Decide whether recursively splitting a string into two nonempty parts, optionally swapping
parts at each split, can transform s1 into s2.

## Hints

1. A split either preserves child order or swaps the two children.
2. Different character multisets rule out a state before trying its splits.

## Approach

### Memoized substring-index split states

Cache two start indices and a shared length. Return immediately for equal ranges, reject
unequal character counts using prefix frequencies, and try every split in both child orders.

### Bottom-up length and position table

Seed one-character matches, then fill increasing substring lengths while trying every
two-part split with original or swapped alignment.

## Why it works

### Memoized substring-index split states

Every recursive scrambling has one top split and one of the two child orders. Testing all
splits with recursively valid children is sufficient and necessary; preserving character
multiplicities is an additional necessary pruning condition.

### Bottom-up length and position table

Both child lengths are strictly smaller than the parent, so their answers are already
available. The same exhaustive split characterization yields an exact bottom-up result
without recursion.

## Walkthrough

"great" can become "rgeat" by scrambling the "gr" part into "rg" while preserving "eat".

## Cost and pitfalls

Memoized substring-index split states: O(n^4) time; O(n^3) space.
Bottom-up length and position table: O(n^4) time; O(n^3) space.

Both preserve strings and use index ranges rather than allocating substrings. n<=30 keeps
memo recursion depth bounded. The table computes even unreachable pair states; memoization
can prune many using equality and frequency checks.
"""


class Solution:
    """Approach: Memoized substring-index split states
    Time: O(n^4)
    Space: O(n^3)
    """

    def isScramble(self, s1: str, s2: str) -> bool:
        from functools import cache

        def prefixes(text):
            table = [[0] * 26]
            for character in text:
                row = table[-1].copy()
                row[ord(character) - ord("a")] += 1
                table.append(row)
            return table

        first, second = prefixes(s1), prefixes(s2)

        @cache
        def solve(i, j, length):
            if all(s1[i + offset] == s2[j + offset] for offset in range(length)):
                return True
            if any(
                first[i + length][letter] - first[i][letter]
                != second[j + length][letter] - second[j][letter]
                for letter in range(26)
            ):
                return False
            for cut in range(1, length):
                if solve(i, j, cut) and solve(i + cut, j + cut, length - cut):
                    return True
                if solve(i, j + length - cut, cut) and solve(i + cut, j, length - cut):
                    return True
            return False

        return solve(0, 0, len(s1))


class TableSolution:
    """Approach: Bottom-up length and position table
    Time: O(n^4)
    Space: O(n^3)
    """

    def isScramble(self, s1: str, s2: str) -> bool:
        n = len(s1)
        dp = [[[False] * n for _ in range(n)] for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                dp[1][i][j] = s1[i] == s2[j]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for j in range(n - length + 1):
                    dp[length][i][j] = any(
                        (dp[cut][i][j] and dp[length - cut][i + cut][j + cut])
                        or (dp[cut][i][j + length - cut] and dp[length - cut][i + cut][j])
                        for cut in range(1, length)
                    )
        return dp[n][0][0]
