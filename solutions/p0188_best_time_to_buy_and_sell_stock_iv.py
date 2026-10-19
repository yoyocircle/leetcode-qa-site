"""## Task

Maximize stock profit with at most k nonoverlapping buy/sell transactions.

## Hints

1. Cash states track completed sales and whether a share is held.
2. For each sale day, retain the best earlier buy balance for that transaction count.

## Approach

### Transaction-indexed cash states

Use buy/sell arrays indexed by transaction budget and update budgets backward. If the budget
permits every profitable adjacent rise, use the unlimited-transactions shortcut.

### Transaction rows and best prior purchase

Add one transaction-budget row at a time. Retain the greatest previous-row profit before a
purchase minus its price, then consider selling today.

## Why it works

### Transaction-indexed cash states

A state either waits or takes its next legal buy/sell action. Backward order reads
previous-day smaller-budget states. With a nonbinding budget, summing positive adjacent
changes equals buying at each valley and selling at its peak.

### Transaction rows and best prior purchase

Any final sale today pairs with some earlier purchase after at most one fewer transaction.
The best-buy accumulator maximizes all such candidates; waiting preserves the earlier
same-row optimum.

## Walkthrough

With k=2 and prices [2,4,1,5], buy/sell twice for profit 2+4=6.

## Cost and pitfalls

Transaction-indexed cash states: O(n*min(k,n)) time; O(min(k,n)) space.
Transaction rows and best prior purchase: O(n*min(k,n)) time; O(n) space.

Inputs are unchanged. The first variant stores transaction states, the second day-prefix
states. Zero budget and a single price yield zero; empty prices are handled as well.
"""


class Solution:
    """Approach: Transaction-indexed cash states
    Time: O(n*min(k,n))
    Space: O(min(k,n))
    """

    def maxProfit(self, k: int, prices: list[int]) -> int:
        if k >= len(prices) // 2:
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
        buy = [-float("inf")] * (k + 1)
        sell = [0] * (k + 1)
        for price in prices:
            for count in range(k, 0, -1):
                sell[count] = max(sell[count], buy[count] + price)
                buy[count] = max(buy[count], sell[count - 1] - price)
        return sell[k]


class TableSolution:
    """Approach: Transaction rows and best prior purchase
    Time: O(n*min(k,n))
    Space: O(n)
    """

    def maxProfit(self, k: int, prices: list[int]) -> int:
        if not prices:
            return 0
        previous = [0] * len(prices)
        for _ in range(min(k, len(prices) // 2)):
            current = [0] * len(prices)
            best_buy = -prices[0]
            for day in range(1, len(prices)):
                current[day] = max(current[day - 1], prices[day] + best_buy)
                best_buy = max(best_buy, previous[day - 1] - prices[day])
            previous = current
        return previous[-1]
