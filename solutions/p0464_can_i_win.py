"""## Task

Players alternately choose unused integers 1..maxChoosableInteger; the first to reach
desiredTotal wins. Decide whether the first player can force a win.

## Hints

1. The chosen-number bitmask determines both available numbers and total so far.
2. A state is winning if one move wins immediately or leaves the opponent a losing state.

## Approach

### Memoized chosen-mask minimax

Cache chosen masks and their implied remaining target. Try each unused choice and return
true if it wins now or gives the opponent a losing continuation.

### Descending-mask retrograde game table

Precompute selected-value totals for all masks, then fill winning states in decreasing
numeric mask order. Any move adds a bit, reaching an already solved larger mask.

## Why it works

### Memoized chosen-mask minimax

This is the definition of a forced win in a finite alternating game: one winning move
suffices, while a state with only opponent-winning continuations loses. The mask uniquely
determines needed, so the cache has at most 2^M meaningful states.

### Descending-mask retrograde game table

A terminal-reaching move wins immediately; every other move is good exactly when its
successor is losing. Descending-mask order respects these dependencies and evaluates the
same exhaustive game condition without recursion.

## Walkthrough

With choices 1..10 and target 11, every first choice can be answered by its complement to
11, so the first player loses.

## Cost and pitfalls

Memoized chosen-mask minimax: O(M*2^M) time; O(2^M) space.
Descending-mask retrograde game table: O(M*2^M) time; O(2^M) space.

M<=20. Both preserve inputs and first reject globally unreachable targets; target zero is
already satisfied. Memo recursion depth is bounded by M, while the dense variant always
allocates two 2^M arrays and may do substantially more work.
"""


class Solution:
    """Approach: Memoized chosen-mask minimax
    Time: O(M*2^M)
    Space: O(2^M)
    """

    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        from functools import cache

        maximum = maxChoosableInteger
        if desiredTotal <= 0:
            return True
        if maximum * (maximum + 1) // 2 < desiredTotal:
            return False

        @cache
        def winning(mask, needed):
            for value in range(1, maximum + 1):
                bit = 1 << (value - 1)
                if not mask & bit and (value >= needed or not winning(mask | bit, needed - value)):
                    return True
            return False

        return winning(0, desiredTotal)


class TableSolution:
    """Approach: Descending-mask retrograde game table
    Time: O(M*2^M)
    Space: O(2^M)
    """

    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        maximum = maxChoosableInteger
        if desiredTotal <= 0:
            return True
        if maximum * (maximum + 1) // 2 < desiredTotal:
            return False
        size = 1 << maximum
        totals = [0] * size
        for mask in range(1, size):
            bit = mask & -mask
            totals[mask] = totals[mask ^ bit] + bit.bit_length()
        wins = [False] * size
        for mask in range(size - 1, -1, -1):
            if totals[mask] >= desiredTotal:
                continue
            for value in range(1, maximum + 1):
                bit = 1 << (value - 1)
                if not mask & bit and (
                    totals[mask] + value >= desiredTotal or not wins[mask | bit]
                ):
                    wins[mask] = True
                    break
        return wins[0]
