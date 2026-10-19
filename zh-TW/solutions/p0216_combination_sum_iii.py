"""## Task

Return combinations of k distinct integers from 1 through 9 whose sum is n. Each answer uses
each digit at most once.

## Hints

1. Choose digits in increasing order.
2. The domain is small enough to enumerate all nine-bit subsets.

## Approach

### Increasing-digit backtracking

Grow increasing paths while decreasing the remainder. Stop after k selections, recording only
remainder zero. Positive digits permit early stopping when a digit exceeds the remainder.

### Nine-bit subset enumeration

Enumerate masks, keep those with exactly k set bits, materialize their digits, and test their
sum.

## Why it works

### Increasing-digit backtracking

Increasing indices prevent reuse and alternate orderings. Every allowed digit subset has one
increasing choice sequence, so each matching combination is found once.

### Nine-bit subset enumeration

A nine-bit mask is a unique subset of 1..9. Filtering by population count and sum is exactly the
problem's size and total condition.

## Walkthrough

For k=3 and n=9, return [1,2,6], [1,3,5], and [2,3,4].

## Cost and pitfalls

Increasing-digit backtracking: O(9*2^9) loose bound time; O(k) auxiliary plus output space.
Nine-bit subset enumeration: O(9*2^9) time; O(k) auxiliary plus output space.
Inputs are unchanged. Mask enumeration has a fixed 512 candidates, making it a practical
alternative. Do not permit digit zero or repeated digits. Copy paths before undoing choices.
"""


class Solution:
    """Approach: Increasing-digit backtracking
    Time: O(9*2^9) loose bound
    Space: O(k) auxiliary plus output
    """

    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        result, path = [], []

        def visit(start, remaining):
            if len(path) == k:
                if remaining == 0:
                    result.append(path.copy())
                return
            for value in range(start, 10):
                if value > remaining:
                    break
                path.append(value)
                visit(value + 1, remaining - value)
                path.pop()

        visit(1, n)
        return result


class MaskSolution:
    """Approach: Nine-bit subset enumeration
    Time: O(9*2^9)
    Space: O(k) auxiliary plus output
    """

    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        result = []
        for mask in range(1 << 9):
            if mask.bit_count() == k:
                digits = [index + 1 for index in range(9) if mask & (1 << index)]
                if sum(digits) == n:
                    result.append(digits)
        return result
