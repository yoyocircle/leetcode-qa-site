"""## Task

Maximize money taken from nonnegative-valued houses arranged in a circle.
Adjacent houses cannot both be chosen, including the first and last houses.

## Hints

1. A legal selection must omit at least one endpoint of the array.
2. Omitting either endpoint leaves an ordinary linear House Robber problem.

## Approach

### Two rolling index ranges

Handle one house directly because it is not its own neighbor. For longer
arrays, solve the half-open index ranges [0,n-1) and [1,n), then return the
larger total. Within each range, maintain the best totals for the previous
one and two prefixes. A new house either extends the older optimum or is
skipped. Pass range boundaries to a helper so neither case copies a slice.

### Condition on the first house

Run a take/skip state machine twice, fixing whether the first house was selected. In the
selected case, disable taking the last house. Impossible states start at negative infinity.

## Why it works

### Two rolling index ranges

Any valid selection excludes the first house, the last house, or both.
Consequently it belongs to at least one of the two linear subproblems.
Every selection from either subproblem is also legal in the circle because
one endpoint is absent. The maximum of their optima therefore equals the
circle's optimum. The linear recurrence checks both take and skip choices.

### Condition on the first house

Each run enumerates exactly selections with its fixed first-house decision. Take extends
only a skipped predecessor, and skip preserves either predecessor. The final prohibition
enforces the circular edge.

## Walkthrough

For [5,1,2,6], excluding the last house gives 7 from 5+2. Excluding the
first gives 7 from 1+6. Taking 5+6 is forbidden, so the answer is 7.

## Cost and pitfalls

For the default Two rolling index ranges approach:

O(n) time and O(1) auxiliary space; input is unchanged. Array slicing would
add O(n) allocation without helping the recurrence. The single-house case
must precede the two endpoint-exclusion cases, which would otherwise omit it.

Two rolling index ranges: O(n) time; O(1) space.
Condition on the first house: O(n) time; O(1) space.
The state model exposes the circular constraint directly; the range model reuses the linear
recurrence. Both avoid slices and preserve input.
"""


class Solution:
    """Approach: Two rolling index ranges
    Time: O(n)
    Space: O(1)
    """

    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_range(start: int, end: int) -> int:
            older = previous = 0
            for index in range(start, end):
                older, previous = previous, max(previous, older + nums[index])
            return previous

        return max(rob_range(0, len(nums) - 1), rob_range(1, len(nums)))


class StateSolution:
    """Approach: Condition on the first house
    Time: O(n)
    Space: O(1)
    """

    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def run(first_taken):
            skip = 0 if not first_taken else -float("inf")
            take = nums[0] if first_taken else -float("inf")
            for index in range(1, len(nums)):
                next_take = skip + nums[index]
                if first_taken and index == len(nums) - 1:
                    next_take = -float("inf")
                skip, take = max(skip, take), next_take
            return max(skip, take)

        return max(run(False), run(True))
