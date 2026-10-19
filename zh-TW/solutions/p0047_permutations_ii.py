"""## Task

Return every distinct ordering of an integer array that may contain repeated values.

## Hints

1. Equal values are interchangeable, but positions still cannot be reused.
2. Use either a canonical equal-index rule or remaining value counts.

## Approach

### Sorted unused-index search

Sort a copy and track used indices. Skip a duplicate index when its equal predecessor has not
been used in the current path.

### Remaining-frequency search

Count each value and choose only values with a positive remaining count, decrementing and
restoring around recursion.

## Why it works

### Sorted unused-index search

The rule imposes one fixed usage order on equal positions, removing only interchangeable index
permutations. Every distinct value ordering retains one legal choice sequence.

### Remaining-frequency search

The frequency vector exactly describes unused supply. Every distinct next value is tried once,
so each valid full value sequence appears exactly once.

## Walkthrough

For [2,2,5], return [2,2,5], [2,5,2], and [5,2,2]. Swapping the two 2 positions does not create
another answer.

## Cost and pitfalls

Sorted unused-index search: O(n*n!) loose bound time; O(n) auxiliary; O(n*P) output space.
Remaining-frequency search: O(n*n!) loose bound time; O(n) auxiliary; O(n*P) output space.
Input is unchanged. P is the number of distinct permutations. Copies of complete paths count
toward time and output storage. Restore used indices or counts after every recursive branch.
"""

from collections import Counter


class Solution:
    """Approach: Sorted unused-index search
    Time: O(n*n!) loose bound
    Space: O(n) auxiliary; O(n*P) output
    """

    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        values = sorted(nums)
        used = [False] * len(values)
        path, result = [], []

        def visit():
            if len(path) == len(values):
                result.append(path.copy())
                return
            for index, value in enumerate(values):
                if used[index] or (index and value == values[index - 1] and not used[index - 1]):
                    continue
                used[index] = True
                path.append(value)
                visit()
                path.pop()
                used[index] = False

        visit()
        return result


class FrequencySolution:
    """Approach: Remaining-frequency search
    Time: O(n*n!) loose bound
    Space: O(n) auxiliary; O(n*P) output
    """

    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        counts = Counter(nums)
        result, path = [], []

        def visit():
            if len(path) == len(nums):
                result.append(path.copy())
                return
            for value in counts:
                if counts[value]:
                    counts[value] -= 1
                    path.append(value)
                    visit()
                    path.pop()
                    counts[value] += 1

        visit()
        return result
