"""## Task

Return the length of the longest contiguous balanced-parentheses substring.

## Hints

1. An unmatched closing parenthesis becomes a new boundary.
2. Two directional scans detect excess opens as well as excess closes.

## Approach

### Stack of unmatched indices

Seed a boundary index -1. Opens push their indices; closes match an open or reset the
unmatched-close boundary. Measure from the remaining stack top.

### Forward and backward balance counts

Count opens and closes from left to right, resetting at excess closes. Repeat right to left
with the symmetric excess-open reset.

## Why it works

### Stack of unmatched indices

After a successful match, the stack top is the closest unmatched boundary before the
balanced suffix. Its distance is therefore the longest valid suffix ending here.

### Forward and backward balance counts

A reset boundary cannot belong to a valid segment crossing it. Balanced counts between
resets reveal valid runs; the reverse scan recovers runs hidden behind unmatched opens in
the forward scan.

## Walkthrough

For ")()())", the middle "()()" has length 4.

## Cost and pitfalls

Stack of unmatched indices: O(n) time; O(n) space.
Forward and backward balance counts: O(n) time; O(1) space.

The empty string returns zero. Neither changes the input or allocates a reversed copy.
Counts alone in one direction miss examples such as "(()".
"""


class Solution:
    """Approach: Stack of unmatched indices
    Time: O(n)
    Space: O(n)
    """

    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]
        best = 0
        for index, character in enumerate(s):
            if character == "(":
                stack.append(index)
            else:
                stack.pop()
                if not stack:
                    stack.append(index)
                else:
                    best = max(best, index - stack[-1])
        return best


class CounterSolution:
    """Approach: Forward and backward balance counts
    Time: O(n)
    Space: O(1)
    """

    def longestValidParentheses(self, s: str) -> int:
        best = 0
        for reverse in (False, True):
            opens = closes = 0
            for index in range(len(s) - 1, -1, -1) if reverse else range(len(s)):
                opens += s[index] == "("
                closes += s[index] == ")"
                if opens == closes:
                    best = max(best, opens + closes)
                elif opens > closes if reverse else closes > opens:
                    opens = closes = 0
        return best
