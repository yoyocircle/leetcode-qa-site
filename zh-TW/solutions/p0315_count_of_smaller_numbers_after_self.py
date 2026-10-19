"""
## Task

For each input index, count later entries strictly smaller than its value. Return one count per
index.

## Hints

1. Process from right to left so the stored values are exactly the suffix.
2. Merge-sort inversions can count smaller right elements in bulk.

## Approach

### Compressed Fenwick frequencies

Compress sorted distinct values into ranks. Scan right to left, querying all smaller ranks
before inserting the current rank.

### Merge-sort indexed inversion counts

Sort (value,original_index) pairs by merge sort. Each right-half element moved ahead of a left-
half element contributes one smaller suffix entry to that left element.

## Why it works

### Compressed Fenwick frequencies

The tree contains precisely the later indices. Its prefix below the current rank counts exactly
smaller later values, and querying before insertion excludes the current element.

### Merge-sort indexed inversion counts

A right-half index originally follows every left-half index. During stable merging, moved right
values are strictly smaller than the current left value; each inversion is counted at the unique
merge splitting its indices.

## Walkthrough

[5,2,6,1] yields [2,1,1,0]: the 5 exceeds later 2 and 1, while 6 exceeds only 1.

## Cost and pitfalls

Compressed Fenwick frequencies: O(n log n) time; O(n) space.

Merge-sort indexed inversion counts: O(n log n) time; O(n) space.

Inputs are unchanged. Equal values must not count; query rank-1 in Fenwick and merge equal left
values before right values. Recursion depth is logarithmic.
"""


class Solution:
    """Approach: Compressed Fenwick frequencies
    Time: O(n log n)
    Space: O(n)
    """

    def countSmaller(self, nums: list[int]) -> list[int]:
        ordered = sorted(set(nums))
        ranks = {value: i + 1 for i, value in enumerate(ordered)}
        bit = [0] * (len(ordered) + 1)
        result = []
        for value in reversed(nums):
            rank = ranks[value]
            index, count = rank - 1, 0
            while index:
                count += bit[index]
                index -= index & -index
            result.append(count)
            while rank < len(bit):
                bit[rank] += 1
                rank += rank & -rank
        return result[::-1]


class MergeSortSolution:
    """Approach: Merge-sort indexed inversion counts
    Time: O(n log n)
    Space: O(n)
    """

    def countSmaller(self, nums: list[int]) -> list[int]:
        answer = [0] * len(nums)

        def sort(items):
            if len(items) <= 1:
                return items
            middle = len(items) // 2
            left, right = sort(items[:middle]), sort(items[middle:])
            i = j = 0
            merged = []
            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    answer[left[i][1]] += j
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            for value, index in left[i:]:
                answer[index] += j
                merged.append((value, index))
            merged.extend(right[j:])
            return merged

        sort([(value, i) for i, value in enumerate(nums)])
        return answer
