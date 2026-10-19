"""## Task

Return unique combinations summing to target from positive candidate values that may repeat.
Each input occurrence may be used at most once.

## Hints

1. Sort so equal choices are adjacent.
2. Skip equal alternatives at one search depth, while allowing later duplicates at deeper
   depths.

## Approach

### Sorted index backtracking

Sort a copy and choose increasing indices. Skip a candidate equal to the previous candidate at
the same depth; stop once a value exceeds the remaining sum.

### Bounded multiplicity search

Compress equal candidates into value/count groups. For each group choose from zero through its
available multiplicity, bounded also by the remaining target.

## Why it works

### Sorted index backtracking

Every multiset answer has one sorted representation. Equal alternatives at one depth lead to
that same representation, while choosing later equal indices deeper still permits the available
multiplicity.

### Bounded multiplicity search

Each answer has one count for every distinct value. Enumerating these bounded count vectors
includes every permitted combination exactly once without index-level duplicate branches.

## Walkthrough

For [1,1,2,3] and target 4, return [1,1,2] and [1,3]. A third 1 cannot be used.

## Cost and pitfalls

Sorted index backtracking: O(n log n + n*2^n) loose bound time; O(n) auxiliary plus output
space.
Bounded multiplicity search: O(n log n + n*product(count+1)) loose bound time; O(n) auxiliary
plus output space.
Inputs are unchanged. Positivity makes remainder pruning valid. Do not advance to the same index
after a choice: unlike unlimited combination sum, an occurrence cannot be reused.
"""

from collections import Counter


class Solution:
    """Approach: Sorted index backtracking
    Time: O(n log n + n*2^n) loose bound
    Space: O(n) auxiliary plus output
    """

    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        values = sorted(candidates)
        result, path = [], []

        def visit(start, remaining):
            if remaining == 0:
                result.append(path.copy())
                return
            for index in range(start, len(values)):
                value = values[index]
                if value > remaining:
                    break
                if index > start and value == values[index - 1]:
                    continue
                path.append(value)
                visit(index + 1, remaining - value)
                path.pop()

        visit(0, target)
        return result


class GroupedCountsSolution:
    """Approach: Bounded multiplicity search
    Time: O(n log n + n*product(count+1)) loose bound
    Space: O(n) auxiliary plus output
    """

    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        groups = sorted(Counter(candidates).items())
        result, path = [], []

        def visit(index, remaining):
            if remaining == 0:
                result.append(path.copy())
                return
            if index == len(groups):
                return
            value, count = groups[index]
            limit = min(count, remaining // value)
            for used in range(limit + 1):
                visit(index + 1, remaining - used * value)
                if used < limit:
                    path.append(value)
            if limit:
                del path[-limit:]

        visit(0, target)
        return result
