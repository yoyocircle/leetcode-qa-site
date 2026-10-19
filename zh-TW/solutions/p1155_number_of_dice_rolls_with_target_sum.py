"""## Task

Count ordered outcomes of n dice with faces 1 through k summing to target, modulo 1,000,000,007.

## Hints

1. One die combines a sliding window of preceding-sum counts.
2. A direct face loop gives the same convolution without the sliding-window optimization.

## Approach

### Sliding-window dice convolution

Each current sum uses the preceding counts at total-1 through total-k. Maintain this range
sum as total increases, adding its new upper entry and removing the expired lower entry.

### Explicit die-face propagation

For each solved sum after the current number of dice, append every feasible face and add its
count to a fresh row.

## Why it works

### Sliding-window dice convolution

Conditioning on the newest die face partitions ordered outcomes. The maintained window
equals exactly the sum of valid predecessor counts, so it evaluates that recurrence in
constant work per sum.

### Explicit die-face propagation

Every ordered outcome is its preceding outcome plus one final face, and these choices are
disjoint. A fresh row ensures exactly one die is appended per iteration.

## Walkthrough

Two six-sided dice sum to 7 in six ordered outcomes, from (1,6) through (6,1).

## Cost and pitfalls

Sliding-window dice convolution: O(n*target) time; O(target) space.
Explicit die-face propagation: O(n*k*target) time; O(target) space.

Inputs are unchanged. Impossible targets naturally have zero count. Arrays include sum zero
for the empty-dice seed but nonempty dice never retain that state. Reducing current entries
modulo the modulus bounds Python integer sizes.
"""


class Solution:
    """Approach: Sliding-window dice convolution
    Time: O(n*target)
    Space: O(target)
    """

    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        modulus = 1_000_000_007
        previous = [0] * (target + 1)
        previous[0] = 1
        for _ in range(n):
            current = [0] * (target + 1)
            window = 0
            for total in range(1, target + 1):
                window += previous[total - 1]
                if total - k - 1 >= 0:
                    window -= previous[total - k - 1]
                current[total] = window % modulus
            previous = current
        return previous[target]


class FaceLoopSolution:
    """Approach: Explicit die-face propagation
    Time: O(n*k*target)
    Space: O(target)
    """

    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        modulus = 1_000_000_007
        counts = [0] * (target + 1)
        counts[0] = 1
        for _ in range(n):
            following = [0] * (target + 1)
            for total, count in enumerate(counts):
                if not count:
                    continue
                for face in range(1, min(k, target - total) + 1):
                    following[total + face] = (following[total + face] + count) % modulus
            counts = following
        return counts[target]
