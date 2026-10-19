"""
## Task

Count nonempty contiguous subarrays whose sum equals k. Values may be negative,
so a window's sum does not change monotonically when its boundaries move.

## Hints

1. Express a subarray sum as the difference between two prefix sums.
2. Do you need the earliest matching prefix or the number of matching prefixes?

## Approach

### Online prefix frequencies

The quadratic baseline checks all start/end pairs. Maintain the running prefix
sum and a frequency map of earlier sums. If the current sum is p, every earlier
prefix p-k contributes one valid subarray. Query its frequency, then record p.

### Enumerate start positions

Fix each start and extend a running sum through every end. This educational baseline may time
out on the largest arrays; it makes the subarray definition explicit.

## Why it works

### Online prefix frequencies

A subarray ending here sums to k exactly when its preceding prefix equals p-k.
Each valid start is counted once at its ending position. Seeding prefix 0 with
frequency 1 represents the boundary before the array.

### Enumerate start positions

Every nonempty subarray has one unique start and end. The nested loops visit it once and
maintain its exact sum, including negative numbers.

## Walkthrough

For [2, -2, 2] and k=2, running sums are 2, 0, 2. They contribute 1, 0, and
2 matches respectively, for a total of 3.

## Cost and pitfalls

Default approach (Online prefix frequencies):

Expected O(n) time and O(n) space; input is unchanged. Record the current prefix
after counting, otherwise k=0 includes an empty subarray. Store frequencies,
not just membership. Ordinary positive-sum sliding windows do not apply.

Online prefix frequencies: O(n) expected time; O(n) space.
Enumerate start positions: O(n squared) time; O(1) space. Fix each start and extend a running
sum through every end. This educational baseline may time out on the largest arrays; it makes
the subarray definition explicit.
"""


class Solution:
    """Approach: Online prefix frequencies
    Time: O(n) expected
    Space: O(n)
    """

    def subarraySum(self, nums: list[int], k: int) -> int:
        frequencies = {0: 1}
        prefix = result = 0
        for number in nums:
            prefix += number
            result += frequencies.get(prefix - k, 0)
            frequencies[prefix] = frequencies.get(prefix, 0) + 1
        return result


class EnumerationSolution:
    """Approach: Enumerate start positions
    Time: O(n squared)
    Space: O(1)
    """

    def subarraySum(self, nums: list[int], k: int) -> int:
        answer = 0
        for start in range(len(nums)):
            total = 0
            for end in range(start, len(nums)):
                total += nums[end]
                answer += total == k
        return answer
