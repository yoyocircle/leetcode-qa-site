"""
## Task

Return the sum of Hamming distances over every unordered pair of nonnegative integers. Values
are bounded by 10^9.

## Hints

1. Count differing pairs independently at each bit.
2. If c values have a set bit, c*(n-c) unordered pairs differ there.

## Approach

### Per-bit population counts

For each of 30 relevant bits, count set values and multiply by the unset count.

### Direct XOR pair enumeration

XOR each unordered value pair and count its set bits. This educational baseline may time out for
large n.

## Why it works

### Per-bit population counts

Every differing pair at a bit selects one set and one unset value, yielding c*(n-c) pairs
exactly once. Summing independent bit contributions equals total Hamming distance.

### Direct XOR pair enumeration

XOR sets exactly the positions where the pair differs. Each unordered pair is enumerated once,
so summing bit_count gives the specification directly.

## Walkthrough

[4,14,2] has pair distances 2,2,2, totaling 6. The same result comes from counting set/unset
pairs at bits 1,2,3.

## Cost and pitfalls

Per-bit population counts: O(30n) time; O(1) space.

Direct XOR pair enumeration: O(n squared) time; O(1) space.

Inputs are unchanged. The factor is c*(n-c), without dividing by two, since selecting a set side
and an unset side already identifies each unordered pair once.
"""


class Solution:
    """Approach: Per-bit population counts
    Time: O(30n)
    Space: O(1)
    """

    def totalHammingDistance(self, nums: list[int]) -> int:
        answer = 0
        for bit in range(30):
            ones = sum((value >> bit) & 1 for value in nums)
            answer += ones * (len(nums) - ones)
        return answer


class PairSolution:
    """Approach: Direct XOR pair enumeration
    Time: O(n squared)
    Space: O(1)
    """

    def totalHammingDistance(self, nums: list[int]) -> int:
        answer = 0
        for i, value in enumerate(nums):
            for j in range(i + 1, len(nums)):
                answer += (value ^ nums[j]).bit_count()
        return answer
