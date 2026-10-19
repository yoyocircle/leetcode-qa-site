"""## Task

Return the greatest length of a contiguous subarray appearing in both integer arrays.

## Hints

1. Matching suffix lengths reset to zero on a mismatch.
2. Existence of a common window is monotone in window length.

## Approach

### Backward-updated matching suffix lengths

Store lengths of equal suffixes ending at the current pair of endpoints. Update the
second-array positions backward so the old diagonal remains available.

### Binary-search exact tuple windows

For a candidate length, store all exact tuple windows from the first array and test windows
from the second. Binary-search the greatest feasible length.

## Why it works

### Backward-updated matching suffix lengths

Equal final elements extend the equal suffix one step; unequal elements force length zero.
Every common contiguous block ends at some endpoint pair, so the maximum state gives the
optimum.

### Binary-search exact tuple windows

A common window of length L contains common windows of every smaller length, so feasibility
is monotone. Tuple equality confirms exact contents even when hashes collide, making this
deterministic in correctness.

## Walkthrough

For [1,2,3,2,1] and [3,2,1,4], the shared contiguous block [3,2,1] has length 3.

## Cost and pitfalls

Backward-updated matching suffix lengths: O(m*n) time; O(n) space.
Binary-search exact tuple windows: O((m+n)*L*log(L+1)) expected time; O(m*L) space.

L=min(m,n). Both preserve arrays. Tuple construction, input slicing, and tuple hashing each
cost O(window length); the window baseline is not a linear-time rolling hash and may be
slower near full limits. The suffix DP finds contiguous blocks, not subsequences.
"""


class Solution:
    """Approach: Backward-updated matching suffix lengths
    Time: O(m*n)
    Space: O(n)
    """

    def findLength(self, nums1: list[int], nums2: list[int]) -> int:
        dp = [0] * (len(nums2) + 1)
        answer = 0
        for first in nums1:
            for j in range(len(nums2), 0, -1):
                dp[j] = dp[j - 1] + 1 if first == nums2[j - 1] else 0
                answer = max(answer, dp[j])
        return answer


class WindowSolution:
    """Approach: Binary-search exact tuple windows
    Time: O((m+n)*L*log(L+1)) expected
    Space: O(m*L)
    """

    def findLength(self, nums1: list[int], nums2: list[int]) -> int:
        def possible(length):
            windows = {
                tuple(nums1[start : start + length]) for start in range(len(nums1) - length + 1)
            }
            return any(
                tuple(nums2[start : start + length]) in windows
                for start in range(len(nums2) - length + 1)
            )

        low, high = 0, min(len(nums1), len(nums2)) + 1
        while low + 1 < high:
            middle = (low + high) // 2
            if possible(middle):
                low = middle
            else:
                high = middle
        return low
