"""## Task

Evaluate an integer expression with plus, minus, spaces, and parentheses, including unary
minus, using integer arithmetic.

## Hints

1. A parenthesis can save the outside total and its pending sign.
2. An operator/value stack provides a general precedence-based alternative without recursion.

## Approach

### Parenthesis context totals

Accumulate a signed total inside the current context. An opening parenthesis saves the outer
total and sign; closing one multiplies the completed subtotal by that sign and restores the
outer total.

### Shunting-yard values and unary operators

Maintain explicit value and operator stacks. Recognize unary signs when an operand is
expected, preserve parenthesis barriers, and apply pending operators before the next
equal-precedence binary sign.

## Why it works

### Parenthesis context totals

Inside each context, completed terms equal its evaluated prefix. Saving and restoring the
outer sign treats the entire parenthesized expression as one signed term, including unary
minus before a parenthesis.

### Shunting-yard values and unary operators

Stack operators retain exactly the unfinished expression structure. Unary operators consume
one value; binary operators consume two in original order. Parenthesis barriers delay
outside operations until the enclosed expression is complete.

## Walkthrough

"1-(2-(3+4))" evaluates to 6; "-(2+3)" evaluates to -5.

## Cost and pitfalls

Parenthesis context totals: O(n) time; O(n) space.
Shunting-yard values and unary operators: O(n) time; O(n) space.

Inputs stay unchanged. Both are iterative for deeply nested expressions and use no eval. The
context method is specialized to addition/subtraction; the operator method exposes parsing
state and unary arity. Valid input excludes unary plus and ambiguous consecutive binary
signs, though the alternate also supports unary plus.
"""


class Solution:
    """Approach: Parenthesis context totals
    Time: O(n)
    Space: O(n)
    """

    def calculate(self, s: str) -> int:
        total = number = 0
        sign = 1
        stack = []
        for character in s:
            if "0" <= character <= "9":
                number = number * 10 + ord(character) - ord("0")
            elif character in "+-":
                total += sign * number
                number = 0
                sign = 1 if character == "+" else -1
            elif character == "(":
                stack.append((total, sign))
                total, sign = 0, 1
            elif character == ")":
                total += sign * number
                number = 0
                outside, multiplier = stack.pop()
                total = outside + multiplier * total
        return total + sign * number


class OperatorSolution:
    """Approach: Shunting-yard values and unary operators
    Time: O(n)
    Space: O(n)
    """

    def calculate(self, s: str) -> int:
        values, operators = [], []

        def apply():
            operator = operators.pop()
            if operator == "u-":
                values.append(-values.pop())
            elif operator == "u+":
                return
            else:
                second, first = values.pop(), values.pop()
                values.append(first + second if operator == "+" else first - second)

        index = 0
        expect_operand = True
        while index < len(s):
            character = s[index]
            if character == " ":
                index += 1
                continue
            if "0" <= character <= "9":
                number = 0
                while index < len(s) and "0" <= s[index] <= "9":
                    number = number * 10 + ord(s[index]) - ord("0")
                    index += 1
                values.append(number)
                expect_operand = False
                continue
            if character == "(":
                operators.append(character)
                expect_operand = True
            elif character == ")":
                while operators[-1] != "(":
                    apply()
                operators.pop()
                expect_operand = False
            elif expect_operand:
                operators.append("u" + character)
            else:
                while operators and operators[-1] != "(":
                    apply()
                operators.append(character)
                expect_operand = True
            index += 1
        while operators:
            apply()
        return values[0]
