"""
## Task

Sort an array containing only 0, 1, and 2 in place without calling a sorting library. Return
None.

## Hints

1. Maintain separate completed regions for zeros and twos.
2. Counting the three values is a second constant-space option.

## Approach

### Dutch national flag partition

Maintain zero, scan, and two boundaries. Move zeros left, twos right, and advance past ones.

### Count then overwrite

Count each of the three colors, then overwrite the list in color order. This takes two passes
but has simpler state.

## Why it works

### Dutch national flag partition

Indices before zero are 0, between zero and scan are 1, and after two are 2. Every swap
preserves these regions and reduces the unclassified region.

### Count then overwrite

The frequency counts preserve the input multiset. Writing each color its exact count in
increasing order yields the unique sorted array.

## Walkthrough

[2,0,2,1,1,0] becomes [0,0,1,1,2,2]. After swapping a 2 with the right boundary, inspect the
incoming value before moving scan.

## Cost and pitfalls

Dutch national flag partition: O(n) time; O(1) space.

Count then overwrite: O(n) time; O(1) space.

Both methods mutate the original list with constant extra space. The counting method uses a
fixed three-element array, not storage proportional to n.
"""


class Solution:
    """Approach: Dutch national flag partition
    Time: O(n)
    Space: O(1)
    """

    def sortColors(self, nums: list[int]) -> None:
        zero = scan = 0
        two = len(nums) - 1
        while scan <= two:
            if nums[scan] == 0:
                nums[zero], nums[scan] = nums[scan], nums[zero]
                zero += 1
                scan += 1
            elif nums[scan] == 2:
                nums[scan], nums[two] = nums[two], nums[scan]
                two -= 1
            else:
                scan += 1


class CountingSolution:
    """Approach: Count then overwrite
    Time: O(n)
    Space: O(1)
    """

    def sortColors(self, nums: list[int]) -> None:
        counts = [0, 0, 0]
        for value in nums:
            counts[value] += 1
        index = 0
        for value, count in enumerate(counts):
            for _ in range(count):
                nums[index] = value
                index += 1
