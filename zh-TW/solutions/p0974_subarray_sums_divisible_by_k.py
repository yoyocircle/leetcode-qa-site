"""
## Task

Count nonempty subarrays whose sum is divisible by positive k. Values may be negative.

## Hints

1. Reduce every prefix sum modulo k.
2. Each pair of equal prefix remainders contributes one subarray.

## Approach

### Online remainder frequencies

Use a length-k count array. Add the frequency of the current remainder before recording this
prefix.

### Batch grouping of prefix remainders

Count every prefix remainder first, then add c choose 2 for each remainder group.

## Why it works

### Online remainder frequencies

Earlier equal remainders correspond one-to-one with qualifying subarrays ending here. Looking up
before insertion excludes the empty subarray.

### Batch grouping of prefix remainders

Every unordered pair of prefix positions in one group has a unique earlier and later endpoint
and defines one divisible nonempty subarray. There are c(c-1)/2 such pairs.

## Walkthrough

For [4,5,0,-2,-3,1], k=5, the remainder group sizes are 2,4,1, giving 1+6+0 = 7.

## Cost and pitfalls

Online remainder frequencies: O(n+k) time; O(k) space.

Batch grouping of prefix remainders: O(n) expected time; O(min(n,k)) space.

Inputs are unchanged. Python modulo already normalizes negative sums to 0..k-1. Seed the empty
prefix in both methods.
"""


class Solution:
    """Approach: Online remainder frequencies
    Time: O(n+k)
    Space: O(k)
    """

    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        counts = [0] * k
        counts[0] = 1
        remainder = answer = 0
        for value in nums:
            remainder = (remainder + value) % k
            answer += counts[remainder]
            counts[remainder] += 1
        return answer


class BatchSolution:
    """Approach: Batch grouping of prefix remainders
    Time: O(n) expected
    Space: O(min(n,k))
    """

    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        counts = {0: 1}
        remainder = 0
        for value in nums:
            remainder = (remainder + value) % k
            counts[remainder] = counts.get(remainder, 0) + 1
        return sum(count * (count - 1) // 2 for count in counts.values())
