"""
## Task

Count contiguous nonempty subarrays containing exactly k odd numbers. Values themselves may be
larger than one.

## Hints

1. Replace every value by its parity.
2. For any block of k odd positions, surrounding even runs provide independent boundary choices.

## Approach

### Odd-prefix frequencies

Accumulate the number of odd elements and count earlier odd-prefix values smaller by k.

### Odd-position gap products

List odd positions with sentinels -1 and n. For each consecutive block of k odds, multiply the
available starting and ending boundary counts.

## Why it works

### Odd-prefix frequencies

The difference of odd-prefix counts equals the number of odd elements in the enclosed interval.
Every matching earlier prefix contributes exactly one qualifying interval.

### Odd-position gap products

A qualifying interval contains one unique block of k consecutive odd positions. Its start lies
after the preceding odd and at or before the first selected odd; its end has an independent
symmetric range.

## Walkthrough

[1,1,2,1,1], k=3 permits the first three odds or the last three odds, giving two intervals.

## Cost and pitfalls

Odd-prefix frequencies: O(n) expected time; O(n) space.

Odd-position gap products: O(n) time; O(n) space.

Inputs are unchanged. The promised k is positive. Sentinels let odd blocks touching either array
endpoint use the same gap formula.
"""


class Solution:
    """Approach: Odd-prefix frequencies
    Time: O(n) expected
    Space: O(n)
    """

    def numberOfSubarrays(self, nums: list[int], k: int) -> int:
        counts = {0: 1}
        odd = answer = 0
        for value in nums:
            odd += value & 1
            answer += counts.get(odd - k, 0)
            counts[odd] = counts.get(odd, 0) + 1
        return answer


class GapSolution:
    """Approach: Odd-position gap products
    Time: O(n)
    Space: O(n)
    """

    def numberOfSubarrays(self, nums: list[int], k: int) -> int:
        positions = [-1] + [i for i, value in enumerate(nums) if value & 1] + [len(nums)]
        answer = 0
        for first in range(1, len(positions) - k):
            last = first + k - 1
            answer += (positions[first] - positions[first - 1]) * (
                positions[last + 1] - positions[last]
            )
        return answer
