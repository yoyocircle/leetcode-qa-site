"""
## Task

Count subarrays whose median equals k in a permutation of 1..n. For even lengths, median means
the left of the two central sorted values.

## Hints

1. Every qualifying subarray contains the unique k.
2. Map values above k to +1 and below k to -1.

## Approach

### Balance matching around the pivot

Find k, count all balances extending left from it, then match each right balance so the full
balance is zero or one.

### Difference of median-threshold Fenwick counts

Count subarrays whose left median is at least k, then subtract those at least k+1. For a
threshold, encode qualifying values as +1 and the others as -1 and count strictly positive sums
using prefix-order statistics.

## Why it works

### Balance matching around the pivot

With k included once, left-median equality requires the number above k to equal the number below
k for odd length, or exceed it by one for even length. Matching balances zero and one covers
exactly these cases.

### Difference of median-threshold Fenwick counts

A left median meets the threshold exactly when a strict majority of entries meet it, which means
positive encoded sum. Earlier prefixes strictly smaller than the current prefix count these
sums; threshold subtraction isolates median k.

## Walkthrough

[3,2,1,4,5], k=4 counts [4], [4,5], and [1,4,5]. The even window [4,5] uses left median 4, not
average 4.5.

## Cost and pitfalls

Balance matching around the pivot: O(n) expected time; O(n) space.

Difference of median-threshold Fenwick counts: O(n log n) time; O(n) space.

Inputs are unchanged. The pivot method uses the promised unique k; the threshold formulation
also works with duplicate values. Strict prefix comparison is essential for the left-median
convention.
"""


class Solution:
    """Approach: Balance matching around the pivot
    Time: O(n) expected
    Space: O(n)
    """

    def countSubarrays(self, nums: list[int], k: int) -> int:
        pivot = nums.index(k)
        counts = {0: 1}
        balance = 0
        for i in range(pivot - 1, -1, -1):
            balance += 1 if nums[i] > k else -1
            counts[balance] = counts.get(balance, 0) + 1
        balance = answer = 0
        for i in range(pivot, len(nums)):
            if i > pivot:
                balance += 1 if nums[i] > k else -1
            answer += counts.get(-balance, 0) + counts.get(1 - balance, 0)
        return answer


class ThresholdFenwickSolution:
    """Approach: Difference of median-threshold Fenwick counts
    Time: O(n log n)
    Space: O(n)
    """

    def countSubarrays(self, nums: list[int], k: int) -> int:
        def at_least(threshold):
            size = 2 * len(nums) + 3
            offset = len(nums) + 1
            bit = [0] * size

            def add(index):
                while index < size:
                    bit[index] += 1
                    index += index & -index

            def count(index):
                answer = 0
                while index:
                    answer += bit[index]
                    index -= index & -index
                return answer

            prefix = answer = 0
            add(offset)
            for value in nums:
                prefix += 1 if value >= threshold else -1
                answer += count(prefix + offset - 1)
                add(prefix + offset)
            return answer

        return at_least(k) - at_least(k + 1)
