"""
## Task

In the digit sequence 123456789101112..., return the one-based nth digit without constructing
the whole prefix.

## Hints

1. There are 9*10^(d-1) d-digit positive integers.
2. After locating the width block, use quotient and remainder to select a number and digit.

## Approach

### Subtract complete digit-width blocks

Remove all digits belonging to shorter numbers, then index the containing number in the
remaining width block.

### Binary search containing integer

Binary-search the smallest integer x whose cumulative written digit count reaches n, then locate
n inside x.

## Why it works

### Subtract complete digit-width blocks

Each removed block has exactly width*count digits. Once n lies in the current block, zero-based
offset n-1 splits uniquely into a number offset and an in-number digit index.

### Binary search containing integer

The cumulative digit count is strictly increasing. Its lower bound is exactly the integer
containing the nth digit, and subtracting the preceding cumulative count yields the digit's one-
based offset.

## Walkthrough

n=11 skips the nine one-digit numbers, leaving offset 2 in the two-digit block. Number 10
contains that position, and its second digit is 0.

## Cost and pitfalls

Subtract complete digit-width blocks: O(log n) time; O(log n) for decimal conversion space.

Binary search containing integer: O(log squared n) time; O(log n) space.

Input is unchanged. n is one-based; use n-1 before division. Python decimal string conversion
costs space proportional to the selected number's digit length.
"""


class Solution:
    """Approach: Subtract complete digit-width blocks
    Time: O(log n)
    Space: O(log n) for decimal conversion
    """

    def findNthDigit(self, n: int) -> int:
        width, start, count = 1, 1, 9
        while n > width * count:
            n -= width * count
            width += 1
            start *= 10
            count *= 10
        number = start + (n - 1) // width
        return int(str(number)[(n - 1) % width])


class IntegerSearchSolution:
    """Approach: Binary search containing integer
    Time: O(log squared n)
    Space: O(log n)
    """

    def findNthDigit(self, n: int) -> int:
        def digits_through(value):
            total, start, width = 0, 1, 1
            while start <= value:
                end = min(value, start * 10 - 1)
                total += (end - start + 1) * width
                start *= 10
                width += 1
            return total

        low, high = 1, n
        while low < high:
            middle = (low + high) // 2
            if digits_through(middle) >= n:
                high = middle
            else:
                low = middle + 1
        offset = n - digits_through(low - 1) - 1
        return int(str(low)[offset])
