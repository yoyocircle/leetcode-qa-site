"""
## Task

Return unique value quadruplets from four distinct indices whose sum is target. Output order
does not matter.

## Hints

1. Sort a copy and fix two indices before a two-pointer search.
2. A pair-sum table must still ensure that all four indices differ.

## Approach

### Two anchors and two pointers

Skip repeated anchors in sorted order, then move the remaining pair inward and skip equal pair
values after a match.

### Incremental disjoint pair sums

Before examining a third index, add all earlier index pairs. Match these pairs with third/fourth
choices, storing canonical quadruplets in a set. Many equal pair sums can make this educational
baseline time out.

## Why it works

### Two anchors and two pointers

For each fixed anchor pair, increasing the smaller pointer raises the sum and decreasing the
larger pointer lowers it. Every feasible sorted quadruplet is reached; duplicate skips preserve
one representative.

### Incremental disjoint pair sums

Stored pairs end strictly before the current third index, which guarantees disjoint indices.
Every increasing index quadruple is considered once at its third/fourth pair; canonical tuples
remove repeated values.

## Walkthrough

[1,0,-1,0,-2,2] with target 0 yields [-2,-1,1,2], [-2,0,0,2], and [-1,0,0,1].

## Cost and pitfalls

Two anchors and two pointers: O(n cubed) time; O(n) plus output space.

Incremental disjoint pair sums: O(n to the fourth) worst case time; O(n squared) plus output
space.

Inputs are unchanged. Count values through distinct indices; a set of values alone would lose
repeated zeros. The default cubic approach avoids large equal-sum pair cross products.
"""


class Solution:
    """Approach: Two anchors and two pointers
    Time: O(n cubed)
    Space: O(n) plus output
    """

    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        values = sorted(nums)
        answer = []
        for i in range(len(values) - 3):
            if i and values[i] == values[i - 1]:
                continue
            for j in range(i + 1, len(values) - 2):
                if j > i + 1 and values[j] == values[j - 1]:
                    continue
                left, right = j + 1, len(values) - 1
                while left < right:
                    total = values[i] + values[j] + values[left] + values[right]
                    if total < target:
                        left += 1
                    elif total > target:
                        right -= 1
                    else:
                        answer.append([values[i], values[j], values[left], values[right]])
                        a, b = values[left], values[right]
                        while left < right and values[left] == a:
                            left += 1
                        while left < right and values[right] == b:
                            right -= 1
        return answer


class PairSumSolution:
    """Approach: Incremental disjoint pair sums
    Time: O(n to the fourth) worst case
    Space: O(n squared) plus output
    """

    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        pairs = {}
        answer = set()
        for third in range(2, len(nums) - 1):
            second = third - 1
            for first in range(second):
                pairs.setdefault(nums[first] + nums[second], []).append((nums[first], nums[second]))
            for fourth in range(third + 1, len(nums)):
                wanted = target - nums[third] - nums[fourth]
                for a, b in pairs.get(wanted, []):
                    answer.add(tuple(sorted((a, b, nums[third], nums[fourth]))))
        return [list(values) for values in sorted(answer)]
