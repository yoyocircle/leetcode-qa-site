"""## Task

Given an integer array, return a uniformly random index whose value equals a requested target.
The target is guaranteed to occur.

## Hints

1. Random selection is over matching positions, not distinct values.
2. Either sample matching indices during a scan or pre-index them once.

## Approach

### Matching-index reservoir

Retain the input reference. On each query scan matching positions and replace the sample with
probability one over the number of matches seen.

### Target-to-indices map

Build a dictionary from values to lists of original indices and select a uniform index within
the target's list.

## Why it works

### Matching-index reservoir

The reservoir invariant makes each matching position equally likely after any prefix.
Nonmatching positions never enter the sample, so final probability is one over total matches.

### Target-to-indices map

Each target list contains exactly its occurrence indices once. Uniform list-position selection
is therefore uniform over all and only matching original positions.

## Walkthrough

For [8,3,8,8], pick(8) returns one of indices 0,2,3 with equal probability; pick(3) always
returns 1.

## Cost and pitfalls

Matching-index reservoir: O(1) constructor; O(n) pick time; O(1) space.
Target-to-indices map: O(n) constructor; O(1) expected pick time; O(n) space.
Neither variant changes the input. The reservoir retains a reference and assumes values remain
stable; the indexed variant owns its index snapshot. Compare valid support and distribution, not
identical random sequences.
"""

from collections import defaultdict
from random import choice, randrange


class Solution:
    """Approach: Matching-index reservoir
    Time: O(1) constructor; O(n) pick
    Space: O(1)
    """

    def __init__(self, nums: list[int]):
        self.values = nums

    def pick(self, target: int) -> int:
        matches = 0
        selected = -1
        for index, value in enumerate(self.values):
            if value == target:
                matches += 1
                if randrange(matches) == 0:
                    selected = index
        return selected


class IndexedSolution:
    """Approach: Target-to-indices map
    Time: O(n) constructor; O(1) expected pick
    Space: O(n)
    """

    def __init__(self, nums: list[int]):
        self.indices = defaultdict(list)
        for index, value in enumerate(nums):
            self.indices[value].append(index)

    def pick(self, target: int) -> int:
        return choice(self.indices[target])
