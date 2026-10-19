"""## Task

Find the greatest product of a nonempty contiguous subarray of integers.

## Hints

1. A negative factor swaps the useful maximum and minimum products.
2. Zero divides the input into independent nonzero runs.

## Approach

### Maximum and minimum ending products

Retain both extremes for products ending at the preceding position. The next product either
restarts or multiplies either extreme.

### Prefix and suffix product scans

Scan products simultaneously from both ends, restarting after a zero. Compare all run
prefixes and suffixes.

## Why it works

### Maximum and minimum ending products

Multiplication by a positive factor preserves order, by a negative factor reverses order,
and by zero collapses all products. Thus both extremes suffice for every possible next
factor.

### Prefix and suffix product scans

Within a nonzero integer run, absolute factors are at least one. With an even negative
count, the whole run is optimal; with an odd count, drop through the first or last negative.
Prefix/suffix scans cover both choices and zero itself.

## Walkthrough

For [-2,3,-4], retaining the negative product -6 allows the final product 24.

## Cost and pitfalls

Maximum and minimum ending products: O(n) time; O(1) space.
Prefix and suffix product scans: O(n) time; O(1) space.

Inputs are unchanged. The bidirectional argument uses integer factors; arbitrary fractions
would invalidate it. Preserve old high and low values during simultaneous updates.
"""


class Solution:
    """Approach: Maximum and minimum ending products
    Time: O(n)
    Space: O(1)
    """

    def maxProduct(self, nums: list[int]) -> int:
        high = low = answer = nums[0]
        for index in range(1, len(nums)):
            value = nums[index]
            high, low = max(value, high * value, low * value), min(value, high * value, low * value)
            answer = max(answer, high)
        return answer


class BidirectionalSolution:
    """Approach: Prefix and suffix product scans
    Time: O(n)
    Space: O(1)
    """

    def maxProduct(self, nums: list[int]) -> int:
        answer = nums[0]
        prefix = suffix = 1
        for index in range(len(nums)):
            prefix = (prefix if prefix else 1) * nums[index]
            suffix = (suffix if suffix else 1) * nums[-1 - index]
            answer = max(answer, prefix, suffix)
        return answer
