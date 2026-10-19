"""
## Task

Return the sum of two signed integers without using addition or subtraction operators. Inputs
lie within -1000..1000.

## Hints

1. XOR adds without carrying; AND identifies carry sources.
2. Mask Python integers to a fixed-width two's-complement representation.

## Approach

### Parallel carry propagation

Repeatedly compute XOR partial sums and shifted AND carries under a 32-bit mask. Decode the
final sign bit.

### Bit-by-bit full adder

Process 32 positions with a one-bit carry. A full-adder truth table gives the sum bit and
outgoing carry.

## Why it works

### Parallel carry propagation

For every bit, XOR plus the shifted carry represents the same total value modulo 2^32. Carry
bits move left each iteration and eventually vanish; the promised sum fits the decoded signed
range.

### Bit-by-bit full adder

The sum bit is x XOR y XOR carry, and a carry exists when at least two input bits are set.
Induction over bit positions reproduces binary addition without arithmetic plus or minus.

## Walkthrough

1 and 3 first produce XOR 2 and carry 2; the next rounds move the carry and settle at binary
100, or 4.

## Cost and pitfalls

Parallel carry propagation: O(W) worst case time; O(1) space.

Bit-by-bit full adder: O(W) time; O(1) space.

Inputs are unchanged. W=32. Python negative integers have unbounded sign extension; omitting the
mask from parallel carry propagation can prevent termination.
"""


class Solution:
    """Approach: Parallel carry propagation
    Time: O(W) worst case
    Space: O(1)
    """

    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        a &= mask
        b &= mask
        while b:
            a, b = (a ^ b) & mask, ((a & b) << 1) & mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)


class RippleCarrySolution:
    """Approach: Bit-by-bit full adder
    Time: O(W)
    Space: O(1)
    """

    def getSum(self, a: int, b: int) -> int:
        answer = carry = 0
        for bit in range(32):
            x, y = (a >> bit) & 1, (b >> bit) & 1
            answer |= (x ^ y ^ carry) << bit
            carry = (x & y) | (x & carry) | (y & carry)
        return answer if answer <= 0x7FFFFFFF else ~(answer ^ 0xFFFFFFFF)
