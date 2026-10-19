"""## Task

Return the longest arithmetic subsequence length, with selected elements kept in input order.

## Hints

1. A subsequence endpoint needs its common difference as part of its state.
2. The official value bound also permits scanning all possible differences.

## Approach

### Endpoint and difference dictionaries

For every earlier endpoint, extend its state for the required difference, or seed a
length-two pair when that state is absent.

### Scan each feasible difference by ending value

For one fixed difference, scan input order and retain the longest chain ending at each
value. Repeat over the bounded difference interval.

## Why it works

### Endpoint and difference dictionaries

Every arithmetic subsequence has a final predecessor and a fixed difference. Trying all
predecessors covers its possible final extension, and the maximum retains the best state for
future extensions.

### Scan each feasible difference by ending value

For a fixed difference, a value can follow only value-difference, so its best previous chain
suffices. Every valid common difference lies between negative and positive value span and is
tested.

## Walkthrough

For [3,6,9,12], common difference 3 gives length 4; repeated values use difference zero.

## Cost and pitfalls

Endpoint and difference dictionaries: O(n^2) expected time; O(n^2) space.
Scan each feasible difference by ending value: O(n*D) expected time; O(U) space.

D is twice the value span plus one, U the number of distinct input values. Official values
lie in 0..500, so scanning differences is viable. Both preserve nums; the zero-difference
update must read the preceding value state before writing it.
"""


class Solution:
    """Approach: Endpoint and difference dictionaries
    Time: O(n^2) expected
    Space: O(n^2)
    """

    def longestArithSeqLength(self, nums: list[int]) -> int:
        ending = [{} for _ in nums]
        answer = 2
        for i, value in enumerate(nums):
            for j in range(i):
                difference = value - nums[j]
                length = ending[j].get(difference, 1) + 1
                ending[i][difference] = max(ending[i].get(difference, 0), length)
                answer = max(answer, length)
        return answer


class DifferenceSolution:
    """Approach: Scan each feasible difference by ending value
    Time: O(n*D) expected
    Space: O(U)
    """

    def longestArithSeqLength(self, nums: list[int]) -> int:
        span = max(nums) - min(nums)
        answer = 1
        for difference in range(-span, span + 1):
            best = {}
            for value in nums:
                length = best.get(value - difference, 0) + 1
                best[value] = max(best.get(value, 0), length)
                answer = max(answer, length)
        return answer
