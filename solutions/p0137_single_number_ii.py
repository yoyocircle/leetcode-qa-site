"""
## Task

Every signed 32-bit integer appears three times except one appearing once. Find that unique
integer in linear time with constant auxiliary storage.

## Hints

1. Track each bit's count modulo three.
2. Two bit masks can represent the one-seen and two-seen states.

## Approach

### Two-mask modulo-three state machine

Update masks of bits seen once and twice, clearing bits when their third occurrence arrives.

### Count each of 32 bits

Sum each bit over all values modulo three and reconstruct an unsigned 32-bit result, then
convert its sign.

## Why it works

### Two-mask modulo-three state machine

For each bit, the mask transitions cycle through counts 0,1,2,0. Tripled values contribute zero
modulo three, leaving exactly the unique value's bits in the once mask.

### Count each of 32 bits

Each repeated value contributes a multiple of three at every bit. The residues are therefore the
unique value's two's-complement bits; subtracting 2^32 for a set sign bit recovers the signed
value.

## Walkthrough

[2,2,3,2] leaves the bits of 3 after modulo-three cancellation. [-2,-2,-2,-7] must reconstruct
-7, not its unsigned encoding.

## Cost and pitfalls

Two-mask modulo-three state machine: O(n) time; O(1) space.

Count each of 32 bits: O(32n) time; O(1) space.

Inputs are unchanged. The state-machine update order matters: twice uses the new once mask. The
explicit bit-count method must restore the signed interpretation.
"""


class Solution:
    """Approach: Two-mask modulo-three state machine
    Time: O(n)
    Space: O(1)
    """

    def singleNumber(self, nums: list[int]) -> int:
        once = twice = 0
        for value in nums:
            once = (once ^ value) & ~twice
            twice = (twice ^ value) & ~once
        return once


class BitCountSolution:
    """Approach: Count each of 32 bits
    Time: O(32n)
    Space: O(1)
    """

    def singleNumber(self, nums: list[int]) -> int:
        answer = 0
        for bit in range(32):
            if sum((value >> bit) & 1 for value in nums) % 3:
                answer |= 1 << bit
        return answer - (1 << 32) if answer & (1 << 31) else answer
