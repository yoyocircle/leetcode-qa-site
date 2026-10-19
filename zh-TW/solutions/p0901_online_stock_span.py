"""
## Task

For each next(price), return the number of consecutive days ending today whose prices are at
most today's price. Prices are in 1..100000.

## Hints

1. A previous larger price is the boundary of the span.
2. Merge consecutive dominated days into one summarized block.

## Approach

### Monotonic price-span stack

Store decreasing prices with the spans they summarize. Pop and absorb all blocks whose price is
at most the incoming price.

### Fenwick maximum over reversed prices

Reverse the bounded price coordinate. A Fenwick tree stores the latest day for prices strictly
greater than the current price; subtract that day from today.

## Why it works

### Monotonic price-span stack

Every popped block consists entirely of prices bounded by its maximum, which the incoming price
dominates. The first surviving larger price stops the span, so the absorbed lengths plus today
are exact.

### Fenwick maximum over reversed prices

The prefix query covers exactly greater prices and returns their greatest day index, the nearest
larger-price blocker. All later days are at most today's price, so their count is the span.

## Walkthrough

Prices [100,80,60,70,60,75,85] return [1,1,1,2,1,4,6]. Equal prices are absorbed into the span.

## Cost and pitfalls

Monotonic price-span stack: O(1) amortized per next time; O(n) space.

Fenwick maximum over reversed prices: O(log P) per next time; O(P) space.

The object owns its price history; next mutates only that object. P=100000 is the promised price
bound. The tree pays fixed storage even for a short history.
"""


class StockSpanner:
    """Approach: Monotonic price-span stack
    Time: O(1) amortized per next
    Space: O(n)
    """

    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span


class FenwickStockSpanner:
    """Approach: Fenwick maximum over reversed prices
    Time: O(log P) per next
    Space: O(P)
    """

    def __init__(self):
        self.latest = [0] * 100001
        self.day = 0

    def next(self, price: int) -> int:
        self.day += 1
        coordinate = 100001 - price
        index, blocker = coordinate - 1, 0
        while index:
            blocker = max(blocker, self.latest[index])
            index -= index & -index
        index = coordinate
        while index < len(self.latest):
            self.latest[index] = max(self.latest[index], self.day)
            index += index & -index
        return self.day - blocker
