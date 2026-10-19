"""
## Task

Return unique value triplets that sum to zero, using three distinct array
positions. The order of triplets does not matter.

## Hints

1. Fix one value and solve a sorted two-sum problem on the remaining suffix.
2. Which duplicate choices would generate an already returned triplet?

## Approach

### Sort with two pointers

Sort a copy. For each distinct first value, move two pointers over its suffix.
After finding a zero sum, advance both pointers and skip repeated endpoint
values. This improves cubic enumeration to quadratic scanning.

### Per-anchor complement sets

Fix one anchor, then find complement pairs using a hash set of already-seen later values.
Canonical sorted triplet tuples remove repeated answers without sorting the input.

## Why it works

### Sort with two pointers

For a fixed first value, sorted two-pointer elimination cannot skip a valid
pair. Every triplet has a smallest sorted position that is considered as the
anchor. Skipping equal anchors and equal successful endpoints removes duplicate
value triplets without removing a distinct answer.

### Per-anchor complement sets

For each anchor, a later value completes a triplet exactly when its required complement was seen
at a distinct earlier later index. Every index triple is considered at its largest later index.

## Walkthrough

For [-2, 0, 1, 1, 2], anchor -2 finds endpoint pairs (0,2) and (1,1).
The answer is [[-2,0,2], [-2,1,1]].

## Cost and pitfalls

Default approach (Sort with two pointers):

O(n squared) time, O(n) auxiliary sorting space, plus output storage. The original
array is unchanged because sorted makes a copy. Start left after the anchor.
Skipping every repeated value before evaluating pairs can lose valid repeated-value
triplets such as [-2,1,1].

Sort with two pointers: O(n squared) time; O(n) plus output space.
Per-anchor complement sets: O(n squared) expected time; O(n) plus output space. Fix one anchor,
then find complement pairs using a hash set of already-seen later values. Canonical sorted
triplet tuples remove repeated answers without sorting the input.
"""


class Solution:
    """Approach: Sort with two pointers
    Time: O(n squared)
    Space: O(n) plus output
    """

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        values = sorted(nums)
        result = []
        for i in range(len(values) - 2):
            if i and values[i] == values[i - 1]:
                continue
            left, right = i + 1, len(values) - 1
            while left < right:
                total = values[i] + values[left] + values[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([values[i], values[left], values[right]])
                    left += 1
                    right -= 1
                    while left < right and values[left] == values[left - 1]:
                        left += 1
                    while left < right and values[right] == values[right + 1]:
                        right -= 1
        return result


class HashingSolution:
    """Approach: Per-anchor complement sets
    Time: O(n squared) expected
    Space: O(n) plus output
    """

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        answers = set()
        for i, anchor in enumerate(nums):
            seen = set()
            for j in range(i + 1, len(nums)):
                value = nums[j]
                complement = -anchor - value
                if complement in seen:
                    answers.add(tuple(sorted((anchor, value, complement))))
                seen.add(value)
        return [list(values) for values in sorted(answers)]
