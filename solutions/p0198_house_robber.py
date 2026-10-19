"""## Task

Choose houses on a street to maximize the money taken. Adjacent houses cannot
both be chosen. Values are nonnegative, and choosing no house earns zero.

## Hints

1. Separate solutions according to whether the last house is chosen.
2. Choosing it only requires the optimum from two positions earlier.

## Approach

### Rolling prefix optimum

Let F(k) be the best total using the first k houses. Initialize F(0)=0 and
the value before the first house to zero. For each amount, compute
max(F(k-1), F(k-2) + amount). Keep just the previous two totals; the entire
table is unnecessary. Update both values together so the old states remain
available for the transition.

### Explicit prefix table

Store every prefix optimum rather than only two adjacent states. Initialize the empty prefix
to zero and compare skipping each house with taking it after the prefix two positions
earlier.

## Why it works

### Rolling prefix optimum

Every legal choice either skips the current house or includes it. Skipping
leaves the optimum for the previous prefix. Including it forbids the previous
house and adds its amount to the optimum two houses back. These cases cover
every legal choice, so their maximum is optimal by induction on prefix length.

### Explicit prefix table

The two cases partition valid selections by whether the final house is used. Every table
entry therefore equals the optimum of its prefix; retaining entries also makes decisions
easier to inspect.

## Walkthrough

For [4,1,7,3], the best prefix totals are 4, 4, 11, and 11. Taking houses
with amounts 4 and 7 gives 11; adding the last house would conflict with 7.

## Cost and pitfalls

For the default Rolling prefix optimum approach:

O(n) time and O(1) auxiliary space; input is unchanged. Greedily taking the
larger amount from each adjacent pair loses information about later conflicts.
Do not overwrite the older total before computing the new total.

Rolling prefix optimum: O(n) time; O(1) space.
Explicit prefix table: O(n) time; O(n) space.
The table trades memory for visible intermediate states. Neither implementation changes the
amounts.
"""


class Solution:
    """Approach: Rolling prefix optimum
    Time: O(n)
    Space: O(1)
    """

    def rob(self, nums: list[int]) -> int:
        older = previous = 0
        for amount in nums:
            older, previous = previous, max(previous, older + amount)
        return previous


class TableSolution:
    """Approach: Explicit prefix table
    Time: O(n)
    Space: O(n)
    """

    def rob(self, nums: list[int]) -> int:
        best = [0] * (len(nums) + 1)
        for end, value in enumerate(nums, 1):
            best[end] = max(best[end - 1], value + (best[end - 2] if end > 1 else 0))
        return best[-1]
