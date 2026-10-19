"""## Task

Find the largest sum of a nonempty contiguous subarray.

## Hints

1. Separate the best sum ending here from the best sum anywhere.
2. A crossing optimum can also join a left suffix and a right prefix.

## Approach

### Kadane ending-here states

Track the best nonempty sum ending at each position. Extend its predecessor or restart at
the current value; retain the greatest ending sum.

### Divide and conquer across a midpoint

Divide index ranges without slicing. Compare a wholly left segment, wholly right segment,
and the best crossing suffix-plus-prefix.

## Why it works

### Kadane ending-here states

Every segment ending here either begins here or extends a segment ending one step earlier.
These exhaustive choices establish the recurrence and their maximum over endpoints is the
answer.

### Divide and conquer across a midpoint

Every segment lies in exactly one side or crosses the midpoint. Independent best suffix and
prefix give the best crossing sum, and recursion solves the other two cases.

## Walkthrough

For [-3,4,-1,2,-5], the segment [4,-1,2] has sum 5.

## Cost and pitfalls

Kadane ending-here states: O(n) time; O(1) space.
Divide and conquer across a midpoint: O(n log n) time; O(log n) space.

Inputs are unchanged. Initializing the answer to zero incorrectly allows an empty segment
for all-negative input. Divide-and-conquer depth is logarithmic, but Kadane is faster.
"""


class Solution:
    """Approach: Kadane ending-here states
    Time: O(n)
    Space: O(1)
    """

    def maxSubArray(self, nums: list[int]) -> int:
        ending = answer = nums[0]
        for index in range(1, len(nums)):
            ending = max(nums[index], ending + nums[index])
            answer = max(answer, ending)
        return answer


class DivideSolution:
    """Approach: Divide and conquer across a midpoint
    Time: O(n log n)
    Space: O(log n)
    """

    def maxSubArray(self, nums: list[int]) -> int:
        def solve(left, right):
            if right - left == 1:
                return nums[left]
            middle = (left + right) // 2
            left_sum = right_sum = -float("inf")
            total = 0
            for index in range(middle - 1, left - 1, -1):
                total += nums[index]
                left_sum = max(left_sum, total)
            total = 0
            for index in range(middle, right):
                total += nums[index]
                right_sum = max(right_sum, total)
            return max(solve(left, middle), solve(middle, right), left_sum + right_sum)

        return solve(0, len(nums))
