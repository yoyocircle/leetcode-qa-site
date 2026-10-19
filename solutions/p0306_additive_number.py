"""## Task

Decide whether a digit string can be split into at least three numbers where each number after
the first two equals their sum. Multi-digit numbers cannot start with zero.

## Hints

1. Only the first two numbers are choices; the rest are forced.
2. Compare each forced sum directly against the next string prefix.

## Approach

### Integer seed-pair enumeration

Choose both initial cut positions, rejecting leading zeros. Repeatedly compute the next integer
sum and match its decimal string until the whole input is consumed.

### Decimal-string seed verification

Use the same seed choices but add decimal strings right to left with a carry. This avoids
parsing whole numbers and makes digit arithmetic explicit.

## Why it works

### Integer seed-pair enumeration

Any additive sequence fixes its first two numbers and every later number. Enumerating all legal
seeds and verifying those forced successors is therefore complete.

### Decimal-string seed verification

Column addition produces exactly the required next decimal number. Matching it consecutively
consumes the unique sequence determined by each seed pair, while the same leading-zero rule
keeps representations canonical.

## Walkthrough

"112358" is additive as 1,1,2,3,5,8. "1023" fails: after seeds 1 and 0 the next number must be
1, not 2.

## Cost and pitfalls

Integer seed-pair enumeration: O(n^3) loose bound at bounded numeric length time; O(n) space.
Decimal-string seed verification: O(n^3) loose digit-work bound time; O(n) space.
The input is unchanged. String slices, decimal conversions, and addition copies are included in
the loose bounds. Do not accept a split containing only two numbers. The official string length
is small enough for exhaustive seed pairs.
"""


class Solution:
    """Approach: Integer seed-pair enumeration
    Time: O(n^3) loose bound at bounded numeric length
    Space: O(n)
    """

    def isAdditiveNumber(self, num: str) -> bool:
        for first in range(1, len(num) - 1):
            if first > 1 and num[0] == "0":
                break
            for second in range(first + 1, len(num)):
                if second - first > 1 and num[first] == "0":
                    break
                a, b = int(num[:first]), int(num[first:second])
                position, count = second, 2
                while position < len(num):
                    following = str(a + b)
                    if not num.startswith(following, position):
                        break
                    position += len(following)
                    a, b = b, a + b
                    count += 1
                if position == len(num) and count >= 3:
                    return True
        return False


class DecimalAdditionSolution:
    """Approach: Decimal-string seed verification
    Time: O(n^3) loose digit-work bound
    Space: O(n)
    """

    def isAdditiveNumber(self, num: str) -> bool:
        def add(left, right):
            i, j, carry = len(left) - 1, len(right) - 1, 0
            digits = []
            while i >= 0 or j >= 0 or carry:
                total = carry
                if i >= 0:
                    total += ord(left[i]) - 48
                    i -= 1
                if j >= 0:
                    total += ord(right[j]) - 48
                    j -= 1
                carry, digit = divmod(total, 10)
                digits.append(str(digit))
            return "".join(reversed(digits))

        for first in range(1, len(num) - 1):
            if first > 1 and num[0] == "0":
                break
            for second in range(first + 1, len(num)):
                if second - first > 1 and num[first] == "0":
                    break
                left, right = num[:first], num[first:second]
                position, count = second, 2
                while position < len(num):
                    following = add(left, right)
                    if not num.startswith(following, position):
                        break
                    position += len(following)
                    left, right = right, following
                    count += 1
                if position == len(num) and count >= 3:
                    return True
        return False
