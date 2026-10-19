"""
## Task

Compact a sorted array in place so each value appears at most twice. Return the retained prefix
length; later entries are unspecified.

## Hints

1. Compare an incoming value with the value two output slots earlier.
2. A run counter offers another direct invariant.

## Approach

### Two-slot output comparison

Write a value if fewer than two outputs exist or it differs from the output two places back.

### Explicit input-run counts

Track the current input run length and copy only its first two entries to the output prefix.

## Why it works

### Two-slot output comparison

Because values arrive sorted, a match two output positions back means the prefix already ends in
two copies of this value. Otherwise adding it cannot create a third copy.

### Explicit input-run counts

Sorted order makes each value occupy one run. Copying min(run length,2) entries from every run
preserves order and exactly enforces the frequency limit.

## Walkthrough

[0,0,1,1,1,1,2,3,3] returns 7 and leaves [0,0,1,1,2,3,3] as the meaningful prefix.

## Cost and pitfalls

Two-slot output comparison: O(n) time; O(1) space.

Explicit input-run counts: O(n) time; O(1) space.

The list is mutated but its identity and length remain unchanged. Do not assert anything about
entries beyond the returned prefix.
"""


class Solution:
    """Approach: Two-slot output comparison
    Time: O(n)
    Space: O(1)
    """

    def removeDuplicates(self, nums: list[int]) -> int:
        write = 0
        for value in nums:
            if write < 2 or value != nums[write - 2]:
                nums[write] = value
                write += 1
        return write


class RunCountSolution:
    """Approach: Explicit input-run counts
    Time: O(n)
    Space: O(1)
    """

    def removeDuplicates(self, nums: list[int]) -> int:
        previous = None
        count = write = 0
        for read in range(len(nums)):
            value = nums[read]
            count = count + 1 if value == previous else 1
            previous = value
            if count <= 2:
                nums[write] = value
                write += 1
        return write
