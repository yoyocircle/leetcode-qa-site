"""## Task

Return the probability a knight remains on an n by n board after exactly k uniformly random
choices among its eight moves.

## Hints

1. Off-board probability mass is lost, not renormalized.
2. Survival from a cell can also be computed backward by remaining moves.

## Approach

### Forward knight probability layers

Track probability mass at each surviving location and send one eighth to each valid move
destination at every step.

### Backward survival probabilities

Cache the survival probability for position and remaining moves. Outside states are zero and
inside zero-move states are one.

## Why it works

### Forward knight probability layers

Independence and equal move probabilities multiply each incoming path weight by one eighth.
Summing disjoint arriving paths gives each state probability, and the final board sum is
survival probability.

### Backward survival probabilities

Conditioning on the first of eight equally likely moves yields the average of successor
survival probabilities. These cases exhaust the next move, proving the recurrence by
remaining-step induction.

## Walkthrough

On a 3x3 board from a corner with one move, two of eight destinations are valid, giving 0.25.

## Cost and pitfalls

Forward knight probability layers: O((k+1)*n^2) time; O(n^2) space.
Backward survival probabilities: O((k+1)*n^2) time; O((k+1)*n^2) space.

Inputs are unchanged. k=0 returns one at every valid starting cell. Memo depth is at most
100, while its cache may retain every step layer; forward propagation saves that factor. Do
not divide by the number of valid moves.
"""


class Solution:
    """Approach: Forward knight probability layers
    Time: O((k+1)*n^2)
    Space: O(n^2)
    """

    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        moves = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))
        current = [[0.0] * n for _ in range(n)]
        current[row][column] = 1.0
        for _ in range(k):
            following = [[0.0] * n for _ in range(n)]
            for r in range(n):
                for c in range(n):
                    for dr, dc in moves:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n:
                            following[nr][nc] += current[r][c] / 8
            current = following
        return sum(map(sum, current))


class MemoSolution:
    """Approach: Backward survival probabilities
    Time: O((k+1)*n^2)
    Space: O((k+1)*n^2)
    """

    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        from functools import cache

        moves = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))

        @cache
        def survive(r, c, remaining):
            if not (0 <= r < n and 0 <= c < n):
                return 0.0
            if remaining == 0:
                return 1.0
            return sum(survive(r + dr, c + dc, remaining - 1) for dr, dc in moves) / 8

        return survive(row, column, k)
