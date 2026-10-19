"""## Task

Partition an array into blocks of length at most k; replace each block by its maximum and
maximize the resulting sum.

## Hints

1. The final block contributes its length times its maximum.
2. Its maximum can be maintained while extending the block backward.

## Approach

### Prefix DP with backward block extension

For every ending prefix, extend its final block backward up to k entries and maintain the
maximum as one more entry joins.

### Suffix DP with a rolling ring buffer

Solve suffixes backward and try the first block of each suffix. Store only the next k suffix
answers in a circular buffer of k+1 positions.

## Why it works

### Prefix DP with backward block extension

Every partition has one final block of a tested length. Its preceding prefix is already
optimal, so maximizing these exhaustive final-block choices produces the best total.

### Suffix DP with a rolling ring buffer

All referenced suffixes start within k positions, so none has been overwritten in the ring.
Trying each possible first block is exhaustive and combines it with an optimal remaining
suffix.

## Walkthrough

For [1,5,2] and k=2, blocks [1,5] and [2] yield 5+5+2=12.

## Cost and pitfalls

Prefix DP with backward block extension: O(n*k) time; O(n) space.
Suffix DP with a rolling ring buffer: O(n*k) time; O(k) space.

Both preserve the array. The ring variant saves memory and performs no slices, but modulo
indexing is less transparent. Nonnegative entries justify the zero initial maximum.
"""


class Solution:
    """Approach: Prefix DP with backward block extension
    Time: O(n*k)
    Space: O(n)
    """

    def maxSumAfterPartitioning(self, arr: list[int], k: int) -> int:
        dp = [0] * (len(arr) + 1)
        for end in range(1, len(arr) + 1):
            maximum = 0
            for length in range(1, min(k, end) + 1):
                maximum = max(maximum, arr[end - length])
                dp[end] = max(dp[end], dp[end - length] + maximum * length)
        return dp[-1]


class SuffixSolution:
    """Approach: Suffix DP with a rolling ring buffer
    Time: O(n*k)
    Space: O(k)
    """

    def maxSumAfterPartitioning(self, arr: list[int], k: int) -> int:
        size = min(k, len(arr)) + 1
        dp = [0] * size
        for start in range(len(arr) - 1, -1, -1):
            maximum = answer = 0
            for end in range(start, min(len(arr), start + k)):
                maximum = max(maximum, arr[end])
                answer = max(answer, maximum * (end - start + 1) + dp[(end + 1) % size])
            dp[start % size] = answer
        return dp[0]
