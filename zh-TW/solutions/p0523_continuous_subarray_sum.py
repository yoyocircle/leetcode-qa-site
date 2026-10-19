"""
## Task

Decide whether a nonempty integer array has a subarray of length at least two whose sum is a
multiple of positive k.

## Hints

1. Two equal prefix remainders enclose a divisible sum.
2. Keep the earliest index to maximize the enclosed length.

## Approach

### Earliest index per remainder

Map each prefix remainder to its first index. Seed remainder zero before the array and require a
gap of at least two.

### Delayed prefix-remainder set

Keep only prefix remainders at least two positions behind the current prefix. Delay inserting
the immediately preceding prefix by one iteration.

## Why it works

### Earliest index per remainder

Equal remainders mean the difference of prefix sums is divisible by k. The earliest matching
index gives the longest available gap, so rejecting shorter matches loses no valid answer.

### Delayed prefix-remainder set

At prefix position j, the set contains exactly eligible prefix positions i <= j-2. A matching
remainder therefore proves divisibility and the minimum length together.

## Walkthrough

For [23,2,4,6,7], k=6, the prefixes after 23 and after 4 both have remainder 5. Their two-
element difference [2,4] qualifies.

## Cost and pitfalls

Earliest index per remainder: O(n) expected time; O(min(n,k)) space.

Delayed prefix-remainder set: O(n) expected time; O(min(n,k)) space.

Inputs are unchanged. k is positive under the problem contract. A single zero is too short; two
zeros qualify for any positive k.
"""


class Solution:
    """Approach: Earliest index per remainder
    Time: O(n) expected
    Space: O(min(n,k))
    """

    def checkSubarraySum(self, nums: list[int], k: int) -> bool:
        first = {0: -1}
        remainder = 0
        for i, value in enumerate(nums):
            remainder = (remainder + value) % k
            if remainder in first:
                if i - first[remainder] >= 2:
                    return True
            else:
                first[remainder] = i
        return False


class DelayedSetSolution:
    """Approach: Delayed prefix-remainder set
    Time: O(n) expected
    Space: O(min(n,k))
    """

    def checkSubarraySum(self, nums: list[int], k: int) -> bool:
        eligible = set()
        previous = current = 0
        for value in nums:
            current = (current + value) % k
            if current in eligible:
                return True
            eligible.add(previous)
            previous = current
        return False
