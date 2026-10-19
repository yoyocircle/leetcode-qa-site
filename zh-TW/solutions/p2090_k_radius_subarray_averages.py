"""
## Task

For each index return the integer average of its radius-k window, or -1 if that window crosses
an array endpoint. Values are nonnegative.

## Hints

1. Each complete window has width 2k+1.
2. Slide one sum or subtract two prefix sums.

## Approach

### One rolling window sum

Initialize a width-(2k+1) sum, write its center average, then subtract the departing value and
add the next value.

### Prefix sums per center

Build a padded prefix-sum array and evaluate every center whose left and right boundaries fit.

## Why it works

### One rolling window sum

The running sum contains exactly the current complete window. Its center is uniquely determined
by its right endpoint; every valid center is visited once and other entries remain -1.

### Prefix sums per center

Subtracting prefixes at center-k and center+k+1 includes exactly the 2k+1 window entries.
Integer division then computes its required truncated average.

## Walkthrough

[7,4,3,9,1,8,5,2,6], k=3 has complete seven-element windows centered at 3,4,5, whose averages
are 5,4,4.

## Cost and pitfalls

One rolling window sum: O(n) time; O(1) auxiliary plus output space.

Prefix sums per center: O(n) time; O(n) auxiliary plus output space.

Inputs are unchanged. k=0 returns the original values in a fresh list. The rolling
implementation avoids slicing the initial window, preserving constant auxiliary storage.
"""


class Solution:
    """Approach: One rolling window sum
    Time: O(n)
    Space: O(1) auxiliary plus output
    """

    def getAverages(self, nums: list[int], k: int) -> list[int]:
        width = 2 * k + 1
        answer = [-1] * len(nums)
        if width > len(nums):
            return answer
        total = sum(nums[i] for i in range(width))
        answer[k] = total // width
        for right in range(width, len(nums)):
            total += nums[right] - nums[right - width]
            answer[right - k] = total // width
        return answer


class PrefixSolution:
    """Approach: Prefix sums per center
    Time: O(n)
    Space: O(n) auxiliary plus output
    """

    def getAverages(self, nums: list[int], k: int) -> list[int]:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        answer = [-1] * len(nums)
        for center in range(k, len(nums) - k):
            answer[center] = (prefix[center + k + 1] - prefix[center - k]) // (2 * k + 1)
        return answer
