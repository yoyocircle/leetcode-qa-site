"""
## Task

Every signed 32-bit integer appears twice except two distinct values appearing once. Return the
two unique values in any order, in linear time with constant auxiliary storage.

## Hints

1. XOR cancels paired values.
2. One set bit in the combined XOR separates the two unique values.

## Approach

### XOR partition by distinguishing bit

XOR all values to obtain a XOR b. Isolate one set bit and XOR each side of that bit partition
independently.

### Frequency map baseline

Count complete values and retain those with frequency one. This educational baseline misses the
required constant-space bound.

## Why it works

### XOR partition by distinguishing bit

The chosen bit differs between the unique values, so they enter different groups. Every
duplicated value stays with its equal partner and cancels; each group leaves one unique value.

### Frequency map baseline

The input multiplicity contract says exactly two frequency entries equal one, so selecting those
keys returns exactly the desired values.

## Walkthrough

[1,2,1,3,2,5] XORs to 3 XOR 5; its low distinguishing bit separates the survivors 3 and 5.

## Cost and pitfalls

XOR partition by distinguishing bit: O(n) time; O(1) space.

Frequency map baseline: O(n) expected time; O(n) space.

Inputs are unchanged. The combined XOR is nonzero because the two unique values differ. Python's
low-bit expression also works when the combined XOR is negative.
"""

from collections import Counter


class Solution:
    """Approach: XOR partition by distinguishing bit
    Time: O(n)
    Space: O(1)
    """

    def singleNumber(self, nums: list[int]) -> list[int]:
        combined = 0
        for value in nums:
            combined ^= value
        bit = combined & -combined
        first = second = 0
        for value in nums:
            if value & bit:
                first ^= value
            else:
                second ^= value
        return [first, second]


class FrequencySolution:
    """Approach: Frequency map baseline
    Time: O(n) expected
    Space: O(n)
    """

    def singleNumber(self, nums: list[int]) -> list[int]:
        counts = Counter(nums)
        return [value for value, count in counts.items() if count == 1]
