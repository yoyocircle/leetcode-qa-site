"""## Task

Compute P(A empties first)+0.5*P(both empty together) for the four equally likely
simultaneous soup-serving choices.

## Hints

1. Round volume upward into units of 25mL.
2. For large equal initial amounts, returning one needs an error proof rather than an
empirical threshold.

## Approach

### Backward remaining-soup probability table

Normalize to m=ceil(n/25). Empty A with nonempty B has value one, empty B alone zero, and
both empty one half. Fill increasing A because every move decreases A. Return one when
m>=480.

### Forward unfinished-state probability frontiers

Propagate probability only among states where both soups remain positive. Collect A-first
mass and half the simultaneous-empty mass; discard B-first mass. Use the same justified
large-volume cutoff.

## Why it works

### Backward remaining-soup probability table

Conditioning on the first serving gives the average of four smaller-A states, so
increasing-A order solves the exact recurrence. Rounding is exact because every requested
removal is a multiple of 25 and only whether remaining volume is positive matters.

### Forward unfinished-state probability frontiers

Each frontier represents one serving round, so terminal outcomes partition all probability
paths exactly once. Before termination, A+B=2m-4t, leaving only O(m) possible states per
round and O(m) rounds.

## Walkthrough

For n=50, the four first moves contribute 1,1,0.5,0, so the result is 0.625. For n=0, both
are already empty and the result is 0.5.

## Cost and pitfalls

Backward remaining-soup probability table: O(m^2) below cutoff; O(1) above time; O(m^2)
below cutoff; O(1) above space.
Forward unfinished-state probability frontiers: O(m^2) below cutoff; O(1) above time; O(m)
below cutoff; O(1) above space.

Both preserve n. Cutoff proof: pre-sample independent B removals Y in {0,1,2,3}, mean 1.5.
The process stops by T=ceil(m/2), since each unfinished round removes four total units. If B
empties no later than A, sum(Y_1..Y_T)>=m. Hoeffding therefore bounds the error of returning
one by exp(-2*(m-1.5*T)^2/(9*T)), at most exp(-(m-3)^2/(36*(m+1)))<1.97e-6 for m>=480. This
is below the official 1e-5 tolerance, with room for floating-point rounding. Sources:
[official rules and tolerance](https://leetcode.com/problems/soup-servings/) and [Hoeffding
inequality, Theorem 2](https://web.stanford.edu/~jduchi/projects/probability_bounds.pdf).
The inequality is a derived bound here, not a claim that the official page specifies this
cutoff.
"""


class Solution:
    """Approach: Backward remaining-soup probability table
    Time: O(m^2) below cutoff; O(1) above
    Space: O(m^2) below cutoff; O(1) above
    """

    def soupServings(self, n: int) -> float:
        size = (n + 24) // 25
        if size >= 480:
            return 1.0
        dp = [[0.0] * (size + 1) for _ in range(size + 1)]
        dp[0] = [1.0] * (size + 1)
        dp[0][0] = 0.5
        for a in range(1, size + 1):
            for b in range(1, size + 1):
                dp[a][b] = (
                    sum(
                        dp[max(0, a - da)][max(0, b - db)]
                        for da, db in ((4, 0), (3, 1), (2, 2), (1, 3))
                    )
                    / 4
                )
        return dp[size][size]


class ForwardSolution:
    """Approach: Forward unfinished-state probability frontiers
    Time: O(m^2) below cutoff; O(1) above
    Space: O(m) below cutoff; O(1) above
    """

    def soupServings(self, n: int) -> float:
        size = (n + 24) // 25
        if size >= 480:
            return 1.0
        if size == 0:
            return 0.5
        frontier = {(size, size): 1.0}
        answer = 0.0
        while frontier:
            following = {}
            for (a, b), probability in frontier.items():
                for da, db in ((4, 0), (3, 1), (2, 2), (1, 3)):
                    na, nb = a - da, b - db
                    mass = probability / 4
                    if na <= 0:
                        answer += mass * (0.5 if nb <= 0 else 1.0)
                    elif nb > 0:
                        state = (na, nb)
                        following[state] = following.get(state, 0.0) + mass
            frontier = following
        return answer
