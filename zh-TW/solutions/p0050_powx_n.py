"""
## Task

Compute x raised to signed integer n. n may be negative; zero is never raised to a nonpositive
power under the input contract.

## Hints

1. Square the base as the exponent is halved.
2. Invert x before processing a negative exponent.

## Approach

### Iterative binary exponentiation

Read exponent bits from least significant to most significant. Multiply the accumulator when a
bit is set and square the base every step.

### Recursive exponent halving

Recursively compute one half-power, square it, and multiply by x for odd exponents.

## Why it works

### Iterative binary exponentiation

The invariant answer*base^remaining equals the desired power. An odd step moves one base into
answer; squaring the base and halving the remaining exponent preserves the invariant.

### Recursive exponent halving

For n=2q, x^n=(x^q)^2; for n=2q+1, one additional x is needed. Induction on n proves the
recurrence, with x^0=1 as the base.

## Walkthrough

2^-3 first becomes (1/2)^3. The binary accumulator selects powers 1/2 and 1/4, giving 1/8.

## Cost and pitfalls

Iterative binary exponentiation: O(log(abs(n)+1)) time; O(1) space.

Recursive exponent halving: O(log(abs(n)+1)) time; O(log(abs(n)+1)) space.

Inputs are unchanged. Floating-point rounding is expected. Python can negate the minimum
signed-32-bit exponent without overflow.
"""


class Solution:
    """Approach: Iterative binary exponentiation
    Time: O(log(abs(n)+1))
    Space: O(1)
    """

    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n
        answer = 1.0
        while n:
            if n & 1:
                answer *= x
            x *= x
            n >>= 1
        return answer


class RecursiveSolution:
    """Approach: Recursive exponent halving
    Time: O(log(abs(n)+1))
    Space: O(log(abs(n)+1))
    """

    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n

        def power(exponent):
            if exponent == 0:
                return 1.0
            half = power(exponent // 2)
            answer = half * half
            return answer * x if exponent % 2 else answer

        return power(n)
