"""
## Task

Each token may be used at most once: pay its value in power for one score, or spend one score to
gain its value in power. Return the greatest score reached.

## Hints

1. Buy the cheapest remaining token and sell the most expensive when extra power is needed.
2. An offline formulation can enumerate how many largest tokens are sold.

## Approach

### Sorted buy-low sell-high pointers

Sort a copy. Buy the lightest affordable token; otherwise, if a sale can still help, sell the
largest token. Record the greatest score before any later sale.

### Sale-count enumeration with prefix budgets

Sort tokens and build prefix sums. For each number d of sold largest tokens, binary-search how
many disjoint smallest tokens their total power can buy, maximizing bought-d.

## Why it works

### Sorted buy-low sell-high pointers

Buying a cheaper token produces the same score with at least as much remaining power; selling a
larger token produces at least as much power for the same lost score. These exchanges preserve
an optimal sequence while the pointers make those choices.

### Sale-count enumeration with prefix budgets

Any plan with b buys and d sales is improved by choosing the b smallest and d largest disjoint
tokens. For positive final score, b>d. If the first smallest token is affordable, execute one
buy before each sale; each largest sale funds the next smallest buy, and the aggregate budget
then funds all remaining buys. Thus the prefix-budget inequality is both necessary and
sufficient for every candidate improving the answer.

## Walkthrough

[100,200,300,400], power=200 buys 100, sells 400, then buys 200 and 300 for a best score of 2.
The offline plan sells one token and buys three.

## Cost and pitfalls

Sorted buy-low sell-high pointers: O(n log n) time; O(n) space.

Sale-count enumeration with prefix budgets: O(n log n) time; O(n) space.

Inputs are unchanged. Empty token lists return zero. Buying zero-valued tokens is permitted. A
final sale cannot improve the maximum score, which is why only plans with more buys than sales
need examination.
"""

from bisect import bisect_right


class Solution:
    """Approach: Sorted buy-low sell-high pointers
    Time: O(n log n)
    Space: O(n)
    """

    def bagOfTokensScore(self, tokens: list[int], power: int) -> int:
        values = sorted(tokens)
        left, right = 0, len(values) - 1
        score = best = 0
        while left <= right:
            if power >= values[left]:
                power -= values[left]
                left += 1
                score += 1
                best = max(best, score)
            elif score and left < right:
                power += values[right]
                right -= 1
                score -= 1
            else:
                break
        return best


class PrefixBudgetSolution:
    """Approach: Sale-count enumeration with prefix budgets
    Time: O(n log n)
    Space: O(n)
    """

    def bagOfTokensScore(self, tokens: list[int], power: int) -> int:
        values = sorted(tokens)
        if not values or power < values[0]:
            return 0
        prefix = [0]
        for value in values:
            prefix.append(prefix[-1] + value)
        best = sold_power = 0
        for sold in range((len(values) - 1) // 2 + 1):
            if sold:
                sold_power += values[-sold]
            bought = bisect_right(prefix, power + sold_power, 0, len(values) - sold + 1) - 1
            best = max(best, bought - sold)
        return best
