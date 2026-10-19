"""## Task

Count paths that leave an m by n grid in at most maxMove orthogonal steps from a given cell,
modulo 1,000,000,007.

## Hints

1. Only still-inside paths continue to the next step.
2. A backward state can ask how many exits remain possible from one cell with a remaining
budget.

## Approach

### Forward in-grid path-count layers

Start with one path at the source. Send each layer count to four neighbors; collect
out-of-grid contributions immediately and propagate only inside states.

### Memoized remaining-move exits

Memoize the number of exit completions from a cell with a remaining budget. An
already-outside state contributes one; an inside state with no moves contributes zero.

## Why it works

### Forward in-grid path-count layers

Each path is classified by its last step. A path is counted exactly once on its first exit,
and exited paths are never extended, so summing all layers counts precisely exits within the
move budget.

### Memoized remaining-move exits

The next direction partitions every possible exit path into four disjoint choices. Outside
states terminate before the budget-zero test, so an exit on the final allowed step is
included.

## Walkthrough

On a 1x1 grid with one move, all four directions leave the grid, giving 4.

## Cost and pitfalls

Forward in-grid path-count layers: O((M+1)*R*C) time; O(R*C) space.
Memoized remaining-move exits: O((M+1)*R*C) time; O((M+1)*R*C) space.

M=maxMove, R=m, C=n. No inputs are mutated. Memo recursion is bounded by maxMove<=50; its
cache includes move count, while the forward default retains only two grid layers. Zero
moves returns zero.
"""


class Solution:
    """Approach: Forward in-grid path-count layers
    Time: O((M+1)*R*C)
    Space: O(R*C)
    """

    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        modulus = 1_000_000_007
        current = [[0] * n for _ in range(m)]
        current[startRow][startColumn] = 1
        answer = 0
        for _ in range(maxMove):
            following = [[0] * n for _ in range(m)]
            for r in range(m):
                for c in range(n):
                    count = current[r][c]
                    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                        if 0 <= nr < m and 0 <= nc < n:
                            following[nr][nc] = (following[nr][nc] + count) % modulus
                        else:
                            answer = (answer + count) % modulus
            current = following
        return answer


class MemoSolution:
    """Approach: Memoized remaining-move exits
    Time: O((M+1)*R*C)
    Space: O((M+1)*R*C)
    """

    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        from functools import cache

        modulus = 1_000_000_007

        @cache
        def exits(row, column, remaining):
            if not (0 <= row < m and 0 <= column < n):
                return 1
            if remaining == 0:
                return 0
            return (
                sum(
                    exits(row + dr, column + dc, remaining - 1)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                )
                % modulus
            )

        return exits(startRow, startColumn, maxMove)
