"""
## Task

Count contiguous nonempty subarrays whose minimum equals minK and maximum equals maxK.

## Hints

1. Track the latest out-of-range position and the latest occurrence of each required bound.
2. Inclusion-exclusion can remove windows missing either required endpoint value.

## Approach

### Latest bound and invalid positions

At each end, a valid start must follow the last invalid value and be no later than the earlier
of the latest minK and maxK occurrences.

### Four bounded-run counts by inclusion-exclusion

Count all windows staying inside [minK,maxK], subtract those missing minK and those missing
maxK, then restore windows missing both.

## Why it works

### Latest bound and invalid positions

Those inequalities are necessary and sufficient: they exclude every invalid value and include
both required bounds. The number of allowed starts is max(0,min(last_min,last_max)-last_bad).

### Four bounded-run counts by inclusion-exclusion

Within a permitted-value run, each endpoint contributes the run length in possible starts.
Inclusion-exclusion retains exactly windows containing both bound values while excluding out-of-
range values.

## Walkthrough

[1,3,5,2,7,5], bounds 1 and 5 gives [1,3,5] and [1,3,5,2]. The 7 resets every subsequent valid
starting boundary.

## Cost and pitfalls

Latest bound and invalid positions: O(n) time; O(1) space.

Four bounded-run counts by inclusion-exclusion: O(n) time; O(1) space.

Inputs are unchanged. minK=maxK must count runs of that single value; the inclusion-exclusion
helper naturally returns zero for an inverted interval.
"""


class Solution:
    """Approach: Latest bound and invalid positions
    Time: O(n)
    Space: O(1)
    """

    def countSubarrays(self, nums: list[int], minK: int, maxK: int) -> int:
        last_min = last_max = last_bad = -1
        answer = 0
        for i, value in enumerate(nums):
            if value < minK or value > maxK:
                last_bad = i
            if value == minK:
                last_min = i
            if value == maxK:
                last_max = i
            answer += max(0, min(last_min, last_max) - last_bad)
        return answer


class InclusionExclusionSolution:
    """Approach: Four bounded-run counts by inclusion-exclusion
    Time: O(n)
    Space: O(1)
    """

    def countSubarrays(self, nums: list[int], minK: int, maxK: int) -> int:
        def bounded(low, high):
            run = answer = 0
            for value in nums:
                run = run + 1 if low <= value <= high else 0
                answer += run
            return answer

        return (
            bounded(minK, maxK)
            - bounded(minK + 1, maxK)
            - bounded(minK, maxK - 1)
            + bounded(minK + 1, maxK - 1)
        )
