"""## Task

Count contiguous arithmetic subarrays of length at least three.

## Hints

1. A matching next difference extends all arithmetic suffixes ending one position earlier.
2. A run of d equal adjacent differences contributes d*(d-1)/2 subarrays.

## Approach

### Count arithmetic suffixes ending here

If the last two differences agree, extend the preceding arithmetic suffixes and add the new
length-three suffix. Otherwise reset the suffix count.

### Sum maximal equal-difference runs

Group adjacent differences into maximal constant runs. Add the triangular number of each run
when it ends, then flush the final run.

## Why it works

### Count arithmetic suffixes ending here

Every qualifying slice has a unique ending index. Equal differences extend exactly the
previous valid suffixes and one additional short slice, so summing endpoint counts is exact.

### Sum maximal equal-difference runs

An arithmetic slice corresponds to at least two consecutive differences inside exactly one
maximal run. A run of d differences has (d-1)+(d-2)+...+1 such intervals.

## Walkthrough

For [1,3,5,7], two length-three slices and one length-four slice give 3.

## Cost and pitfalls

Count arithmetic suffixes ending here: O(n) time; O(1) space.
Sum maximal equal-difference runs: O(n) time; O(1) space.

Both preserve nums, handle arrays shorter than three naturally, and allocate no difference
list or slices. Equal values produce difference zero and are valid arithmetic slices.
"""


class Solution:
    """Approach: Count arithmetic suffixes ending here
    Time: O(n)
    Space: O(1)
    """

    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        ending = answer = 0
        for index in range(2, len(nums)):
            ending = (
                ending + 1
                if nums[index] - nums[index - 1] == nums[index - 1] - nums[index - 2]
                else 0
            )
            answer += ending
        return answer


class RunSolution:
    """Approach: Sum maximal equal-difference runs
    Time: O(n)
    Space: O(1)
    """

    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        answer = run = 0
        previous = None
        for index in range(1, len(nums)):
            difference = nums[index] - nums[index - 1]
            if difference != previous:
                answer += run * (run - 1) // 2
                run = 0
            run += 1
            previous = difference
        return answer + run * (run - 1) // 2
