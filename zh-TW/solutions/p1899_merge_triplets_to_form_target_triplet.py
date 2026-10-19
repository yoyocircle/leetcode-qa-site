"""
## Task

You may merge triplets by taking coordinatewise maxima. Decide whether some sequence of merges
can produce the target triplet.

## Hints

1. A triplet exceeding any target coordinate can never participate.
2. Among eligible triplets, every target coordinate must be attained somewhere.

## Approach

### Accumulate eligible maxima

Ignore any triplet with an oversized coordinate. Compute coordinatewise maxima over all eligible
triplets and compare with target.

### Coordinate witness bit mask

For every eligible triplet, set the bit of each coordinate equal to its target. All three
witness bits must become set.

## Why it works

### Accumulate eligible maxima

An oversized value cannot decrease under merges. All eligible merges stay at most target; if
each coordinate reaches target in their combined maximum, merging those triplets constructs
target.

### Coordinate witness bit mask

Eligibility prevents overshoot, while each set bit proves one required coordinate is available.
The union of witnesses can be merged, and without a witness no maximum operation can invent that
coordinate.

## Walkthrough

[[2,5,3],[1,8,4],[1,7,5]], target [2,7,5]: ignore [1,8,4], then merge the other two to obtain
the target.

## Cost and pitfalls

Accumulate eligible maxima: O(n) time; O(1) space.

Coordinate witness bit mask: O(n) time; O(1) space.

Inputs are unchanged. Coordinates are positive under the contract, so zero is a safe initial
maximum. Requiring one triplet to match every coordinate would miss valid merges.
"""


class Solution:
    """Approach: Accumulate eligible maxima
    Time: O(n)
    Space: O(1)
    """

    def mergeTriplets(self, triplets: list[list[int]], target: list[int]) -> bool:
        best = [0, 0, 0]
        for values in triplets:
            if all(value <= bound for value, bound in zip(values, target, strict=True)):
                for i in range(3):
                    best[i] = max(best[i], values[i])
        return best == target


class WitnessSolution:
    """Approach: Coordinate witness bit mask
    Time: O(n)
    Space: O(1)
    """

    def mergeTriplets(self, triplets: list[list[int]], target: list[int]) -> bool:
        witnessed = 0
        for values in triplets:
            if any(value > target[i] for i, value in enumerate(values)):
                continue
            for i, value in enumerate(values):
                if value == target[i]:
                    witnessed |= 1 << i
        return witnessed == 7
