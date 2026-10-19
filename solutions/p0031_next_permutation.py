"""
## Task

Rearrange nums in place into its next lexicographically larger permutation. If none exists,
rearrange into ascending order. Return None.

## Hints

1. Find the rightmost position that can increase.
2. After increasing that position, minimize the remaining suffix.

## Approach

### Pivot swap and suffix reversal

Find the rightmost ascent, swap its left value with the rightmost larger suffix value, and
reverse the nonincreasing suffix.

### Pivot swap and suffix sorting

Find the same pivot, scan the suffix for its smallest larger value, and sort the suffix. This
simpler baseline misses the required constant-extra-space target.

## Why it works

### Pivot swap and suffix reversal

Changing the latest possible position makes the smallest lexicographic increase. The chosen
successor is the smallest larger suffix value; reversing the descending suffix then gives its
minimum order.

### Pivot swap and suffix sorting

The first different position must be the rightmost pivot that can increase. Choosing its
smallest greater replacement and sorting the remainder minimizes all later positions.

## Walkthrough

[1,3,2] has pivot 1 at index 0. Swap it with 2, then order the suffix to obtain [2,1,3]. A
descending array wraps to ascending.

## Cost and pitfalls

Pivot swap and suffix reversal: O(n) time; O(1) space.

Pivot swap and suffix sorting: O(n log n) time; O(n) space.

Both methods mutate the original list and retain its identity. Equal values require strict
comparison when choosing a successor.
"""


class Solution:
    """Approach: Pivot swap and suffix reversal
    Time: O(n)
    Space: O(1)
    """

    def nextPermutation(self, nums: list[int]) -> None:
        pivot = len(nums) - 2
        while pivot >= 0 and nums[pivot] >= nums[pivot + 1]:
            pivot -= 1
        if pivot >= 0:
            successor = len(nums) - 1
            while nums[successor] <= nums[pivot]:
                successor -= 1
            nums[pivot], nums[successor] = nums[successor], nums[pivot]
        left, right = pivot + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


class SortingSolution:
    """Approach: Pivot swap and suffix sorting
    Time: O(n log n)
    Space: O(n)
    """

    def nextPermutation(self, nums: list[int]) -> None:
        pivot = len(nums) - 2
        while pivot >= 0 and nums[pivot] >= nums[pivot + 1]:
            pivot -= 1
        if pivot < 0:
            nums.sort()
            return
        successor = min(
            (i for i in range(pivot + 1, len(nums)) if nums[i] > nums[pivot]), key=nums.__getitem__
        )
        nums[pivot], nums[successor] = nums[successor], nums[pivot]
        nums[pivot + 1 :] = sorted(nums[pivot + 1 :])
