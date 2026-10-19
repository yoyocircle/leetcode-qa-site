"""## Task

Maximize profit with at most two stock transactions. Each transaction buys
before selling, and you must sell a held share before buying another.
Choosing no transactions yields zero profit.

## Hints

1. Track cash after a first buy, first sell, second buy, and second sell.
2. Each state either persists or advances from the previous day's preceding state.

## Approach

### Four cash-balance states

Maintain four best cash balances. Initialize sell states to zero and buy
states to negative infinity, representing no share held versus impossible
holding states before any day. For each price, update in reverse transaction
order: second sell, second buy, first sell, first buy. Each transition
therefore reads the preceding day's state. Buying subtracts the price;
selling adds it. The second sell state is the answer.

### Best single trade on each side

Compute the best one-transaction profit for every prefix. Scan backward while maintaining
the best one-transaction suffix profit and combine the prefix/suffix at every split day.

## Why it works

### Four cash-balance states

Every valid action sequence follows the order buy, sell, buy, sell, with
optional actions omitted by the at-most-two budget. A state's best balance
either comes from taking no action today or from the preceding state plus
today's buy or sell. These exhaust all legal transitions. Zero sell-state
initialization also permits fewer transactions, and maximizing balances at
every stage preserves all future profit possibilities.

### Best single trade on each side

Any two nonoverlapping trades have a split between them. Prefix and suffix optima dominate
those two trades, while each combined pair remains legal. Sharing the split day permits
selling then buying at the same price without improving beyond valid distinct-day schedules.

## Walkthrough

For [3,1,4,2,5], buy at 1 and sell at 4 for profit 3, then buy at 2
and sell at 5 for another 3. The final best balance is 6.

## Cost and pitfalls

For the default Four cash-balance states approach:

O(n) time and O(1) space; input is unchanged. Update backward if the
recurrence uses previous-day states. Selecting the two largest individual
price rises can produce overlapping transactions. Holding-state balances
include purchase cost; they are not realized profits.

Four cash-balance states: O(n) time; O(1) space.
Best single trade on each side: O(n) time; O(n) space.
The split table uses more memory but separates the two transactions visibly. Neither method
sorts or changes the price sequence.
"""


class Solution:
    """Approach: Four cash-balance states
    Time: O(n)
    Space: O(1)
    """

    def maxProfit(self, prices: list[int]) -> int:
        buy1 = buy2 = -float("inf")
        sell1 = sell2 = 0
        for price in prices:
            sell2 = max(sell2, buy2 + price)
            buy2 = max(buy2, sell1 - price)
            sell1 = max(sell1, buy1 + price)
            buy1 = max(buy1, -price)
        return sell2


class SplitSolution:
    """Approach: Best single trade on each side
    Time: O(n)
    Space: O(n)
    """

    def maxProfit(self, prices: list[int]) -> int:
        left = [0] * len(prices)
        minimum = prices[0]
        for index, price in enumerate(prices):
            minimum = min(minimum, price)
            left[index] = max(left[index - 1] if index else 0, price - minimum)
        maximum = prices[-1]
        right = answer = 0
        for index in range(len(prices) - 1, -1, -1):
            maximum = max(maximum, prices[index])
            right = max(right, maximum - prices[index])
            answer = max(answer, left[index] + right)
        return answer
