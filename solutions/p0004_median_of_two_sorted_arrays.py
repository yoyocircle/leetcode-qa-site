"""
## Task

Return the median of two sorted arrays without merging them. One array may be
empty, but their combined length is positive.

## Hints

1. Partition both arrays so the left side holds half the combined elements.
2. What inequalities make every left element no larger than every right element?

## Approach

### Binary-search partition

Binary search a cut in the shorter array; the required left-side size determines
the other cut. Use infinite sentinels at empty sides. A valid partition satisfies
left_a<=right_b and left_b<=right_a. Move the cut left if left_a is too large,
otherwise right.

### Merge until middle

Advance two sorted-array pointers until the middle position, retaining only the last two values.
This educational baseline misses the mandated logarithmic-time bound.

## Why it works

### Binary-search partition

Sortedness reduces cross-partition ordering to those two boundary comparisons.
Moving the cut in the indicated direction fixes its violated inequality.
At a valid partition, the greatest left value is the odd-length median; for an
even length, average it with the smallest right value.

### Merge until middle

Choosing the smaller next head emits the globally sorted order. The last emitted value and its
predecessor at the middle position are exactly the median element or central pair.

## Walkthrough

For [1,4] and [2,3,8], cuts after 1 and after 3 make left=[1,2,3],
right=[4,8]. The median is max(1,3)=3.

## Cost and pitfalls

Default approach (Binary-search partition):

O(log(min(m,n)+1)) time and O(1) space; inputs are unchanged. Search the shorter
array so the derived cut stays valid. Use (m+n+1)//2 for left size. This is a
partition search, not a search for the median's numeric value.

Binary-search partition: O(log(min(m,n)+1)) time; O(1) space.
Merge until middle: O(m+n) time; O(1) space. Advance two sorted-array pointers until the middle
position, retaining only the last two values. This educational baseline misses the mandated
logarithmic-time bound.
"""


class Solution:
    """Approach: Binary-search partition
    Time: O(log(min(m,n)+1))
    Space: O(1)
    """

    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        left, right = 0, m
        while left <= right:
            i = (left + right) // 2
            j = (m + n + 1) // 2 - i
            a_left = nums1[i - 1] if i else float("-inf")
            a_right = nums1[i] if i < m else float("inf")
            b_left = nums2[j - 1] if j else float("-inf")
            b_right = nums2[j] if j < n else float("inf")
            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                right = i - 1
            else:
                left = i + 1
        raise ValueError("Inputs must be sorted")


class MergeSolution:
    """Approach: Merge until middle
    Time: O(m+n)
    Space: O(1)
    """

    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        i = j = 0
        previous = current = 0
        total = len(nums1) + len(nums2)
        for _ in range(total // 2 + 1):
            previous = current
            if j == len(nums2) or (i < len(nums1) and nums1[i] <= nums2[j]):
                current = nums1[i]
                i += 1
            else:
                current = nums2[j]
                j += 1
        return float(current) if total % 2 else (previous + current) / 2
