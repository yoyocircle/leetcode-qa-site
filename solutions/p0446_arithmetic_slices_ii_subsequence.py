"""## Task

Count index-distinct arithmetic subsequences of length at least three; selected positions
need not be contiguous.

## Hints

1. A pair has a difference but is not yet a counted answer.
2. Every longer subsequence has a unique final pair of positions.

## Approach

### Endpoint maps keyed by common difference

Store counts of length-at-least-two subsequences by endpoint and difference. A new pair
seeds one state; only extensions of existing states contribute to the requested answer.

### Explicit final-pair recurrence

Let pairs[j][i] count length-at-least-three subsequences with final positions j,i. Enumerate
earlier positions k with value 2*nums[j]-nums[i], adding the new triple and every prior
subsequence ending k,j.

## Why it works

### Endpoint maps keyed by common difference

Every arithmetic subsequence of length at least three arises once by removing its final
position. The remaining state has the same difference, and counting only extensions excludes
bare pairs.

### Explicit final-pair recurrence

Each counted sequence has one unique penultimate pair. Its third-last position must have the
derived value, and it is either the triple itself or an extension of a longer sequence
counted at that earlier pair.

## Walkthrough

For [2,4,6,8], [2,4,6], [4,6,8], and [2,4,6,8] give 3.

## Cost and pitfalls

Endpoint maps keyed by common difference: O(n^2) expected time; O(n^2) space.
Explicit final-pair recurrence: O(n^3) worst case time; O(n^2) space.

Both preserve nums and support negative differences and repeated values. The explicit-pair
baseline can time out near n=1000, especially on equal values; use the quadratic default.
Dictionaries use expected constant-time lookups.
"""


class Solution:
    """Approach: Endpoint maps keyed by common difference
    Time: O(n^2) expected
    Space: O(n^2)
    """

    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        ending = [{} for _ in nums]
        answer = 0
        for end, value in enumerate(nums):
            for previous in range(end):
                difference = value - nums[previous]
                extensions = ending[previous].get(difference, 0)
                answer += extensions
                ending[end][difference] = ending[end].get(difference, 0) + extensions + 1
        return answer


class PairTableSolution:
    """Approach: Explicit final-pair recurrence
    Time: O(n^3) worst case
    Space: O(n^2)
    """

    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        positions = {}
        for index, value in enumerate(nums):
            positions.setdefault(value, []).append(index)
        pairs = [[0] * len(nums) for _ in nums]
        answer = 0
        for end in range(len(nums)):
            for previous in range(end):
                required = 2 * nums[previous] - nums[end]
                for earlier in positions.get(required, ()):
                    if earlier >= previous:
                        break
                    pairs[previous][end] += 1 + pairs[earlier][previous]
                answer += pairs[previous][end]
        return answer
