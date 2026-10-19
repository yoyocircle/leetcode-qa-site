"""
## Task

Split a nonnegative integer array into exactly k nonempty contiguous pieces, minimizing the
largest piece sum.

## Hints

1. A proposed maximum sum permits a greedy count of required pieces.
2. A partition DP can enumerate the final piece boundary.

## Approach

### Binary search a feasible maximum sum

Search between the maximum element and total sum. Greedily extend each piece until adding the
next value would exceed the candidate limit.

### Exact-piece dynamic programming

For each piece count, compute the optimal maximum sum for each prefix by trying every valid
final-piece start. This educational baseline may time out at full constraints.

## Why it works

### Binary search a feasible maximum sum

For a fixed limit, ending a piece as late as possible cannot use more pieces than any earlier
cut. Feasibility is monotone in the limit. A partition with at most k pieces can be refined into
exactly k because all values are nonnegative and k<=n.

### Exact-piece dynamic programming

Every partition of a prefix into c pieces consists of an optimal c-1-piece prefix and one
nonempty final interval. Minimizing the maximum of their costs over every split enumerates
exactly all legal partitions.

## Walkthrough

[7,2,5,10,8], k=2 splits as [7,2,5] and [10,8], with maximum 18. A limit of 17 requires three
pieces.

## Cost and pitfalls

Binary search a feasible maximum sum: O(n log(S+1)) time; O(1) space.

Exact-piece dynamic programming: O(k*n squared) time; O(n) space.

Inputs are unchanged. S is total sum. Zero values are permitted; splitting an existing piece
never raises its sum. Exactly-k DP states must leave enough elements for nonempty pieces.
"""


class Solution:
    """Approach: Binary search a feasible maximum sum
    Time: O(n log(S+1))
    Space: O(1)
    """

    def splitArray(self, nums: list[int], k: int) -> int:
        low, high = max(nums), sum(nums)
        while low < high:
            limit = (low + high) // 2
            pieces, total = 1, 0
            for value in nums:
                if total + value > limit:
                    pieces += 1
                    total = 0
                total += value
            if pieces <= k:
                high = limit
            else:
                low = limit + 1
        return low


class PartitionDPSolution:
    """Approach: Exact-piece dynamic programming
    Time: O(k*n squared)
    Space: O(n)
    """

    def splitArray(self, nums: list[int], k: int) -> int:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        previous = [0] + [float("inf")] * len(nums)
        for pieces in range(1, k + 1):
            current = [float("inf")] * (len(nums) + 1)
            for end in range(pieces, len(nums) + 1):
                current[end] = min(
                    max(previous[start], prefix[end] - prefix[start])
                    for start in range(pieces - 1, end)
                )
            previous = current
        return int(previous[-1])
