"""
## Task

Return the maximum length of a subsequence whose successive nonzero differences strictly
alternate positive and negative. A singleton qualifies.

## Hints

1. Track the best subsequence ending in an up step and in a down step.
2. An equal pair cannot extend a wiggle.

## Approach

### Compressed up/down greedy states

Compare adjacent values. A rise extends the best down-ending length by one; a fall extends the
best up-ending length.

### Per-index alternating-subsequence DP

For each endpoint, inspect every earlier endpoint and extend only a subsequence ending with the
opposite direction. This slower baseline may time out if input limits are enlarged.

## Why it works

### Compressed up/down greedy states

Within a run moving in one direction, retaining its more extreme endpoint leaves at least as
much room for a future reversal. Only direction changes need extend the chosen subsequence,
which the two states count.

### Per-index alternating-subsequence DP

Every non-singleton wiggle has a penultimate index and an opposite final step direction there.
Enumerating those predecessor states implements the complete optimal-substructure recurrence.

## Walkthrough

[1,7,4,9,2,5] alternates at every step and has answer 6. [1,2,3,4] has answer 2 despite four
increasing values.

## Cost and pitfalls

Compressed up/down greedy states: O(n) time; O(1) space.

Per-index alternating-subsequence DP: O(n squared) time; O(n) space.

Inputs are unchanged. Both methods handle repeated values by adding no step on equality. The
quadratic DP is viable for the stated small length bound but illustrates the work removed by
state compression.
"""


class Solution:
    """Approach: Compressed up/down greedy states
    Time: O(n)
    Space: O(1)
    """

    def wiggleMaxLength(self, nums: list[int]) -> int:
        up = down = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                up = down + 1
            elif nums[i] < nums[i - 1]:
                down = up + 1
        return max(up, down)


class QuadraticDPSolution:
    """Approach: Per-index alternating-subsequence DP
    Time: O(n squared)
    Space: O(n)
    """

    def wiggleMaxLength(self, nums: list[int]) -> int:
        up = [1] * len(nums)
        down = [1] * len(nums)
        for i, value in enumerate(nums):
            for j in range(i):
                if nums[j] < value:
                    up[i] = max(up[i], down[j] + 1)
                elif nums[j] > value:
                    down[i] = max(down[i], up[j] + 1)
        return max(max(up), max(down))
