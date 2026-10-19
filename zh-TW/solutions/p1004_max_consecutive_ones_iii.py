"""
## Task

Return the longest binary subarray that can become all ones by changing at most k zeroes.

## Hints

1. Count zeroes rather than changed positions.
2. Zero positions can delimit every candidate window.

## Approach

### Zero-budget window

Extend right and shrink from left until the number of zeroes is at most k.

### Sentinel zero-position intervals

Record zero positions with sentinels -1 and n. A block containing k consecutive zeroes extends
between the zero just before and just after that block.

## Why it works

### Zero-budget window

For each right endpoint, the smallest left endpoint satisfying the zero budget gives the longest
valid suffix. Earlier starts are invalid, so taking the largest suffix is optimal.

### Sentinel zero-position intervals

Every maximal valid window lies between two excluded zeroes and contains at most k zeroes.
Enumerating blocks of exactly k zeroes covers the optimum unless all zeroes can be flipped, when
the full array is valid.

## Walkthrough

[1,1,0,0,1,1,1,0], k=1 has best length 4, from either zero next to the final run of three ones.

## Cost and pitfalls

Zero-budget window: O(n) time; O(1) space.

Sentinel zero-position intervals: O(n) time; O(n) space.

Inputs are unchanged. k=0 still works: consecutive excluded zeroes delimit ordinary runs of
ones.
"""


class Solution:
    """Approach: Zero-budget window
    Time: O(n)
    Space: O(1)
    """

    def longestOnes(self, nums: list[int], k: int) -> int:
        left = zeroes = best = 0
        for right, value in enumerate(nums):
            zeroes += value == 0
            while zeroes > k:
                zeroes -= nums[left] == 0
                left += 1
            best = max(best, right - left + 1)
        return best


class ZeroPositionSolution:
    """Approach: Sentinel zero-position intervals
    Time: O(n)
    Space: O(n)
    """

    def longestOnes(self, nums: list[int], k: int) -> int:
        zeroes = [-1] + [i for i, value in enumerate(nums) if value == 0] + [len(nums)]
        count = len(zeroes) - 2
        if count <= k:
            return len(nums)
        return max(zeroes[i + k + 1] - zeroes[i] - 1 for i in range(count - k + 1))
