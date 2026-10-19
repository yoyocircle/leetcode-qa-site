"""## Task

Count index-distinct longest strictly increasing subsequences.

## Hints

1. Each endpoint needs both a best length and a count achieving that length.
2. A Fenwick tree can merge these pairs over all smaller values.

## Approach

### Endpoint lengths and multiplicities

For each earlier smaller value, replace the endpoint count when a longer predecessor is
found or add its count when lengths tie.

### Coordinate-compressed Fenwick maxima and counts

Compress values into ranks. A prefix query below the current rank merges the longest
predecessor lengths and their counts; update the current rank with its new endpoint pair.

## Why it works

### Endpoint lengths and multiplicities

Each longer subsequence has a unique penultimate index. Counts from equally good
predecessors are therefore disjoint and additive, while shorter predecessor lengths cannot
contribute to an optimum.

### Coordinate-compressed Fenwick maxima and counts

The merge operation retains longer lengths and sums equal-length counts, matching the
endpoint recurrence. Strictly lower-rank queries exclude equal values. Fenwick disjoint
intervals avoid double-counting during a query.

## Walkthrough

For [1,3,5,4,7], [1,3,5,7] and [1,3,4,7] give 2 longest subsequences.

## Cost and pitfalls

Endpoint lengths and multiplicities: O(n^2) time; O(n) space.
Coordinate-compressed Fenwick maxima and counts: O(n log n) time; O(n) space.

Inputs are unchanged. Repeated equal values contribute separate length-one subsequences but
never extend each other. Fenwick storage is faster asymptotically but requires careful count
merging.
"""


class Solution:
    """Approach: Endpoint lengths and multiplicities
    Time: O(n^2)
    Space: O(n)
    """

    def findNumberOfLIS(self, nums: list[int]) -> int:
        lengths, counts = [1] * len(nums), [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] >= nums[i]:
                    continue
                candidate = lengths[j] + 1
                if candidate > lengths[i]:
                    lengths[i], counts[i] = candidate, counts[j]
                elif candidate == lengths[i]:
                    counts[i] += counts[j]
        longest = max(lengths)
        return sum(
            count for length, count in zip(lengths, counts, strict=True) if length == longest
        )


class FenwickSolution:
    """Approach: Coordinate-compressed Fenwick maxima and counts
    Time: O(n log n)
    Space: O(n)
    """

    def findNumberOfLIS(self, nums: list[int]) -> int:
        ranks = {value: index + 1 for index, value in enumerate(sorted(set(nums)))}
        tree = [(0, 0)] * (len(ranks) + 1)

        def merge(first, second):
            if first[0] != second[0]:
                return max(first, second, key=lambda pair: pair[0])
            return first[0], first[1] + second[1]

        answer = (0, 0)
        for value in nums:
            rank = ranks[value]
            index, best = rank - 1, (0, 0)
            while index:
                best = merge(best, tree[index])
                index -= index & -index
            candidate = (best[0] + 1, best[1] if best[0] else 1)
            answer = merge(answer, candidate)
            index = rank
            while index < len(tree):
                tree[index] = merge(tree[index], candidate)
                index += index & -index
        return answer[1]
