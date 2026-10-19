"""
## Task

Count nonempty subarrays with an odd sum and return the count modulo 1,000,000,007.

## Hints

1. A subarray is odd when its two prefix parities differ.
2. Track odd and even counts of subarrays ending at the current position as an alternative
   state.

## Approach

### Opposite-prefix parity counts

Maintain the number of even and odd prefix sums. A new prefix contributes the count of earlier
prefixes with opposite parity.

### Odd and even suffix dynamic programming

Track counts of odd and even subarrays ending here. An odd incoming value swaps their parity
roles and adds a one-element odd subarray; an even value adds a one-element even one.

## Why it works

### Opposite-prefix parity counts

Subtracting prefixes changes parity exactly when their parities differ. Every interval has one
pair of endpoints, so opposite-prefix counting includes every odd interval once.

### Odd and even suffix dynamic programming

Every suffix ending here is either the singleton or an older suffix extended by this value.
Updating those disjoint cases gives exact counts; summing the odd count over endpoints counts
the answer.

## Walkthrough

[1,3,5] has three odd singletons and one odd length-three subarray, giving four. The three
length-two subarrays for a longer odd run would be even.

## Cost and pitfalls

Opposite-prefix parity counts: O(n) time; O(1) space.

Odd and even suffix dynamic programming: O(n) time; O(1) space.

Inputs are unchanged. Only the final count is reduced modulo the required constant; parity
remains exact. Prefix counts and suffix counts have different meanings.
"""


class Solution:
    """Approach: Opposite-prefix parity counts
    Time: O(n)
    Space: O(1)
    """

    def numOfSubarrays(self, arr: list[int]) -> int:
        counts = [1, 0]
        parity = answer = 0
        for value in arr:
            parity ^= value & 1
            answer = (answer + counts[1 - parity]) % 1_000_000_007
            counts[parity] += 1
        return answer


class SuffixDPSolution:
    """Approach: Odd and even suffix dynamic programming
    Time: O(n)
    Space: O(1)
    """

    def numOfSubarrays(self, arr: list[int]) -> int:
        even = odd = answer = 0
        for value in arr:
            if value & 1:
                even, odd = odd, even + 1
            else:
                even += 1
            answer = (answer + odd) % 1_000_000_007
        return answer
