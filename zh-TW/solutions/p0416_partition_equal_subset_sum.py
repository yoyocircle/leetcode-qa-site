"""## Task

Decide whether positive integers can be divided into two subsets of equal sum.

## Hints

1. Only a subset summing to half the total is needed.
2. One integer can store reachability bits for all possible sums.

## Approach

### Bitset subset reachability

Bit k indicates an achievable sum k. Shift by the next value to add it to every previous
subset, OR with skipped subsets, and mask above target.

### Explicit set of achievable sums

Store reachable sums as set elements and build a separate set of new sums per value before
merging.

## Why it works

### Bitset subset reachability

The union partitions subsets into those taking or skipping the current value. A shift reads
the old integer, so each input position is used once.

### Explicit set of achievable sums

A separate collection prevents repeatedly consuming the same position. Positive inputs
justify discarding sums above target, which cannot decrease later.

## Walkthrough

For [1,5,11,5], sum 22 permits target 11, reached by the single 11.

## Cost and pitfalls

Bitset subset reachability: O(n*T/w) machine-word work time; O(T/w) machine words space.
Explicit set of achievable sums: O(n*T) expected time; O(T) space.

T is half the total and w the integer machine-word width. Python big-int shifts process
multiple words; they are not O(1). Inputs remain unchanged. The set representation may use
far more memory.
"""


class Solution:
    """Approach: Bitset subset reachability
    Time: O(n*T/w) machine-word work
    Space: O(T/w) machine words
    """

    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        bits = 1
        mask = (1 << (target + 1)) - 1
        for value in nums:
            bits = (bits | (bits << value)) & mask
        return bool(bits & (1 << target))


class SetSolution:
    """Approach: Explicit set of achievable sums
    Time: O(n*T) expected
    Space: O(T)
    """

    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        reachable = {0}
        for value in nums:
            following = {previous + value for previous in reachable if previous + value <= target}
            reachable.update(following)
        return target in reachable
