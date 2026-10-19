"""## Task

Generate every balanced parentheses string containing exactly n matching pairs.

## Hints

1. Never close more pairs than have been opened.
2. A balanced string is an opening parenthesis, a balanced interior, a closing parenthesis, and
   a balanced suffix.

## Approach

### Balance-constrained backtracking

Track opened and closed counts. Add an opening while opened<n and a closing while closed<opened.
Record strings of length 2n.

### Catalan concatenation DP

For each size, combine every smaller interior and suffix as "("+inside+")"+after. Store all
strings by pair count.

## Why it works

### Balance-constrained backtracking

Every prefix maintains nonnegative balance and never exceeds n openings. Complete strings have
equal counts, and every valid string follows one permitted sequence of choices.

### Catalan concatenation DP

The closing parenthesis matching the first opening uniquely splits a nonempty valid string into
its interior and suffix. Enumerating that split generates all and only balanced strings without
duplicates.

## Walkthrough

For n=2, an empty interior with suffix "()" gives "()()"; interior "()" with empty suffix gives
"(())".

## Cost and pitfalls

Balance-constrained backtracking: O(n*C_n) time; O(n) auxiliary plus output space.
Catalan concatenation DP: O(n^2*C_n) loose bound time; O(n^2*C_n) loose bound space.
C_n counts balanced strings. Strings and path joins incur copying included in the bounds. DP
retains intermediate strings; DFS needs only one working path. Recursion is bounded by n<=8.
"""


class Solution:
    """Approach: Balance-constrained backtracking
    Time: O(n*C_n)
    Space: O(n) auxiliary plus output
    """

    def generateParenthesis(self, n: int) -> list[str]:
        result, path = [], []

        def visit(opened, closed):
            if closed == n:
                result.append("".join(path))
                return
            if opened < n:
                path.append("(")
                visit(opened + 1, closed)
                path.pop()
            if closed < opened:
                path.append(")")
                visit(opened, closed + 1)
                path.pop()

        visit(0, 0)
        return result


class CatalanDPSolution:
    """Approach: Catalan concatenation DP
    Time: O(n^2*C_n) loose bound
    Space: O(n^2*C_n) loose bound
    """

    def generateParenthesis(self, n: int) -> list[str]:
        values = [[""]]
        for size in range(1, n + 1):
            values.append(
                [
                    "(" + inside + ")" + after
                    for left in range(size)
                    for inside in values[left]
                    for after in values[size - left - 1]
                ]
            )
        return values[n]
