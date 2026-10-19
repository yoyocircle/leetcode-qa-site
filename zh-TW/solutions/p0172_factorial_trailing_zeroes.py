"""
## Task

Return the number of trailing decimal zeroes in n factorial, for nonnegative n, without
constructing the factorial.

## Hints

1. Every trailing zero consumes a factor 2 and a factor 5.
2. Factors of 5 are scarcer; multiples of 25 contribute an extra one.

## Approach

### Repeated division by five

Sum floor(n/5), floor(n/25), and further powers by repeatedly dividing n by five.

### Count factors in multiples of five

Visit each multiple of five and divide out every factor of five. This direct educational
baseline may time out for very large n.

## Why it works

### Repeated division by five

Every multiple of 5 contributes one factor, every multiple of 25 another, and so on. This counts
every factor of 5 exactly once per multiplicity; enough factors of 2 always exist to pair them.

### Count factors in multiples of five

Integers not divisible by five contribute no factors of five. For each remaining integer,
repeated exact division counts its full multiplicity, so the summed count is the factorial's
five-adic exponent.

## Walkthrough

25! has floor(25/5)=5 ordinary factors of five plus floor(25/25)=1 extra, so it ends in six
zeroes.

## Cost and pitfalls

Repeated division by five: O(log(n+1)) time; O(1) space.

Count factors in multiples of five: O(n log(n+1)) conservative bound time; O(1) space.

Input is unchanged. 0! is 1 and has no trailing zero. Counting multiples of ten alone misses
factors paired across different factorial terms.
"""


class Solution:
    """Approach: Repeated division by five
    Time: O(log(n+1))
    Space: O(1)
    """

    def trailingZeroes(self, n: int) -> int:
        answer = 0
        while n:
            n //= 5
            answer += n
        return answer


class FactorEnumerationSolution:
    """Approach: Count factors in multiples of five
    Time: O(n log(n+1)) conservative bound
    Space: O(1)
    """

    def trailingZeroes(self, n: int) -> int:
        answer = 0
        for multiple in range(5, n + 1, 5):
            value = multiple
            while value % 5 == 0:
                answer += 1
                value //= 5
        return answer
