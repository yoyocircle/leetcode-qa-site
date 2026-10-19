"""## Task

Return the length of the longest strictly increasing subsequence. Selected
elements keep their original order but need not occupy adjacent positions.

## Hints

1. Among equal-length subsequences, a smaller final value is easier to extend.
2. Store one smallest tail for each length, then binary-search where a value fits.

## Approach

### Binary-search smallest tails

Maintain tails[k], the smallest possible final value of an increasing
subsequence of length k+1 in the processed prefix. For each value, use
bisect_left to find the first tail at least as large. Replace that tail,
or append if all tails are smaller. The number of tails is the answer.
This compresses subsequence-length states without keeping predecessor links.

### Subsequence ending at each index

Let lengths[i] be the longest increasing subsequence ending exactly at i. Start each at one
and inspect earlier smaller values as possible predecessors.

### Fenwick prefix maximum

Compress values to sorted ranks. Query the best subsequence length over strictly smaller
ranks, add one, and update the current rank in a Fenwick tree storing maxima.

## Why it works

### Binary-search smallest tails

Tails are strictly increasing. A value placed at index k can extend a
subsequence of length k because its previous tail is smaller. Replacing
the existing length-(k+1) tail improves or preserves future extension
possibilities. It cannot create a longer length unless all prior tails are
smaller, in which case appending is justified. These updates preserve the
smallest-tail invariant for every achievable length.

### Subsequence ending at each index

An increasing subsequence ending at i either contains only that value or extends an earlier
smaller final value. Trying all predecessors finds its optimum; the maximum over endpoints
gives the answer.

### Fenwick prefix maximum

Each query combines exactly the possible smaller-valued predecessors already processed.
Disjoint Fenwick prefix intervals cover every such rank; max updates retain the best
endpoint length. Thus it implements the endpoint recurrence in logarithmic time.

## Walkthrough

For [4,1,3,2,5], tails evolves as [4], [1], [1,3], [1,2], [1,2,5].
The answer is 3. Intermediate tails summarize possibilities; they are not
necessarily an actual subsequence with consistent stored positions.

## Cost and pitfalls

For the default Binary-search smallest tails approach:

O(n log n) time and O(n) space; input is unchanged. Assignment replaces
an entry in O(1); it does not insert and shift elements. bisect_left
ensures duplicate values do not extend a strictly increasing subsequence.

Binary-search smallest tails: O(n log n) time; O(n) space.
Subsequence ending at each index: O(n^2) time; O(n) space.
The quadratic baseline is useful for the recurrence but may be slow near the largest limits
and misses the O(n log n) follow-up. Both preserve input.

Fenwick prefix maximum: O(n log n) time and O(n) space, including coordinate compression.
This variant supports value-prefix queries and generalizes to LIS counting; the tails method
is shorter when only length is needed. Inputs remain unchanged.
"""

from bisect import bisect_left


class Solution:
    """Approach: Binary-search smallest tails
    Time: O(n log n)
    Space: O(n)
    """

    def lengthOfLIS(self, nums: list[int]) -> int:
        tails: list[int] = []
        for value in nums:
            position = bisect_left(tails, value)
            if position == len(tails):
                tails.append(value)
            else:
                tails[position] = value
        return len(tails)


class QuadraticSolution:
    """Approach: Subsequence ending at each index
    Time: O(n^2)
    Space: O(n)
    """

    def lengthOfLIS(self, nums: list[int]) -> int:
        lengths = [1] * len(nums)
        for end in range(len(nums)):
            for previous in range(end):
                if nums[previous] < nums[end]:
                    lengths[end] = max(lengths[end], lengths[previous] + 1)
        return max(lengths)


class FenwickSolution:
    """Approach: Fenwick prefix maximum
    Time: O(n log n)
    Space: O(n)
    """

    def lengthOfLIS(self, nums: list[int]) -> int:
        ranks = {value: index + 1 for index, value in enumerate(sorted(set(nums)))}
        tree = [0] * (len(ranks) + 1)
        answer = 0
        for value in nums:
            rank = ranks[value]
            index, length = rank - 1, 0
            while index:
                length = max(length, tree[index])
                index -= index & -index
            length += 1
            answer = max(answer, length)
            index = rank
            while index < len(tree):
                tree[index] = max(tree[index], length)
                index += index & -index
        return answer
