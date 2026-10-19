"""## Task

Return a largest subset of distinct positive integers in which every pair divides one another.

## Hints

1. Sorting turns a divisible subset into an increasing divisibility chain.
2. Retain either predecessor indices or the best chain itself.

## Approach

### Lengths and predecessor links

Sort a copy and compute the best chain ending at each number. Store only its length and
chosen predecessor, then reconstruct the longest chain.

### Explicit best chains by endpoint

Retain the complete best chain for every endpoint. Find the longest divisible predecessor
chain and copy it once before appending the current number.

## Why it works

### Lengths and predecessor links

Divisibility is transitive. Extending a divisible predecessor chain preserves pairwise
divisibility, and every valid sorted subset has such a predecessor chain.

### Explicit best chains by endpoint

The selected predecessor maximizes attainable chain length; its copied sequence is valid by
transitivity. Considering every endpoint covers the largest subset.

## Walkthrough

For [1,2,3,6], either [1,2,6] or [1,3,6] is valid and has size 3.

## Cost and pitfalls

Lengths and predecessor links: O(n^2) time; O(n) space.
Explicit best chains by endpoint: O(n^2) time; O(n^2) space.

Inputs remain unchanged. Sorted storage and final reversal allocate copies. Explicit chains
have quadratic total copying/storage in the longest-chain case; predecessor links avoid it.
Multiple optimal answers are accepted.
"""


class Solution:
    """Approach: Lengths and predecessor links
    Time: O(n^2)
    Space: O(n)
    """

    def largestDivisibleSubset(self, nums: list[int]) -> list[int]:
        ordered = sorted(nums)
        lengths, previous = [1] * len(nums), [-1] * len(nums)
        best = 0
        for i in range(len(nums)):
            for j in range(i):
                if ordered[i] % ordered[j] == 0 and lengths[j] + 1 > lengths[i]:
                    lengths[i], previous[i] = lengths[j] + 1, j
            if lengths[i] > lengths[best]:
                best = i
        result = []
        while best >= 0:
            result.append(ordered[best])
            best = previous[best]
        return result[::-1]


class ChainSolution:
    """Approach: Explicit best chains by endpoint
    Time: O(n^2)
    Space: O(n^2)
    """

    def largestDivisibleSubset(self, nums: list[int]) -> list[int]:
        ordered = sorted(nums)
        chains = []
        for i, value in enumerate(ordered):
            best = []
            for j in range(i):
                if value % ordered[j] == 0 and len(chains[j]) > len(best):
                    best = chains[j]
            chains.append(best + [value])
        return max(chains, key=len)
