"""## Task

Delete characters from two strings until they become equal, minimizing the sum of deleted
ASCII values.

## Hints

1. A mismatch must delete at least one of its two endpoint characters.
2. Equivalently maximize the total character weight of a common subsequence that is kept.

## Approach

### Rolling minimum-deletion prefix costs

Initialize empty-prefix deletion costs. Matching letters reuse the diagonal; otherwise
delete either current character and pay its ASCII value. Save the diagonal during row
compression.

### Maximum-weight common subsequence

Compute a common subsequence maximizing the sum of retained ASCII values. Subtract twice
that weight from the combined original string weights.

## Why it works

### Rolling minimum-deletion prefix costs

A common final character can be retained for free. If final characters differ, at least one
must be deleted; considering both possibilities covers every transformation and chooses its
minimum cost.

### Maximum-weight common subsequence

The retained common text survives once in each string, saving twice its weight. Maximizing
those savings is exactly minimizing deletions, and weighted LCS considers every legal
retention order.

## Walkthrough

For "sea" and "eat", retain "ea" and delete s and t, costing 115+116=231.

## Cost and pitfalls

Rolling minimum-deletion prefix costs: O(m*n+m+n) time; O(min(m,n)+1) space.
Maximum-weight common subsequence: O(m*n+m+n) time; O(n+1) space.

m and n are string lengths. Both preserve inputs and avoid slices. A longest common
subsequence by character count need not maximize ASCII weight; use weighted states. All
weights are positive.
"""


class Solution:
    """Approach: Rolling minimum-deletion prefix costs
    Time: O(m*n+m+n)
    Space: O(min(m,n)+1)
    """

    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        dp = [0]
        for character in s2:
            dp.append(dp[-1] + ord(character))
        for first in s1:
            diagonal = dp[0]
            dp[0] += ord(first)
            for j, second in enumerate(s2, 1):
                above = dp[j]
                dp[j] = (
                    diagonal
                    if first == second
                    else min(above + ord(first), dp[j - 1] + ord(second))
                )
                diagonal = above
        return dp[-1]


class KeepWeightSolution:
    """Approach: Maximum-weight common subsequence
    Time: O(m*n+m+n)
    Space: O(n+1)
    """

    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        dp = [0] * (len(s2) + 1)
        for first in s1:
            diagonal = 0
            for j, second in enumerate(s2, 1):
                above = dp[j]
                dp[j] = diagonal + ord(first) if first == second else max(above, dp[j - 1])
                diagonal = above
        return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * dp[-1]
