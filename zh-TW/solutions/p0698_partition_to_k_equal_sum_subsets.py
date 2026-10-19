"""## Task

Partition every positive input number into k nonempty groups with equal sums. Return whether
such a partition exists.

## Hints

1. The total must divide evenly by the group count.
2. Either place large values into symmetric buckets or remember the remainder for each
   used-index mask.

## Approach

### Descending bucket assignment

Sort a copy descending and place each next value into a bucket that stays within the target.
Skip buckets with a load already tried at this depth; stop after a failed empty bucket.

### Used-mask remainder DP

For each reachable index mask store the current unfinished bucket sum. Add an unused value if it
fits; a completed bucket resets the remainder to zero.

## Why it works

### Descending bucket assignment

Each placement assigns one value without exceeding the required total. Equal-load buckets are
interchangeable, so symmetry pruning removes duplicate states rather than distinct feasible
partitions.

### Used-mask remainder DP

A mask fixes the total selected sum and thus its remainder modulo target. Remembering one
remainder is sufficient, and every legal ordered group filling corresponds to a path through
these masks.

## Walkthrough

For [2,2,2,2] and k=2, the target is 4 and two groups [2,2] succeed.

## Cost and pitfalls

Descending bucket assignment: O(n log n + k^n) loose bound time; O(n*k) space.
Used-mask remainder DP: O(n*2^n) time; O(2^n) space.
Inputs are unchanged. Exponential search is appropriate for the small maximum n (15 or 16).
Sorting largest first exposes impossible assignments earlier. The bitmask table trades
predictable work for exponential storage. Bucket search can retain up to k tried
loads at each of n active recursive frames.
"""


class Solution:
    """Approach: Descending bucket assignment
    Time: O(n log n + k^n) loose bound
    Space: O(n*k)
    """

    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        values = sorted(nums, reverse=True)
        total = sum(values)
        if total % k:
            return False
        target = total // k
        if values[0] > target:
            return False
        loads = [0] * k

        def place(index):
            if index == len(values):
                return True
            tried = set()
            for bucket, load in enumerate(loads):
                if load in tried or load + values[index] > target:
                    continue
                tried.add(load)
                loads[bucket] += values[index]
                if place(index + 1):
                    return True
                loads[bucket] -= values[index]
                if load == 0:
                    break
            return False

        return place(0)


class BitmaskDPSolution:
    """Approach: Used-mask remainder DP
    Time: O(n*2^n)
    Space: O(2^n)
    """

    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        values = nums
        total = sum(values)
        if total % k:
            return False
        target = total // k
        if target == 0:
            return True
        remainders = [-1] * (1 << len(values))
        remainders[0] = 0
        for mask, remainder in enumerate(remainders):
            if remainder < 0:
                continue
            for index, value in enumerate(values):
                bit = 1 << index
                if not mask & bit and remainder + value <= target:
                    remainders[mask | bit] = (remainder + value) % target
        return remainders[-1] == 0
