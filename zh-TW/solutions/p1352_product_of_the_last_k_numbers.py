"""## Task

Accept a stream of nonnegative integers and return the product of its last k numbers on request.
k never exceeds the number added.

## Hints

1. Prefix-product division works until a zero occurs.
2. A zero can discard all earlier prefix products because any query crossing it must return
   zero.

## Approach

### Prefix products since last zero

Keep prefix=[1] for the current nonzero suffix. Nonzero add appends its cumulative product; zero
resets it. A query longer than the suffix returns zero, otherwise divide two exact prefix
products.

### Stored stream and direct multiplication

Append each value and multiply the requested suffix from newest backward, stopping when its
product reaches zero.

## Why it works

### Prefix products since last zero

Within a nonzero suffix division cancels the earlier factors exactly. Crossing its preceding
zero forces product zero, so no pre-zero numeric history is needed.

### Stored stream and direct multiplication

The loop multiplies exactly the last k stored entries. Early stopping after zero preserves the
final product because any remaining factors keep it zero.

## Walkthrough

After adding 3,0,2,5, getProduct(2) returns 10 and getProduct(3) returns 0. A later add(4) makes
getProduct(3)=40.

## Cost and pitfalls

Prefix products since last zero: O(1) amortized add; O(1) getProduct under bounded products
time; O(n) space.
Stored stream and direct multiplication: O(1) amortized add; O(k) getProduct; may time out time;
O(n) space.
Objects own their state. Python clearing a long prefix on zero can take linear time for that
call, but each stored prefix is discarded once, giving amortized constant add. Numeric costs use
the official bounded contiguous-product guarantee. The scanning baseline misses the
constant-time follow-up.
"""


class ProductOfNumbers:
    """Approach: Prefix products since last zero
    Time: O(1) amortized add; O(1) getProduct under bounded products
    Space: O(n)
    """

    def __init__(self):
        self.prefix = [1]

    def add(self, num: int) -> None:
        if num == 0:
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):
            return 0
        return self.prefix[-1] // self.prefix[-k - 1]


class ScanningProductOfNumbers:
    """Approach: Stored stream and direct multiplication
    Time: O(1) amortized add; O(k) getProduct; may time out
    Space: O(n)
    """

    def __init__(self):
        self.values = []

    def add(self, num: int) -> None:
        self.values.append(num)

    def getProduct(self, k: int) -> int:
        result = 1
        for index in range(len(self.values) - 1, len(self.values) - k - 1, -1):
            result *= self.values[index]
            if result == 0:
                break
        return result
