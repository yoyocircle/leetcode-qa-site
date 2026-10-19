"""## Task

Connect equal values in two arrays with the maximum number of lines that do not cross and do
not share an endpoint.

## Hints

1. Noncrossing selected positions must be increasing in both arrays.
2. Reverse the matching-position order within one source element to avoid reusing that element.

## Approach

### Rolling longest-common-subsequence DP

Treat the problem as LCS: matching values may extend the diagonal, and differing values
require skipping an endpoint. Retain one row plus the old diagonal.

### LIS over streamed matching positions

Index every occurrence in the second array. For each first-array value, process matching
second-array positions descending and feed them into strict LIS tails.

## Why it works

### Rolling longest-common-subsequence DP

Two lines cross exactly when their endpoint orders disagree. Thus a legal set of lines is an
equal-valued common subsequence, and maximizing its length maximizes uncrossed lines.

### LIS over streamed matching positions

Increasing positions select noncrossing equal-valued connections. Descending matches from
one source element cannot both enter an increasing subsequence, so endpoint reuse is
excluded. Every legal line set appears among the streamed match choices.

## Walkthrough

For [1,4,2] and [1,2,4], either 1 then 4 or 1 then 2 gives two uncrossed lines.

## Cost and pitfalls

Rolling longest-common-subsequence DP: O(m*n) time; O(n) space.
LIS over streamed matching positions: O(m+n+r*log(n+1)) time; O(n) space.

m,n are input lengths and r the number of equal-valued position pairs. Both preserve arrays.
Match events are streamed, not stored as an O(r) list; repeated values can make r=m*n and
favor the simple DP instead.
"""


class Solution:
    """Approach: Rolling longest-common-subsequence DP
    Time: O(m*n)
    Space: O(n)
    """

    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:
        dp = [0] * (len(nums2) + 1)
        for first in nums1:
            diagonal = 0
            for j, second in enumerate(nums2, 1):
                above = dp[j]
                dp[j] = diagonal + 1 if first == second else max(above, dp[j - 1])
                diagonal = above
        return dp[-1]


class MatchPositionsSolution:
    """Approach: LIS over streamed matching positions
    Time: O(m+n+r*log(n+1))
    Space: O(n)
    """

    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:
        from bisect import bisect_left

        positions = {}
        for index, value in enumerate(nums2):
            positions.setdefault(value, []).append(index)
        tails = []
        for value in nums1:
            for position in reversed(positions.get(value, ())):
                index = bisect_left(tails, position)
                if index == len(tails):
                    tails.append(position)
                else:
                    tails[index] = position
        return len(tails)
