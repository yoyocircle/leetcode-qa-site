"""
## Task

Multiply two nonnegative decimal integer strings and return their product as a string. Do not
convert the whole inputs to built-in integers.

## Hints

1. A product of m and n digits needs at most m+n output slots.
2. Single-digit multiplication and string addition also support the usual written algorithm.

## Approach

### Digit-array grade-school multiplication

Accumulate digit products into their positional slots and propagate each carry toward the
preceding slot.

### Partial-product strings and addition

Multiply num1 by each single digit of num2, append its decimal shift, and add the partial
product to a running string sum.

## Why it works

### Digit-array grade-school multiplication

Digits at input positions i and j contribute to decimal slot i+j+1. Dividing each accumulated
slot into a digit and carry preserves its numeric value; all pair products are included exactly
once.

### Partial-product strings and addition

Single-digit carry multiplication computes each positional partial product exactly. Summing
these shifted products follows the distributive expansion of the second input, so the final
string represents their product.

## Walkthrough

"123" times "45" adds partial products "615" and "4920", giving "5535".

## Cost and pitfalls

Digit-array grade-school multiplication: O(mn) time; O(m+n) space.

Partial-product strings and addition: O(mn+n squared) time; O(m+n) space.

Inputs are unchanged. m and n are digit lengths. Per-digit integer arithmetic is allowed;
converting an entire input to int or returning leading zeroes violates the intended contract.
"""


class Solution:
    """Approach: Digit-array grade-school multiplication
    Time: O(mn)
    Space: O(m+n)
    """

    def multiply(self, num1: str, num2: str) -> str:
        digits = [0] * (len(num1) + len(num2))
        for i in range(len(num1) - 1, -1, -1):
            for j in range(len(num2) - 1, -1, -1):
                total = digits[i + j + 1] + (ord(num1[i]) - 48) * (ord(num2[j]) - 48)
                digits[i + j + 1] = total % 10
                digits[i + j] += total // 10
        return "".join(map(str, digits)).lstrip("0") or "0"


class PartialProductSolution:
    """Approach: Partial-product strings and addition
    Time: O(mn+n squared)
    Space: O(m+n)
    """

    def multiply(self, num1: str, num2: str) -> str:
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

        answer = "0"
        for shift, char in enumerate(reversed(num2)):
            carry = 0
            digits = []
            for other in reversed(num1):
                carry, digit = divmod((ord(char) - 48) * (ord(other) - 48) + carry, 10)
                digits.append(str(digit))
            if carry:
                digits.append(str(carry))
            partial = "".join(reversed(digits)) + "0" * shift
            answer = add(answer, partial)
        return answer.lstrip("0") or "0"
