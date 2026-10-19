"""
## Task

Count nonempty contiguous subarrays of a binary array whose sum equals goal.

## Hints

1. Equal-prefix differences identify target sums.
2. Exactly goal can also be counted as at most goal minus at most goal-1.

## Approach

### Prefix-sum frequency map

Count earlier prefix sums. Before inserting the current prefix, add how many earlier prefixes
equal current-goal.

### Difference of bounded-sum windows

Run a shrinking nonnegative-sum window for each of the two bounds and subtract their counts.
Each endpoint contributes its number of valid starting positions.

## Why it works

### Prefix-sum frequency map

Each earlier matching prefix defines exactly one nonempty subarray ending here. Recording after
querying excludes an empty subarray when goal is zero.

### Difference of bounded-sum windows

Nonnegative values make all suffixes of a valid window valid. Thus each helper counts exactly
the subarrays at most its bound, and subtraction leaves only sum goal.

## Walkthrough

[1,0,1,0,1], goal=2 has four qualifying windows. For [0,0] and goal=0, all three nonempty
windows qualify.

## Cost and pitfalls

Prefix-sum frequency map: O(n) expected time; O(n) space.

Difference of bounded-sum windows: O(n) time; O(1) space.

Inputs are unchanged. The window method relies on nonnegative entries. The negative-bound helper
must return zero so goal=0 works.
"""


class Solution:
    """Approach: Prefix-sum frequency map
    Time: O(n) expected
    Space: O(n)
    """

    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:
        counts = {0: 1}
        prefix = answer = 0
        for value in nums:
            prefix += value
            answer += counts.get(prefix - goal, 0)
            counts[prefix] = counts.get(prefix, 0) + 1
        return answer


class WindowSolution:
    """Approach: Difference of bounded-sum windows
    Time: O(n)
    Space: O(1)
    """

    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:
        def at_most(bound):
            if bound < 0:
                return 0
            left = total = answer = 0
            for right, value in enumerate(nums):
                total += value
                while total > bound:
                    total -= nums[left]
                    left += 1
                answer += right - left + 1
            return answer

        return at_most(goal) - at_most(goal - 1)
