"""
## Task

Send exactly half of the people to city A and half to city B, minimizing total travel cost. Each
person provides [costA,costB].

## Hints

1. Start by sending everyone to one city and compare the cost difference of switching.
2. A prefix DP can track how many A slots have been filled.

## Approach

### Sort by A-minus-B cost difference

Sort people by costA-costB. Send the first half to A and the remainder to B.

### City-capacity prefix dynamic programming

Process people in order. Store the minimum cost for each possible number assigned to A,
rejecting transitions exceeding either city capacity.

## Why it works

### Sort by A-minus-B cost difference

Relative to an all-B assignment, choosing A changes the total by costA-costB. Exactly half must
switch, so selecting the smallest differences minimizes the sum; exchanging any inverted pair
cannot increase cost.

### City-capacity prefix dynamic programming

Every assignment of a prefix ends by sending the last person to A or B. The state count
determines both used capacities, so minimizing the two legal predecessor transitions computes
exactly the optimal costs.

## Walkthrough

[[10,20],[30,200],[400,50],[30,20]] sends the first two people to A and the last two to B for
10+30+50+20=110.

## Cost and pitfalls

Sort by A-minus-B cost difference: O(n log n) time; O(n) space.

City-capacity prefix dynamic programming: O(n squared) time; O(n) space.

Inputs and nested pairs are unchanged. n denotes the total even number of people. Greedy
differences, rather than each person's cheapest absolute city cost, enforce the exact half-and-
half capacity.
"""


class Solution:
    """Approach: Sort by A-minus-B cost difference
    Time: O(n log n)
    Space: O(n)
    """

    def twoCitySchedCost(self, costs: list[list[int]]) -> int:
        ordered = sorted(costs, key=lambda pair: pair[0] - pair[1])
        half = len(costs) // 2
        return sum(pair[0] if i < half else pair[1] for i, pair in enumerate(ordered))


class CapacityDPSolution:
    """Approach: City-capacity prefix dynamic programming
    Time: O(n squared)
    Space: O(n)
    """

    def twoCitySchedCost(self, costs: list[list[int]]) -> int:
        half = len(costs) // 2
        previous = [0] + [float("inf")] * half
        for processed, (first, second) in enumerate(costs, 1):
            current = [float("inf")] * (half + 1)
            for count in range(min(half, processed) + 1):
                if count and processed - count <= half:
                    current[count] = min(current[count], previous[count - 1] + first)
                if processed - count <= half:
                    current[count] = min(current[count], previous[count] + second)
            previous = current
        return int(previous[half])
