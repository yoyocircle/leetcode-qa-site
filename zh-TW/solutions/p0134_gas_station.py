"""
## Task

A circular route has gas[i] fuel at station i and costs cost[i] to reach the next station.
Starting with an empty tank, return a feasible starting index or -1. A feasible answer is
promised unique.

## Hints

1. Total gas must cover total travel cost.
2. Any failed prefix invalidates every candidate start inside that prefix.

## Approach

### Reset after a failed segment

Accumulate total fuel balance and a candidate segment balance. Whenever the candidate balance
becomes negative, restart just after that station.

### Start after the minimum prefix balance

Locate the smallest cumulative gas-minus-cost prefix, including the empty prefix. If total
balance is nonnegative, start just after that minimum.

## Why it works

### Reset after a failed segment

If a segment from s fails at i, every later start within it has no more available prefix surplus
and also fails by i. Thus the reset discards only impossible starts. Nonnegative global total
guarantees the final candidate also survives the wraparound.

### Start after the minimum prefix balance

Every suffix prefix after the minimum has nonnegative relative balance. On the wrapped portion,
the original prefix minus the minimum is augmented by nonnegative total balance. Both parts
therefore keep the tank nonnegative.

## Walkthrough

[1,2,3,4,5] gas and [3,4,5,1,2] cost has balance [-2,-2,-2,3,3]. The minimum cumulative balance
ends at station 2, so start at 3.

## Cost and pitfalls

Reset after a failed segment: O(n) time; O(1) space.

Start after the minimum prefix balance: O(n) time; O(1) space.

Inputs are unchanged. The tank has no upper capacity bound. A negative total immediately rules
out every start, regardless of local rich stations.
"""


class Solution:
    """Approach: Reset after a failed segment
    Time: O(n)
    Space: O(1)
    """

    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        total = tank = start = 0
        for i, (supply, expense) in enumerate(zip(gas, cost, strict=True)):
            difference = supply - expense
            total += difference
            tank += difference
            if tank < 0:
                start = i + 1
                tank = 0
        return start if total >= 0 else -1


class MinimumPrefixSolution:
    """Approach: Start after the minimum prefix balance
    Time: O(n)
    Space: O(1)
    """

    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        prefix = minimum = 0
        start = 0
        for i in range(len(gas)):
            prefix += gas[i] - cost[i]
            if prefix < minimum:
                minimum = prefix
                start = i + 1
        return -1 if prefix < 0 else start % len(gas)
