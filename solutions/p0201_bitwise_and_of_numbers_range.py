"""
## Task

Compute the bitwise AND of all integers in the inclusive nonnegative interval [left,right].

## Hints

1. Only the common leading bits can survive.
2. Clearing right's least significant set bit skips a block containing a zero in that bit.

## Approach

### Shift to common prefix

Shift both endpoints right until they match, then restore the removed positions as zeroes.

### Clear low set bits of right

Repeatedly replace right by right & (right-1) until it is no greater than left.

## Why it works

### Shift to common prefix

Above their highest differing bit, all interval values share the same prefix. At and below that
differing bit, the interval crosses a binary boundary that supplies zeroes, so no lower bit
survives the AND.

### Clear low set bits of right

Clearing the lowest set bit removes a suffix block whose interval AND already forces that bit
and all lower bits to zero. Repeating until the endpoint lies at or below left leaves exactly
the common surviving prefix.

## Walkthrough

For [5,7], binary endpoints 101 and 111 share prefix 1; the result is 100, or 4.

## Cost and pitfalls

Shift to common prefix: O(log(right+1)) time; O(1) space.

Clear low set bits of right: O(log(right+1)) time; O(1) space.

Inputs are unchanged. Zero is handled naturally. Iterating through every integer would be
impractical for wide intervals.
"""


class Solution:
    """Approach: Shift to common prefix
    Time: O(log(right+1))
    Space: O(1)
    """

    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        shift = 0
        while left < right:
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift


class ClearBitsSolution:
    """Approach: Clear low set bits of right
    Time: O(log(right+1))
    Space: O(1)
    """

    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        while right > left:
            right &= right - 1
        return right
