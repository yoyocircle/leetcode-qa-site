"""
## Task

Decide whether indices i < j < k exist with nums[i] < nums[k] < nums[j]. All inequalities are
strict.

## Hints

1. Scan backward to maintain candidates for the middle-height value.
2. A prefix minimum can represent the first value.

## Approach

### Reverse monotonic stack

Scan from right to left with a decreasing stack and the largest confirmed third value. A larger
incoming value pops possible third values; any later smaller incoming value completes the
pattern.

### Prefix minima with sorted suffix

Try each middle index using the minimum prefix value and a sorted multiset of later values.
Binary-search for a suffix value strictly between the two. List removals make this an
educational baseline that may time out.

## Why it works

### Reverse monotonic stack

Every saved third value has a larger second value earlier than it in the processed suffix. If
the current value is smaller, the index and value orders both hold. Popping records the best
third value without losing any future witness.

### Prefix minima with sorted suffix

For a chosen middle index, a witness exists exactly when a later value is greater than the
smallest preceding value and smaller than the middle value. Lower bound finds the smallest
eligible later value.

## Walkthrough

[3,1,4,2] contains values 1,4,2 at indices 1,2,3. [1,2,3,4] has no such pattern.

## Cost and pitfalls

Reverse monotonic stack: O(n) time; O(n) space.

Prefix minima with sorted suffix: O(n squared) time; O(n) space.

Inputs are unchanged. Equality cannot satisfy either strict inequality. The stack method handles
large negative values without a guessed numeric sentinel.
"""

from bisect import bisect_left, bisect_right


class Solution:
    """Approach: Reverse monotonic stack
    Time: O(n)
    Space: O(n)
    """

    def find132pattern(self, nums: list[int]) -> bool:
        stack = []
        third = float("-inf")
        for value in reversed(nums):
            if value < third:
                return True
            while stack and stack[-1] < value:
                third = stack.pop()
            stack.append(value)
        return False


class SortedSuffixSolution:
    """Approach: Prefix minima with sorted suffix
    Time: O(n squared)
    Space: O(n)
    """

    def find132pattern(self, nums: list[int]) -> bool:
        if len(nums) < 3:
            return False
        suffix = sorted(nums[1:])
        smallest = nums[0]
        for j in range(1, len(nums) - 1):
            suffix.pop(bisect_left(suffix, nums[j]))
            index = bisect_right(suffix, smallest)
            if index < len(suffix) and suffix[index] < nums[j]:
                return True
            smallest = min(smallest, nums[j])
        return False
