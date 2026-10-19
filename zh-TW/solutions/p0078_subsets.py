"""## Task

Return every subset of an array of distinct values, including the empty subset.
Subset order and result order do not matter.

## Hints

1. Build a subset by choosing later indices only.
2. Save a copy whenever the current path itself is a valid answer.

## Approach

### Increasing-index backtracking

Backtrack from a starting index. Record the current subset, then choose each
remaining value in turn, recurse after its index, and undo the choice.
Choosing increasing indices avoids duplicate representations.

### Subset bitmasks

Enumerate masks from zero through 2^n-1. Bit i selects input position i. Build a fresh list from
the set bits for each mask; no mutable recursive path is needed.

## Why it works

### Increasing-index backtracking

Every subset has one unique sequence of increasing input indices. The recursion
visits exactly those sequences, including the empty sequence, so it enumerates
each subset once.

### Subset bitmasks

Every subset corresponds to exactly one n-bit membership vector. Enumerating each vector once
therefore enumerates all subsets once, including the empty mask.

## Walkthrough

For [2,5], record [], then explore [2] and [2,5]. Undo both choices and
explore [5]. The complete answer is [[],[2],[2,5],[5]].

## Cost and pitfalls

Default approach costs and behavior:

O(n * 2^n) time including answer copies, O(n) auxiliary path/recursion space,
and O(n * 2^n) output storage. Input is unchanged. Append path.copy(), not the
live path object; otherwise later undo operations change saved answers. The
index advances after a choice because each value can be used at most once.

Alternative tradeoff: O(n*2^n) time; O(n) temporary; O(n*2^n) output space.
"""


class Solution:
    """Approach: Increasing-index backtracking
    Time: O(n*2^n)
    Space: O(n) auxiliary; O(n*2^n) output
    """

    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = []
        path = []

        def visit(start):
            result.append(path.copy())
            for i in range(start, len(nums)):
                path.append(nums[i])
                visit(i + 1)
                path.pop()

        visit(0)
        return result


class BitmaskSolution:
    """Approach: Subset bitmasks
    Time: O(n*2^n)
    Space: O(n) temporary; O(n*2^n) output
    """

    def subsets(self, nums: list[int]) -> list[list[int]]:
        return [
            [value for index, value in enumerate(nums) if mask & (1 << index)]
            for mask in range(1 << len(nums))
        ]
