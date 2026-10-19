"""
## Task

Return the greatest nonnegative integer at most n whose decimal digits are nondecreasing from
left to right.

## Hints

1. When a digit decreases, reduce an earlier digit and maximize the remaining suffix.
2. Digit DP can instead construct the best number under the upper bound.

## Approach

### Right-to-left decrement and nine suffix

Scan digits right to left. On a descent, decrement the preceding digit and mark the later suffix
for replacement by nines.

### Memoized upper-bound digit construction

Use states (position,previous_digit,tight). Try next digits from largest to smallest while
respecting nondecreasing order and the bound; retain the first feasible suffix.

## Why it works

### Right-to-left decrement and nine suffix

At a descent, keeping the earlier prefix unchanged cannot produce a legal suffix. Reducing the
latest possible offending digit gives the smallest necessary decrease; filling everything after
it with nines maximizes the result. Right-to-left scanning propagates any new descent.

### Memoized upper-bound digit construction

The state captures every constraint on a suffix. Descending candidate order chooses the largest
feasible first differing digit, and recursively optimal suffixes complete the greatest valid
number. Leading zeroes represent shorter numbers without a separate case.

## Walkthrough

332 first reduces the second 3, exposing a new descent at the first 3. Reducing that as well and
filling the suffix with nines yields 299.

## Cost and pitfalls

Right-to-left decrement and nine suffix: O(L) time; O(L) space.

Memoized upper-bound digit construction: O(100L) time; O(10L) space.

Input is unchanged. L is decimal digit count, at most 10 under the bound. Digit DP recursion is
therefore shallow. Converting a leading-zero result to an integer gives its canonical numeric
form.
"""

from functools import cache


class Solution:
    """Approach: Right-to-left decrement and nine suffix
    Time: O(L)
    Space: O(L)
    """

    def monotoneIncreasingDigits(self, n: int) -> int:
        digits = list(str(n))
        boundary = len(digits)
        for i in range(len(digits) - 1, 0, -1):
            if digits[i] < digits[i - 1]:
                digits[i - 1] = str(int(digits[i - 1]) - 1)
                boundary = i
        for i in range(boundary, len(digits)):
            digits[i] = "9"
        return int("".join(digits))


class DigitDPSolution:
    """Approach: Memoized upper-bound digit construction
    Time: O(100L)
    Space: O(10L)
    """

    def monotoneIncreasingDigits(self, n: int) -> int:
        digits = tuple(map(int, str(n)))

        @cache
        def build(position, previous, tight):
            if position == len(digits):
                return 0
            limit = digits[position] if tight else 9
            for digit in range(limit, previous - 1, -1):
                suffix = build(position + 1, digit, tight and digit == limit)
                if suffix is not None:
                    return digit * 10 ** (len(digits) - position - 1) + suffix
            return None

        return build(0, 0, True)
