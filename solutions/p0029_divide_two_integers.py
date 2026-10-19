"""
## Task

Divide two signed 32-bit integers without multiplication, division, or modulo. Truncate toward
zero and clamp overflow to the signed 32-bit range.

## Hints

1. Subtract powers-of-two multiples of the divisor.
2. Apply the sign after dividing absolute values.

## Approach

### Repeated largest doubled subtraction

For each remainder, repeatedly double the divisor until the next doubling would exceed it, then
subtract that block and add its quotient bit.

### Binary long division

Scan candidate quotient bits from highest to lowest and subtract a shifted divisor whenever it
fits.

## Why it works

### Repeated largest doubled subtraction

Each subtraction preserves original_dividend = quotient*divisor + remainder. The remainder
decreases by at least half when a largest fitting power-of-two block is removed, until it is
smaller than the divisor.

### Binary long division

Before each bit, all higher quotient bits are settled and the remaining value is below the next
higher divisor multiple. Setting the current bit exactly when its multiple fits reproduces
integer long division.

## Walkthrough

-7 divided by 3 computes magnitude quotient 2 and then negates it, yielding -2 rather than floor
result -3. -2^31 divided by -1 clamps to 2^31-1.

## Cost and pitfalls

Repeated largest doubled subtraction: O(log squared V) time; O(1) space.

Binary long division: O(log V) time; O(1) space.

Inputs are unchanged; divisor is nonzero. V is the dividend magnitude plus one. All divisions in
these implementations use only shifts and subtraction.
"""


class Solution:
    """Approach: Repeated largest doubled subtraction
    Time: O(log squared V)
    Space: O(1)
    """

    def divide(self, dividend: int, divisor: int) -> int:
        negative = (dividend < 0) != (divisor < 0)
        remaining, base = abs(dividend), abs(divisor)
        quotient = 0
        while remaining >= base:
            chunk, count = base, 1
            while chunk << 1 <= remaining:
                chunk <<= 1
                count <<= 1
            remaining -= chunk
            quotient += count
        if negative:
            quotient = -quotient
        return min((1 << 31) - 1, max(-(1 << 31), quotient))


class LongDivisionSolution:
    """Approach: Binary long division
    Time: O(log V)
    Space: O(1)
    """

    def divide(self, dividend: int, divisor: int) -> int:
        remaining, base = abs(dividend), abs(divisor)
        quotient = 0
        for bit in range(remaining.bit_length() - 1, -1, -1):
            if base << bit <= remaining:
                remaining -= base << bit
                quotient |= 1 << bit
        if (dividend < 0) != (divisor < 0):
            quotient = -quotient
        return min((1 << 31) - 1, max(-(1 << 31), quotient))
