"""
## Task

Decide whether a string of parentheses and stars can be balanced when each star may act as an
opening parenthesis, a closing parenthesis, or empty.

## Hints

1. Track the smallest and largest possible unmatched-opening counts.
2. Separate position stacks can enforce that substitute closing stars occur after their matching
   openings.

## Approach

### Interval of possible opening counts

Maintain low and high unmatched-opening counts. A star widens the range by one each way; clamp
low to zero and reject if high becomes negative.

### Opening and star position stacks

Match each closing parenthesis with a real opening if possible, otherwise a prior star. After
scanning, match remaining openings with later stars.

## Why it works

### Interval of possible opening counts

Every possible unmatched count between the bounds remains achievable after each character. A
negative high means even the most opening-friendly choices fail; final low zero means at least
one assignment ends balanced.

### Opening and star position stacks

Using a real opening first preserves flexible stars for later needs. Any unmatched opening can
only be closed by a later star; matching the latest positions detects exactly whether all
remaining openings have such substitutes.

## Walkthrough

"(*))" can use the star as an opening parenthesis. "*(" fails because a star before the
remaining opening cannot act as its closing parenthesis.

## Cost and pitfalls

Interval of possible opening counts: O(n) time; O(1) space.

Opening and star position stacks: O(n) time; O(n) space.

Inputs are unchanged. Empty substitution is allowed; requiring every star to become a
parenthesis would reject valid strings. Stack matching must compare positions, not only counts.
"""


class Solution:
    """Approach: Interval of possible opening counts
    Time: O(n)
    Space: O(1)
    """

    def checkValidString(self, s: str) -> bool:
        low = high = 0
        for char in s:
            if char == "(":
                low += 1
                high += 1
            elif char == ")":
                low -= 1
                high -= 1
            else:
                low -= 1
                high += 1
            if high < 0:
                return False
            low = max(0, low)
        return low == 0


class PositionStackSolution:
    """Approach: Opening and star position stacks
    Time: O(n)
    Space: O(n)
    """

    def checkValidString(self, s: str) -> bool:
        openings = []
        stars = []
        for i, char in enumerate(s):
            if char == "(":
                openings.append(i)
            elif char == "*":
                stars.append(i)
            elif openings:
                openings.pop()
            elif stars:
                stars.pop()
            else:
                return False
        while openings and stars:
            if openings.pop() > stars.pop():
                return False
        return not openings
