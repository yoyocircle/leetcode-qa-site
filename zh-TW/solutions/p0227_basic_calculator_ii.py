"""## Task

Evaluate a valid expression containing nonnegative integers and +, -, *, /, with
multiplication/division precedence and division truncated toward zero.

## Hints

1. Resolve multiplication and division within the current term before adding it to the total.
2. A stack can retain all additive terms instead of one rolling term.

## Approach

### Rolling additive total and current term

Retain the completed additive total and one signed multiplicative term. A new plus/minus
commits the preceding term; multiplication/division modifies only the current term.

### Stack of signed additive terms

Push signed terms for plus/minus and immediately fold multiplication/division into the last
term. Sum the completed term list at the end.

## Why it works

### Rolling additive total and current term

The total contains exactly finished low-precedence terms, while term contains the current
precedence chain. Applying operators in this separation matches the grammar and
left-associative multiplication/division.

### Stack of signed additive terms

Each stack entry is one additive term after all higher-precedence operations seen within it.
Folding the top preserves precedence, and the final sum combines the fully evaluated terms.

## Walkthrough

"14-3/2" gives 13 because 3/2 truncates to 1; "3+2*2" gives 7.

## Cost and pitfalls

Rolling additive total and current term: O(n) time; O(1) space.
Stack of signed additive terms: O(n) time; O(n) space.

Both preserve s and avoid an appended-string copy by using a virtual final operator.
Integer-only truncation avoids float rounding and differs from Python floor division for
negative intermediate terms. Valid input never divides by zero.
"""


class Solution:
    """Approach: Rolling additive total and current term
    Time: O(n)
    Space: O(1)
    """

    def calculate(self, s: str) -> int:
        total = term = number = 0
        operator = "+"
        for index in range(len(s) + 1):
            character = s[index] if index < len(s) else "+"
            if "0" <= character <= "9":
                number = number * 10 + ord(character) - ord("0")
            elif character != " ":
                if operator == "+":
                    total, term = total + term, number
                elif operator == "-":
                    total, term = total + term, -number
                elif operator == "*":
                    term *= number
                else:
                    term = (abs(term) // number) * (1 if term >= 0 else -1)
                operator, number = character, 0
        return total + term


class StackSolution:
    """Approach: Stack of signed additive terms
    Time: O(n)
    Space: O(n)
    """

    def calculate(self, s: str) -> int:
        stack = []
        number = 0
        operator = "+"
        for index in range(len(s) + 1):
            character = s[index] if index < len(s) else "+"
            if "0" <= character <= "9":
                number = number * 10 + ord(character) - ord("0")
            elif character != " ":
                if operator == "+":
                    stack.append(number)
                elif operator == "-":
                    stack.append(-number)
                elif operator == "*":
                    stack[-1] *= number
                else:
                    previous = stack[-1]
                    stack[-1] = (abs(previous) // number) * (1 if previous >= 0 else -1)
                operator, number = character, 0
        return sum(stack)
