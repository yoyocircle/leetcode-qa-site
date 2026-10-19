"""## Task

Repeatedly smash two stones, leaving their absolute weight difference; minimize the final
remaining weight, with zero when none remain.

## Hints

1. A final result is the difference between two groups of original stone weights.
2. The best group sum lies as close as possible to half the total.

## Approach

### Subset-sum bitset near half total

Mark all subset sums up to half total in a Python integer bitset. Its highest set bit is the
best achievable smaller-side weight.

### Meet-in-the-middle subset sums

Enumerate subset sums independently in each index half. Sort one half and binary-search the
largest partner fitting the half-total target for every sum in the other.

## Why it works

### Subset-sum bitset near half total

Every smash subtracts the signed contributions of two groups, and an optimal
minimum-difference partition can be realized by repeatedly smashing stones from opposite
groups; a smaller final difference would contradict optimality. Thus maximizing a subset no
larger than half solves the game.

### Meet-in-the-middle subset sums

Every full subset splits uniquely across the two halves. The binary-search partner is the
greatest feasible sum for its fixed first-half choice, so maximizing over those choices
finds the optimal partition.

## Walkthrough

For [2,7,4,1,8,1], two groups can differ by 1, which is the minimum final weight.

## Cost and pitfalls

Subset-sum bitset near half total: O(n*S/w) machine-word work time; O(S/w) machine words space.
Meet-in-the-middle subset sums: O(n*2^(n/2)) time; O(2^(n/2)) space.

S is total weight+1, w the integer word width, and n<=30. Both preserve stones. Bit shifts
process multiple machine words rather than costing O(1); meet-in-the-middle avoids
dependence on weight magnitude but allocates exponential lists and temporary comprehensions.
"""


class Solution:
    """Approach: Subset-sum bitset near half total
    Time: O(n*S/w) machine-word work
    Space: O(S/w) machine words
    """

    def lastStoneWeightII(self, stones: list[int]) -> int:
        total = sum(stones)
        target = total // 2
        reachable = 1
        limit = (1 << (target + 1)) - 1
        for stone in stones:
            reachable = (reachable | (reachable << stone)) & limit
        best = reachable.bit_length() - 1
        return total - 2 * best


class MeetMiddleSolution:
    """Approach: Meet-in-the-middle subset sums
    Time: O(n*2^(n/2))
    Space: O(2^(n/2))
    """

    def lastStoneWeightII(self, stones: list[int]) -> int:
        from bisect import bisect_right

        middle = len(stones) // 2
        first = [0]
        for index in range(middle):
            first += [total + stones[index] for total in first]
        second = [0]
        for index in range(middle, len(stones)):
            second += [total + stones[index] for total in second]
        second.sort()
        total = sum(stones)
        target, best = total // 2, 0
        for subtotal in first:
            index = bisect_right(second, target - subtotal) - 1
            if index >= 0:
                best = max(best, subtotal + second[index])
        return total - 2 * best
