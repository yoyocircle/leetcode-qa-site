"""## Task

Count integers x with 0 <= x < 10^n whose decimal digits are all distinct.

## Hints

1. Count separately by the number of significant digits.
2. Leading zeroes in a fixed-width representation are padding, not used digits.

## Approach

### Count by significant length

Count zero once. For each positive length, choose a nonzero first digit in nine ways, then
choose each following digit from unused digits.

### Digit-mask DP with leading padding

Construct n positions using a digit-used mask and a started flag. Leading zeroes keep the
not-started state; after starting, every digit must be unused.

## Why it works

### Count by significant length

A length-k positive number has a unique sequence of digit choices. The first position
forbids zero; later positions forbid precisely the digits already used. Summing disjoint
lengths counts every valid integer once.

### Digit-mask DP with leading padding

Each integer below 10^n has one padded representation. Padding does not consume zero, and
all significant digits consume distinct bits, giving a one-to-one correspondence between
accepted DP paths and valid integers.

## Walkthrough

For n=2, all 10 one-digit values count, and 9*9 two-digit values count, giving 91.

## Cost and pitfalls

Count by significant length: O(min(n,10)) time; O(1) space.
Digit-mask DP with leading padding: O(n*10*2^10) time; O(2^10) space.

Both preserve n and return one when n=0. More than ten significant digits cannot be unique.
The combinatorial default avoids the larger mask frontier; Python integers store exact
counts.
"""


class Solution:
    """Approach: Count by significant length
    Time: O(min(n,10))
    Space: O(1)
    """

    def countNumbersWithUniqueDigits(self, n: int) -> int:
        answer = 1
        ways = 9
        for length in range(1, min(n, 10) + 1):
            if length > 1:
                ways *= 11 - length
            answer += ways
        return answer


class DigitDPSolution:
    """Approach: Digit-mask DP with leading padding
    Time: O(n*10*2^10)
    Space: O(2^10)
    """

    def countNumbersWithUniqueDigits(self, n: int) -> int:
        counts = {(0, False): 1}
        for _ in range(n):
            following = {}
            for (mask, started), count in counts.items():
                for digit in range(10):
                    if not started and digit == 0:
                        state = (0, False)
                    elif mask & (1 << digit):
                        continue
                    else:
                        state = (mask | (1 << digit), True)
                    following[state] = following.get(state, 0) + count
            counts = following
        return sum(counts.values())
