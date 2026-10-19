"""
## Task

For each daily temperature, return how many days pass before a strictly warmer
temperature. Use zero when no warmer future day exists.

## Hints

1. Keep days whose answer is still unknown.
2. A new warmer day can resolve several earlier days at once.

## Approach

### Unresolved-day stack

Maintain a stack of unresolved indices with nonincreasing temperatures. When a
warmer day arrives, pop every cooler top index and fill its waiting distance.
Push the current day after resolving those earlier days.

### Reverse jump pointers

Scan backward and jump through already-computed next-warmer links until a warmer day appears.
This avoids a separate stack, but its conservative quadratic worst-case bound may time out at
full constraints.

## Why it works

### Unresolved-day stack

An index stays unresolved until the first later day warmer than it arrives.
If such a day had appeared earlier, that index would already have been popped.
Thus every assigned distance is to the earliest valid warmer day.

### Reverse jump pointers

When a future day is not warmer, any days it skips before its own next warmer day are no warmer
than it and cannot answer the current query. Following its link preserves the first possible
answer.

## Walkthrough

For [60, 60, 65, 62], day 2 resolves days 1 and 0 with waits 1 and 2.
No warmer day follows days 2 or 3. Return [2, 1, 0, 0].

## Cost and pitfalls

Default approach (Unresolved-day stack):

O(n) time and O(n) auxiliary space, plus O(n) output. Every index is pushed
and popped at most once. Inputs are unchanged. Equal temperatures are not warmer,
so pop only on a strict increase. Store indices, since values alone do not give
waiting distances.

Unresolved-day stack: O(n) time; O(n) space.
Reverse jump pointers: O(n squared) worst case time; O(1) auxiliary, O(n) output space. Scan
backward and jump through already-computed next-warmer links until a warmer day appears. This
avoids a separate stack, but its conservative quadratic worst-case bound may time out at full
constraints.
"""


class Solution:
    """Approach: Unresolved-day stack
    Time: O(n)
    Space: O(n)
    """

    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        result = [0] * len(temperatures)
        waiting = []
        for day, temperature in enumerate(temperatures):
            while waiting and temperatures[waiting[-1]] < temperature:
                previous = waiting.pop()
                result[previous] = day - previous
            waiting.append(day)
        return result


class JumpSolution:
    """Approach: Reverse jump pointers
    Time: O(n squared) worst case
    Space: O(1) auxiliary, O(n) output
    """

    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        result = [0] * len(temperatures)
        for i in range(len(temperatures) - 2, -1, -1):
            j = i + 1
            while j < len(temperatures) and temperatures[j] <= temperatures[i]:
                if result[j] == 0:
                    j = len(temperatures)
                else:
                    j += result[j]
            if j < len(temperatures):
                result[i] = j - i
        return result
