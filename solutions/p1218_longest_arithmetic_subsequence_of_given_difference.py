"""## Task

Find the longest subsequence whose adjacent selected values differ by the given fixed
difference.

## Hints

1. A current value has only one required predecessor value.
2. An index-based DP offers a direct but slower baseline.

## Approach

### Best length by final value

Scan in order and extend the longest previously seen subsequence ending at value-difference.
Store its new best under value.

### Index endpoint recurrence

Retain one length per endpoint and inspect every earlier index with the required value
difference.

## Why it works

### Best length by final value

Every valid predecessor has that exact value. Among such predecessors, only the longest
chain matters to all future extensions, so merging states by final value loses nothing.

### Index endpoint recurrence

Removing the last selected element leaves a smaller endpoint state. All legal predecessors
are tested and earlier index order enforces the subsequence constraint.

## Walkthrough

For [1,5,7,8,5,3,4,2,1] and difference -2, select 7,5,3,1 for length 4.

## Cost and pitfalls

Best length by final value: O(n) expected time; O(u) space.
Index endpoint recurrence: O(n^2) time; O(n) space.

u is distinct value count. Both preserve arr. The quadratic baseline may time out at
n=100000; use the dictionary default. Difference zero permits repeated equal values and must
extend from the old stored state.
"""


class Solution:
    """Approach: Best length by final value
    Time: O(n) expected
    Space: O(u)
    """

    def longestSubsequence(self, arr: list[int], difference: int) -> int:
        best = {}
        answer = 0
        for value in arr:
            length = best.get(value - difference, 0) + 1
            best[value] = max(best.get(value, 0), length)
            answer = max(answer, length)
        return answer


class QuadraticSolution:
    """Approach: Index endpoint recurrence
    Time: O(n^2)
    Space: O(n)
    """

    def longestSubsequence(self, arr: list[int], difference: int) -> int:
        lengths = [1] * len(arr)
        for i in range(len(arr)):
            for j in range(i):
                if arr[i] - arr[j] == difference:
                    lengths[i] = max(lengths[i], lengths[j] + 1)
        return max(lengths)
