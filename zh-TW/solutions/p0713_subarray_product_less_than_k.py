"""
## Task

Count contiguous nonempty subarrays whose product is strictly less than k. All array entries are
positive integers.

## Hints

1. For one right endpoint, every suffix of a valid window is valid.
2. If k is at most one, no positive product qualifies.

## Approach

### Multiplicative sliding window

Multiply in each value and divide outgoing factors while the product is too large. Add the
number of possible starts in the surviving window.

### Exact prefix products with binary search

Build arbitrary-precision prefix products. For each end, binary-search earlier prefix products
greater than prefix[end] // k. This avoids logarithm rounding, but huge integers make it an
educational baseline that may time out.

## Why it works

### Multiplicative sliding window

Positive integer factors make shortening a window nonincreasing in product. The surviving left
endpoint is the earliest valid start, so exactly right-left+1 subarrays ending here qualify.

### Exact prefix products with binary search

For positive prefix products P, P[end]/P[start] < k is equivalent to P[start] > P[end]//k.
Prefix products are nondecreasing even with ones, so upper bound counts all eligible starts
exactly.

## Walkthrough

[10,5,2,6], k=100 contributes 1,2,2,3 valid suffixes at its four endpoints, totaling 8.

## Cost and pitfalls

Multiplicative sliding window: O(n) arithmetic operations time; O(1) integer variables space.

Exact prefix products with binary search: O(n log n) big-integer operations time; O(n squared
log M) bits worst case space.

Inputs are unchanged. Strict inequality needs an upper bound in the prefix method. M is the
maximum value; the default maintains products bounded by k times one incoming value.
"""

from bisect import bisect_right


class Solution:
    """Approach: Multiplicative sliding window
    Time: O(n) arithmetic operations
    Space: O(1) integer variables
    """

    def numSubarrayProductLessThanK(self, nums: list[int], k: int) -> int:
        if k <= 1:
            return 0
        product = 1
        left = answer = 0
        for right, value in enumerate(nums):
            product *= value
            while product >= k:
                product //= nums[left]
                left += 1
            answer += right - left + 1
        return answer


class PrefixProductSolution:
    """Approach: Exact prefix products with binary search
    Time: O(n log n) big-integer operations
    Space: O(n squared log M) bits worst case
    """

    def numSubarrayProductLessThanK(self, nums: list[int], k: int) -> int:
        if k <= 1:
            return 0
        prefix = [1]
        for value in nums:
            prefix.append(prefix[-1] * value)
        answer = 0
        for end in range(1, len(prefix)):
            first = bisect_right(prefix, prefix[end] // k, 0, end)
            answer += end - first
        return answer
