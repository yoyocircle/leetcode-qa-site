"""## Task

Choose the longest chain of pairs where each selected pair end is strictly smaller than the
next selected pair start; pairs may be reordered.

## Hints

1. The earliest finishing pair leaves the most room for future pairs.
2. A sorted dependency order also supports endpoint dynamic programming.

## Approach

### Earliest-finish interval greedy

Sort a copy by finish time and accept each pair whose start exceeds the last accepted finish.

### All-predecessor pair-chain DP

Sort pairs by start and compute the best chain ending at each pair by testing every earlier
strictly compatible pair.

## Why it works

### Earliest-finish interval greedy

Replacing the first pair in an optimal remaining chain by an earliest-finishing compatible
pair cannot invalidate any later pair. Repeating that exchange proves every greedy
acceptance preserves an optimum.

### All-predecessor pair-chain DP

A chain predecessor necessarily starts earlier because each pair starts before its own end.
Sorting therefore gives a dependency order, and enumerating all final predecessors produces
the exact longest-chain recurrence.

## Walkthrough

For [[1,2],[2,3],[3,4]], strict separation permits [1,2] then [3,4], giving 2.

## Cost and pitfalls

Earliest-finish interval greedy: O(n log n) time; O(n) space.
All-predecessor pair-chain DP: O(n^2) time; O(n) space.

Both create a sorted reference list and leave pairs unchanged; that O(n) allocation is
included even in the greedy space bound. Touching endpoints do not chain. The quadratic
variant trades the exchange proof for an explicit recurrence.
"""


class Solution:
    """Approach: Earliest-finish interval greedy
    Time: O(n log n)
    Space: O(n)
    """

    def findLongestChain(self, pairs: list[list[int]]) -> int:
        end = -float("inf")
        answer = 0
        for start, finish in sorted(pairs, key=lambda pair: pair[1]):
            if start > end:
                answer += 1
                end = finish
        return answer


class DPSolution:
    """Approach: All-predecessor pair-chain DP
    Time: O(n^2)
    Space: O(n)
    """

    def findLongestChain(self, pairs: list[list[int]]) -> int:
        ordered = sorted(pairs)
        lengths = [1] * len(ordered)
        for end in range(len(ordered)):
            for previous in range(end):
                if ordered[previous][1] < ordered[end][0]:
                    lengths[end] = max(lengths[end], lengths[previous] + 1)
        return max(lengths)
