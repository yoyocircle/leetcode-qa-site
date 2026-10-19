"""
## Task

Choose three distinct positions whose values have a sum closest to target.
Return that sum. The problem promises a unique closest answer.

## Hints

1. Reuse the sorted two-pointer search from 3Sum.
2. Update the best distance before discarding an endpoint.

## Approach

### Sort with two pointers

Sort a copy, fix each first value, and scan the remaining suffix from both ends.
Record any closer sum. Move left for a sum below target and right for a sum
above target. An exact match is immediately optimal.

### Binary-search nearest third value

Sort a copy, fix the first two indices, and inspect the lower-bound neighbor and predecessor for
the third value. This is slower than two pointers but demonstrates nearest-value binary search.

## Why it works

### Sort with two pointers

When the sum is below target, all smaller right choices with the same left
endpoint are no closer than the sum just examined. Symmetrically, when it is
above target, all larger left choices with the same right endpoint are no closer.
The eliminated candidates cannot improve the recorded result.

### Binary-search nearest third value

For a fixed pair, the absolute error is minimized by the third value closest to the remaining
target. The lower-bound neighbor and predecessor cover both sides of that target.

## Walkthrough

For [-3, 1, 4, 7] and target 5, anchor -3 first gives sum 5 from (-3,1,7).
Its distance is zero, so return 5 without further searching.

## Cost and pitfalls

Default approach (Sort with two pointers):

O(n squared) time and O(n) auxiliary space for the sorted copy. Input is unchanged.
Initialize the best sum from three actual values. Compare absolute distances,
not raw sums, and return the sum rather than its distance from target.

Sort with two pointers: O(n squared) time; O(n) space.
Binary-search nearest third value: O(n squared log n) time; O(n) space. Sort a copy, fix the
first two indices, and inspect the lower-bound neighbor and predecessor for the third value.
This is slower than two pointers but demonstrates nearest-value binary search.
"""


class Solution:
    """Approach: Sort with two pointers
    Time: O(n squared)
    Space: O(n)
    """

    def threeSumClosest(self, nums: list[int], target: int) -> int:
        values = sorted(nums)
        best = sum(values[:3])
        for i in range(len(values) - 2):
            left, right = i + 1, len(values) - 1
            while left < right:
                total = values[i] + values[left] + values[right]
                if abs(total - target) < abs(best - target):
                    best = total
                if total == target:
                    return total
                if total < target:
                    left += 1
                else:
                    right -= 1
        return best


class BinarySearchSolution:
    """Approach: Binary-search nearest third value
    Time: O(n squared log n)
    Space: O(n)
    """

    def threeSumClosest(self, nums: list[int], target: int) -> int:
        values = sorted(nums)
        best = sum(values[:3])
        for i in range(len(values) - 2):
            for j in range(i + 1, len(values) - 1):
                left, right = j + 1, len(values)
                wanted = target - values[i] - values[j]
                while left < right:
                    middle = (left + right) // 2
                    if values[middle] < wanted:
                        left = middle + 1
                    else:
                        right = middle
                for index in (left - 1, left):
                    if j < index < len(values):
                        total = values[i] + values[j] + values[index]
                        if abs(total - target) < abs(best - target):
                            best = total
        return best
