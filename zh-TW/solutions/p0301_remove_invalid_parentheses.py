"""## Task

Remove the minimum number of parentheses needed to make a string valid and return every distinct
result. Non-parenthesis characters must remain in order.

## Hints

1. A scan determines the minimum unmatched opening and closing counts.
2. Deleting one character per BFS layer also searches by removal count.

## Approach

### Exact-removal-budget backtracking

Count unmatched openings and closings first. Backtrack keeping or deleting parentheses with
exactly those budgets, preserving nonnegative kept balance and all letters. Deduplicate
completed strings.

### Deletion-layer BFS

At each layer validate all current strings. Return the first layer with valid results; otherwise
remove one parenthesis at every possible position and deduplicate the next layer.

## Why it works

### Exact-removal-budget backtracking

The scan gives unavoidable deletions. Every retained prefix must have nonnegative balance; final
zero balance with exhausted minimum budgets yields exactly a valid minimally edited result.

### Deletion-layer BFS

A layer contains strings reachable with the same deletion count. The first successful layer is
therefore minimal, and all valid strings in that layer must be returned.

## Walkthrough

For "()())()", minimum one deletion yields "(())()" and "()()()".

## Cost and pitfalls

Exact-removal-budget backtracking: O(n*2^p) loose bound time; O(n) auxiliary plus output space.
Deletion-layer BFS: O(n^2*2^p) loose bound; may time out time; O(n*2^p) loose bound space.
The input is immutable. p is its number of parentheses. Python deletion slices copy strings. The
BFS baseline may use much more memory at full limits; the default prunes with exact budgets.
Letters are never deleted.
"""


class Solution:
    """Approach: Exact-removal-budget backtracking
    Time: O(n*2^p) loose bound
    Space: O(n) auxiliary plus output
    """

    def removeInvalidParentheses(self, s: str) -> list[str]:
        left = right = 0
        for char in s:
            if char == "(":
                left += 1
            elif char == ")":
                if left:
                    left -= 1
                else:
                    right += 1
        result, path = set(), []

        def visit(index, balance, remove_left, remove_right):
            if remove_left + remove_right > len(s) - index:
                return
            if index == len(s):
                if balance == remove_left == remove_right == 0:
                    result.add("".join(path))
                return
            char = s[index]
            if char == "(" and remove_left:
                visit(index + 1, balance, remove_left - 1, remove_right)
            if char == ")" and remove_right:
                visit(index + 1, balance, remove_left, remove_right - 1)
            following = balance + (char == "(") - (char == ")")
            if following >= 0:
                path.append(char)
                visit(index + 1, following, remove_left, remove_right)
                path.pop()

        visit(0, 0, left, right)
        return sorted(result)


class BreadthFirstSolution:
    """Approach: Deletion-layer BFS
    Time: O(n^2*2^p) loose bound; may time out
    Space: O(n*2^p) loose bound
    """

    def removeInvalidParentheses(self, s: str) -> list[str]:
        def valid(text):
            balance = 0
            for char in text:
                balance += (char == "(") - (char == ")")
                if balance < 0:
                    return False
            return balance == 0

        level = {s}
        while True:
            accepted = sorted(text for text in level if valid(text))
            if accepted:
                return accepted
            level = {
                text[:index] + text[index + 1 :]
                for text in level
                for index, char in enumerate(text)
                if char in "()" and (index == 0 or char != text[index - 1])
            }
