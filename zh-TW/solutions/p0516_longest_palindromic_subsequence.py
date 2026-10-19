"""## Task

Return the maximum length of a palindromic subsequence; skipped characters need not be adjacent.

## Hints

1. Compare the two endpoints of an interval.
2. A palindromic subsequence has the same characters in reverse order.

## Approach

### Interval palindrome table

Fill left endpoints backward and right endpoints forward. Equal endpoints wrap an inner
palindrome; otherwise omit either endpoint.

### LCS against the reversed string

Compute only the length of a longest common subsequence of s and its reversed copy using a
rolling row.

## Why it works

### Interval palindrome table

An optimal palindrome can use both equal endpoints around an optimal interior. If endpoints
differ they cannot both be used as the outside pair, so at least one must be omitted.

### LCS against the reversed string

Every palindromic subsequence is common to both strings. Conversely, a longest common
subsequence can be symmetrized around the crossing of forward and reverse positions without
reducing its length, giving an equally long palindrome. This equivalence is for length;
arbitrary LCS reconstruction need not itself be palindromic.

## Walkthrough

For "bbab", select the first, second, and fourth letters to obtain "bbb" of length 3.

## Cost and pitfalls

Interval palindrome table: O(n^2) time; O(n^2) space.
LCS against the reversed string: O(n^2) time; O(n) space.

The reversed copy costs O(n) time and space. Neither method mutates the string. Retain the
old diagonal before a rolling-row update.
"""


class Solution:
    """Approach: Interval palindrome table
    Time: O(n^2)
    Space: O(n^2)
    """

    def longestPalindromeSubseq(self, s: str) -> int:
        dp = [[0] * len(s) for _ in s]
        for left in range(len(s) - 1, -1, -1):
            dp[left][left] = 1
            for right in range(left + 1, len(s)):
                dp[left][right] = (
                    2 + dp[left + 1][right - 1]
                    if s[left] == s[right]
                    else max(dp[left + 1][right], dp[left][right - 1])
                )
        return dp[0][-1]


class LCSSolution:
    """Approach: LCS against the reversed string
    Time: O(n^2)
    Space: O(n)
    """

    def longestPalindromeSubseq(self, s: str) -> int:
        reverse = s[::-1]
        dp = [0] * (len(s) + 1)
        for first in s:
            diagonal = 0
            for column, second in enumerate(reverse, 1):
                above = dp[column]
                dp[column] = diagonal + 1 if first == second else max(above, dp[column - 1])
                diagonal = above
        return dp[-1]
