"""
## Task

Count nonempty contiguous subarrays whose sum is in the inclusive range [lower,upper]. Values
may be negative.

## Hints

1. A subarray sum is a difference of two prefix sums.
2. For each current prefix, count earlier prefixes in [current-upper,current-lower].

## Approach

### Merge-sort prefix difference counting

Merge-sort prefix sums. For each left-half prefix, advance two right-half pointers delimiting
the allowed difference interval, then merge the halves.

### Compressed Fenwick prefix counts

Compress all prefix values and insert them in original order. Two rank-prefix queries count
prior prefixes in the required inclusive interval.

## Why it works

### Merge-sort prefix difference counting

Original prefix order guarantees each left-half prefix precedes every right-half prefix at that
merge. Sorted values make both valid-range boundaries monotone; every eligible prefix pair is
counted at its unique split.

### Compressed Fenwick prefix counts

Before inserting the current prefix, the tree contains precisely earlier prefix positions.
Subtracting counts below the lower bound from counts at most the upper bound counts exactly
eligible subarray starts.

## Walkthrough

[-2,5,-1] with bounds [-2,2] has qualifying sums -2, -1, and 2, giving three subarrays.

## Cost and pitfalls

Merge-sort prefix difference counting: O(n log n) time; O(n) space.

Compressed Fenwick prefix counts: O(n log n) time; O(n) space.

Inputs are unchanged. Inclusive boundaries require different < and <= pointer tests. Python
integers handle prefix sums beyond signed-32-bit range.
"""

from bisect import bisect_left, bisect_right


class Solution:
    """Approach: Merge-sort prefix difference counting
    Time: O(n log n)
    Space: O(n)
    """

    def countRangeSum(self, nums: list[int], lower: int, upper: int) -> int:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)

        def sort(values):
            if len(values) <= 1:
                return values, 0
            middle = len(values) // 2
            left, first = sort(values[:middle])
            right, second = sort(values[middle:])
            answer = first + second
            low = high = 0
            for value in left:
                while low < len(right) and right[low] - value < lower:
                    low += 1
                while high < len(right) and right[high] - value <= upper:
                    high += 1
                answer += high - low
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged, answer

        return sort(prefix)[1]


class FenwickSolution:
    """Approach: Compressed Fenwick prefix counts
    Time: O(n log n)
    Space: O(n)
    """

    def countRangeSum(self, nums: list[int], lower: int, upper: int) -> int:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        ordered = sorted(set(prefix))
        bit = [0] * (len(ordered) + 1)

        def count(end):
            result = 0
            while end:
                result += bit[end]
                end -= end & -end
            return result

        answer = 0
        for value in prefix:
            answer += count(bisect_right(ordered, value - lower)) - count(
                bisect_left(ordered, value - upper)
            )
            index = bisect_left(ordered, value) + 1
            while index < len(bit):
                bit[index] += 1
                index += index & -index
        return answer
