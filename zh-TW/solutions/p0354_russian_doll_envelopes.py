"""## Task

Find the longest chain of envelopes with both width and height strictly increasing.

## Hints

1. Sort widths, but prevent equal-width envelopes from extending each other.
2. Then solve strict LIS on heights, or compare every smaller envelope directly.

## Approach

### Width sort and height LIS

Sort ascending width and descending height for equal widths. Apply strict
increasing-subsequence tails to heights.

### All-predecessor nesting DP

Sort into a dependency order and explicitly test both dimensions against every earlier envelope.

## Why it works

### Width sort and height LIS

Descending heights prevent an increasing subsequence from selecting two equal-width entries.
For different widths, increasing heights exactly characterize valid nesting; the
smallest-tail invariant gives the longest chain.

### All-predecessor nesting DP

The final predecessor of any chain ending here must be smaller in both coordinates. All such
candidates appear earlier after sorting, so their best lengths provide the exact recurrence.

## Walkthrough

For [[2,3],[2,4],[3,5]], only one width-two envelope can precede [3,5], giving 2.

## Cost and pitfalls

Width sort and height LIS: O(n log n) time; O(n) space.
All-predecessor nesting DP: O(n^2) time; O(n) space.

Sorted copies preserve input and cost O(n) reference storage. The quadratic baseline may
time out at n=100000; use the default for full constraints. bisect_left enforces strict
height growth.
"""


class Solution:
    """Approach: Width sort and height LIS
    Time: O(n log n)
    Space: O(n)
    """

    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        from bisect import bisect_left

        ordered = sorted(envelopes, key=lambda pair: (pair[0], -pair[1]))
        tails = []
        for _, height in ordered:
            position = bisect_left(tails, height)
            if position == len(tails):
                tails.append(height)
            else:
                tails[position] = height
        return len(tails)


class QuadraticSolution:
    """Approach: All-predecessor nesting DP
    Time: O(n^2)
    Space: O(n)
    """

    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        ordered = sorted(envelopes)
        dp = [1] * len(ordered)
        for i, (width, height) in enumerate(ordered):
            for j in range(i):
                if ordered[j][0] < width and ordered[j][1] < height:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
