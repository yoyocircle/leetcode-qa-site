"""## Task

Maximize stock profit when selling forces one full day before another purchase.

## Hints

1. Distinguish holding, just sold, and resting states.
2. A purchase today may use only profit available two days earlier.

## Approach

### Three cooldown states

Holding may persist or buy from rest; a sale comes from holding; rest may persist or finish
yesterday's cooldown. Update all states simultaneously.

### Day-profit table with a two-day buy lag

Store best realized profits by day and maintain a holding balance. Buying on day i can use
realized profit only from day i-2 or earlier.

## Why it works

### Three cooldown states

The states classify every legal end-of-day status. Only rest permits buying, so a just-sold
share cannot be repurchased the following day. Every legal next action is represented.

### Day-profit table with a two-day buy lag

The lag excludes yesterday's sale from today's purchase. A realized optimum either waits or
sells the best legal holding state, covering all possibilities.

## Walkthrough

For [1,2,3,0,2], sell at 2, rest at 3, then buy at 0 and sell at 2 for total 3.

## Cost and pitfalls

Three cooldown states: O(n) time; O(1) space.
Day-profit table with a two-day buy lag: O(n) time; O(n) space.

Inputs are unchanged. Keep old states for the three-state update. An ordinary two-state
stock recurrence incorrectly permits purchases during cooldown.
"""


class Solution:
    """Approach: Three cooldown states
    Time: O(n)
    Space: O(1)
    """

    def maxProfit(self, prices: list[int]) -> int:
        hold, sold, rest = -float("inf"), -float("inf"), 0
        for price in prices:
            hold, sold, rest = max(hold, rest - price), hold + price, max(rest, sold)
        return max(sold, rest)


class TableSolution:
    """Approach: Day-profit table with a two-day buy lag
    Time: O(n)
    Space: O(n)
    """

    def maxProfit(self, prices: list[int]) -> int:
        profits = [0] * len(prices)
        hold = -prices[0]
        for day in range(1, len(prices)):
            profits[day] = max(profits[day - 1], hold + prices[day])
            hold = max(hold, (profits[day - 2] if day >= 2 else 0) - prices[day])
        return profits[-1]
