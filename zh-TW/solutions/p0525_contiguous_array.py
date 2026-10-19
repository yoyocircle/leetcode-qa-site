"""
## Task

Return the greatest length of a contiguous binary subarray with equally many
zeros and ones.

## Hints

1. Treat a zero as -1 and a one as +1.
2. If two prefixes have the same balance, what lies between them?

## Approach

### First index per balance

Checking every interval costs O(n squared). Track the running balance and the
first index where each balance appeared. Repeating a balance gives a zero-sum
interval; compare its length with the best so far.

### Sort equal prefix balances

Pair every prefix balance with its index, sort the pairs, and compare the smallest and largest
index in each equal-balance group. This replaces hashing with sorting.

## Why it works

### First index per balance

Equal prefix balances mean the interval has net balance zero, hence equal counts.
The earliest occurrence gives the longest interval ending at the current index,
so later occurrences must never replace it.

### Sort equal prefix balances

A subarray is balanced exactly when its endpoint prefix balances match. The farthest pair in
each group is its longest candidate; taking the largest group span is optimal.

## Walkthrough

For [0, 0, 1, 1, 1], balances are -1, -2, -1, 0, 1. Balance 0 was first
seen at index -1; repeating it at index 3 gives length 4.

## Cost and pitfalls

Default approach (First index per balance):

Expected O(n) time and O(n) space. Inputs are unchanged. Seed balance 0 at -1
to include intervals starting at index 0. This problem stores an earliest index,
unlike Subarray Sum Equals K, which needs a count of earlier prefixes.

First index per balance: O(n) expected time; O(n) space.
Sort equal prefix balances: O(n log n) time; O(n) space. Pair every prefix balance with its
index, sort the pairs, and compare the smallest and largest index in each equal-balance group.
This replaces hashing with sorting.
"""


class Solution:
    """Approach: First index per balance
    Time: O(n) expected
    Space: O(n)
    """

    def findMaxLength(self, nums: list[int]) -> int:
        first = {0: -1}
        balance = best = 0
        for i, number in enumerate(nums):
            balance += 1 if number else -1
            if balance in first:
                best = max(best, i - first[balance])
            else:
                first[balance] = i
        return best


class SortedBalanceSolution:
    """Approach: Sort equal prefix balances
    Time: O(n log n)
    Space: O(n)
    """

    def findMaxLength(self, nums: list[int]) -> int:
        prefixes = [(0, -1)]
        balance = 0
        for i, value in enumerate(nums):
            balance += 1 if value else -1
            prefixes.append((balance, i))
        prefixes.sort()
        first = 0
        best = 0
        for i, (balance, index) in enumerate(prefixes):
            if i == 0 or balance != prefixes[i - 1][0]:
                first = index
            best = max(best, index - first)
        return best
