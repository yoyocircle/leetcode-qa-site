"""
## Task

For each array position, return the product of every other value. The required
solution is linear and cannot use division. Zeros and negative numbers are valid.

## Hints

1. Separate the elements before a position from those after it.
2. Can the output array store one of those two partial products?

## Approach

### Two running products

A nested scan costs O(n squared). Instead, write the product strictly to each
position's left into the output. Walk backward with a running product strictly
to the right and multiply it into the saved left product.

### Prefix and suffix arrays

Store explicit prefix and suffix products, then combine entries around each index. This uses
more space but makes the exclusion boundary visible.

## Why it works

### Two running products

The two products cover every input element exactly once except the current
element. Updating the running product after writing preserves this exclusion.

### Prefix and suffix arrays

prefix[i] contains exactly indices below i, and suffix[i+1] contains exactly indices above i.
Their product includes every required factor once, including zeros correctly.

## Walkthrough

For [2, 0, 4], left products are [1, 2, 0]. Right products are [0, 4, 1].
Their position-wise products give [0, 8, 0].

## Cost and pitfalls

Default approach (Two running products):

O(n) time and O(1) auxiliary space, excluding the O(n) output. Inputs are
unchanged. Initialize products to 1, not 0. Multiply before incorporating the
current element. Division would both violate the requirement and mishandle zeros.

Two running products: O(n) time; O(1) auxiliary, O(n) output space.
Prefix and suffix arrays: O(n) time; O(n) space. Store explicit prefix and suffix products, then
combine entries around each index. This uses more space but makes the exclusion boundary
visible.
"""


class Solution:
    """Approach: Two running products
    Time: O(n)
    Space: O(1) auxiliary, O(n) output
    """

    def productExceptSelf(self, nums: list[int]) -> list[int]:
        result = [1] * len(nums)
        prefix = 1
        for i, number in enumerate(nums):
            result[i] = prefix
            prefix *= number
        suffix = 1
        for i in range(len(nums) - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result


class PrefixSuffixSolution:
    """Approach: Prefix and suffix arrays
    Time: O(n)
    Space: O(n)
    """

    def productExceptSelf(self, nums: list[int]) -> list[int]:
        size = len(nums)
        prefix = [1] * (size + 1)
        suffix = [1] * (size + 1)
        for i in range(size):
            prefix[i + 1] = prefix[i] * nums[i]
        for i in range(size - 1, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i]
        return [prefix[i] * suffix[i + 1] for i in range(size)]
