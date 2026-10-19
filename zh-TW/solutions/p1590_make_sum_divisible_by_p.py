"""
## Task

Remove the shortest contiguous subarray, possibly empty, so the remaining positive-integer array
sum is divisible by p. Removing the entire array is forbidden; return -1 if necessary.

## Hints

1. The removed sum must have remainder total modulo p.
2. For a fixed right endpoint, the latest matching prefix gives the shortest removal.

## Approach

### Latest index per prefix remainder

Track the latest index for each prefix remainder and query current-total_remainder before
updating it.

### Batch prefix positions and predecessor search

Store all prefix positions grouped by remainder. For each end position, binary-search the
greatest eligible earlier position in the required group.

## Why it works

### Latest index per prefix remainder

A removal works exactly when its endpoint prefix difference has the required remainder. Among
earlier equal remainders, the latest index minimizes length without affecting future
eligibility.

### Batch prefix positions and predecessor search

Grouping preserves exactly the remainder equality needed for divisibility. A predecessor search
enforces earlier index order and chooses its largest member, hence the shortest valid removal
for that end.

## Walkthrough

[3,1,4,2], p=6 has total remainder 4. Removing the singleton [4] makes the remaining sum 6, so
return 1.

## Cost and pitfalls

Latest index per prefix remainder: O(n) expected time; O(n) space.

Batch prefix positions and predecessor search: O(n log n) time; O(n) space.

Inputs are unchanged. Both methods reject a best length equal to n. Normalize a negative
remainder difference with modulo before lookup.
"""

from bisect import bisect_left


class Solution:
    """Approach: Latest index per prefix remainder
    Time: O(n) expected
    Space: O(n)
    """

    def minSubarray(self, nums: list[int], p: int) -> int:
        required = sum(nums) % p
        if required == 0:
            return 0
        latest = {0: -1}
        remainder = 0
        best = len(nums)
        for i, value in enumerate(nums):
            remainder = (remainder + value) % p
            wanted = (remainder - required) % p
            if wanted in latest:
                best = min(best, i - latest[wanted])
            latest[remainder] = i
        return best if best < len(nums) else -1


class PositionSearchSolution:
    """Approach: Batch prefix positions and predecessor search
    Time: O(n log n)
    Space: O(n)
    """

    def minSubarray(self, nums: list[int], p: int) -> int:
        required = sum(nums) % p
        if required == 0:
            return 0
        prefix = [0]
        positions = {0: [0]}
        for i, value in enumerate(nums, 1):
            prefix.append((prefix[-1] + value) % p)
            positions.setdefault(prefix[-1], []).append(i)
        best = len(nums)
        for end in range(1, len(prefix)):
            candidates = positions.get((prefix[end] - required) % p, [])
            index = bisect_left(candidates, end) - 1
            if index >= 0:
                best = min(best, end - candidates[index])
        return best if best < len(nums) else -1
