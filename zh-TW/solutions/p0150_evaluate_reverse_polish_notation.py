"""
## Task

Evaluate a valid postfix expression containing integers and the four arithmetic
operators. Integer division truncates toward zero, and divisors are nonzero.

## Hints

1. An operator consumes the two most recent unfinished values.
2. Which popped value is the right operand of subtraction or division?

## Approach

### Value stack

Push numbers onto a stack. On an operator, pop right and then left, evaluate
left operator right, and push the result. For division, divide absolute values
with integer division and restore the sign.

### Explicit expression-tree reduction

First build an expression tree with a node stack, then evaluate it using an iterative postorder
traversal. This separates parsing from evaluation and avoids recursion depth limits.

## Why it works

### Value stack

After each token, the stack contains the values of completed subexpressions
that have not yet been consumed. Replacing two operands by their result preserves
that interpretation. A valid complete expression leaves exactly one result.

### Explicit expression-tree reduction

Each operator joins the two complete operand expressions immediately before it. Iterative
postorder computes children before their operator, so every node has the same value as its
represented expression.

## Walkthrough

Tokens ["7", "-3", "/", "2", "*"] first produce 7 / -3 = -2, then
-2 * 2 = -4. The final result is -4.

## Cost and pitfalls

Default approach (Value stack):

O(n) time and O(n) space for n tokens under the problem's bounded-integer model.
Inputs are unchanged. Python // floors negative results, so -7 // 3 is not the
required -2. Do not reverse operands. Integer-only division avoids float conversion.

Value stack: O(n) time; O(n) space.
Explicit expression-tree reduction: O(n) time; O(n) space. First build an expression tree with a
node stack, then evaluate it using an iterative postorder traversal. This separates parsing from
evaluation and avoids recursion depth limits.
"""


class Solution:
    """Approach: Value stack
    Time: O(n)
    Space: O(n)
    """

    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for token in tokens:
            if token not in {"+", "-", "*", "/"}:
                stack.append(int(token))
                continue
            right, left = stack.pop(), stack.pop()
            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                result = abs(left) // abs(right)
                if (left < 0) != (right < 0):
                    result = -result
            stack.append(result)
        return stack[0]


class ExpressionTreeSolution:
    """Approach: Explicit expression-tree reduction
    Time: O(n)
    Space: O(n)
    """

    def evalRPN(self, tokens: list[str]) -> int:
        expressions = []
        for token in tokens:
            if token not in {"+", "-", "*", "/"}:
                expressions.append((int(token), None, None))
            else:
                right, left = expressions.pop(), expressions.pop()
                expressions.append((token, left, right))
        pending = [(expressions[0], False)]
        values = []
        while pending:
            node, expanded = pending.pop()
            token, left, right = node
            if left is None:
                values.append(token)
            elif not expanded:
                pending.extend(((node, True), (right, False), (left, False)))
            else:
                b, a = values.pop(), values.pop()
                if token == "+":
                    values.append(a + b)
                elif token == "-":
                    values.append(a - b)
                elif token == "*":
                    values.append(a * b)
                else:
                    quotient = abs(a) // abs(b)
                    values.append(-quotient if (a < 0) != (b < 0) else quotient)
        return values[0]
