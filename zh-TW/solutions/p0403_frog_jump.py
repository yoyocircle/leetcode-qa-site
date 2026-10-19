"""## Task

Decide whether a frog can reach the last sorted stone, starting with a jump of one and then
using previous jump length minus one, equal, or plus one, always positive.

## Hints

1. A reachable stone needs the previous jump length as state.
2. A dense index-pair recurrence can derive the needed last jump from stone positions.

## Approach

### Sparse jump-length sets by stone position

Associate every stone position with reachable last-jump lengths. Starting at position zero
with length zero forces the first positive choice to one; propagate only to existing stones.

### Dense arrival-index and last-jump table

For every earlier stone pair, compute their distance as the required arriving jump. It is
reachable if the earlier stone supports a last jump one smaller, equal, or one larger.

## Why it works

### Sparse jump-length sets by stone position

Each propagated state appends one allowed jump to an existing valid route. Conversely, every
route arrives from an earlier stone with one of those three predecessor-length transitions,
so scanning positions ascending discovers it.

### Dense arrival-index and last-jump table

After visiting at most n stones, jump length cannot exceed n because it starts at one and
grows by at most one. Thus a bounded jump dimension covers every route; the predecessor
recurrence checks exactly the legal final transitions.

## Walkthrough

Stones [0,1,3,5,6,8,12,17] permit jumps 1,2,2,3,4,5 and reach the end.

## Cost and pitfalls

Sparse jump-length sets by stone position: O(n^2) expected time; O(n^2) space.
Dense arrival-index and last-jump table: O(n^2) time; O(n^2) space.

Both preserve stones. Sparse sets can avoid many impossible jump states, while the dense
table guarantees quadratic scanning and allocates n*(n+1) references. Neither uses
recursion, important at n=2000. Positions are strictly increasing, so no state updates its
own set.
"""


class Solution:
    """Approach: Sparse jump-length sets by stone position
    Time: O(n^2) expected
    Space: O(n^2)
    """

    def canCross(self, stones: list[int]) -> bool:
        jumps = {position: set() for position in stones}
        jumps[0].add(0)
        for position in stones:
            for previous in jumps[position]:
                for following in (previous - 1, previous, previous + 1):
                    target = position + following
                    if following > 0 and target in jumps:
                        jumps[target].add(following)
        return bool(jumps[stones[-1]])


class TableSolution:
    """Approach: Dense arrival-index and last-jump table
    Time: O(n^2)
    Space: O(n^2)
    """

    def canCross(self, stones: list[int]) -> bool:
        n = len(stones)
        dp = [[False] * (n + 1) for _ in stones]
        dp[0][0] = True
        for end in range(1, n):
            for previous in range(end):
                jump = stones[end] - stones[previous]
                if jump > n:
                    continue
                dp[end][jump] = (
                    dp[end][jump]
                    or dp[previous][jump - 1]
                    or dp[previous][jump]
                    or (jump < n and dp[previous][jump + 1])
                )
        return any(dp[-1])
