"""
## Task

In a sorted array, locate the two distinct positions whose values sum to target.
Exactly one solution exists. Return 1-based indices using constant extra space.

## Hints

1. Start with the smallest and largest available values.
2. When their sum is too small, which endpoint cannot belong to a solution?

## Approach

### Inward two pointers

Place pointers at both ends. Increase the left pointer when the sum is too small;
decrease the right pointer when it is too large. Stop when the sum matches.

### Binary search complements

For each left index, binary-search its complement strictly to the right. This keeps constant
auxiliary space but repeats logarithmic searches.

## Why it works

### Inward two pointers

If the sum is too small, pairing the left value with any smaller right value
cannot help. If it is too large, pairing the right value with any larger left
value cannot help. Each discarded endpoint is therefore safe to exclude.

### Binary search complements

The unique promised pair has a smaller index i; when i is examined, binary search finds its
complement among later values. Searching only later positions forbids reusing one element.

## Walkthrough

For [1, 4, 6, 9] and target 10, the outside pair already matches. Return [1, 4].
For target 7, move the right endpoint from 9 to 6, then return [1, 3].

## Cost and pitfalls

Default approach (Inward two pointers):

O(n) time and O(1) auxiliary space; inputs are unchanged. Return indices, not
values, and add 1 to both. Keep left strictly below right so an element is never
used twice. Equal values at different positions are allowed.

Inward two pointers: O(n) time; O(1) space.
Binary search complements: O(n log n) time; O(1) space. For each left index, binary-search its
complement strictly to the right. This keeps constant auxiliary space but repeats logarithmic
searches.
"""


class Solution:
    """Approach: Inward two pointers
    Time: O(n)
    Space: O(1)
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1
        raise ValueError("The problem guarantees a solution")


class BinarySearchSolution:
    """Approach: Binary search complements
    Time: O(n log n)
    Space: O(1)
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        for i, value in enumerate(numbers):
            left, right = i + 1, len(numbers)
            while left < right:
                middle = (left + right) // 2
                if numbers[middle] < target - value:
                    left = middle + 1
                else:
                    right = middle
            if left < len(numbers) and numbers[left] == target - value:
                return [i + 1, left + 1]
        raise ValueError("The problem guarantees a solution")
