"""## Task

Count ways to decode a digit string using 1 through 26 for letters A through Z.

## Hints

1. A zero cannot decode alone.
2. The final decoded letter consumes one valid digit or two digits from 10 through 26.

## Approach

### Rolling prefix decode counts

Maintain counts for prefixes ending one and two positions earlier. Add the one-digit choice
when nonzero and the two-digit choice when its tens and units form 10 through 26.

### Memoized suffix decoding

Count completions from each index, rejecting leading zero and recursing on either valid next
code. Cache indices rather than substring copies.

## Why it works

### Rolling prefix decode counts

Every decoding ends with exactly one valid one- or two-digit code. Removing that last code
leaves one of the retained shorter prefixes, and the two groups do not overlap.

### Memoized suffix decoding

Every valid decoding has one unique first code of length one or two. The recurrence
partitions by that choice, and the empty remaining suffix contributes one completed
decoding.

## Walkthrough

"226" decodes as 2|2|6, 22|6, or 2|26, giving 3; "06" gives zero.

## Cost and pitfalls

Rolling prefix decode counts: O(n) time; O(1) space.
Memoized suffix decoding: O(n) time; O(n) space.

Inputs remain unchanged. Memo recursion depth is at most n=100 and safe at the stated
limits. The rolling recurrence saves cache and stack storage; neither treats zero as a
standalone letter.
"""


class Solution:
    """Approach: Rolling prefix decode counts
    Time: O(n)
    Space: O(1)
    """

    def numDecodings(self, s: str) -> int:
        older, previous = 1, int(s[0] != "0")
        for index in range(1, len(s)):
            current = previous if s[index] != "0" else 0
            if s[index - 1] == "1" or (s[index - 1] == "2" and s[index] <= "6"):
                current += older
            older, previous = previous, current
        return previous


class MemoSolution:
    """Approach: Memoized suffix decoding
    Time: O(n)
    Space: O(n)
    """

    def numDecodings(self, s: str) -> int:
        from functools import cache

        @cache
        def decode(index):
            if index == len(s):
                return 1
            if s[index] == "0":
                return 0
            answer = decode(index + 1)
            if index + 1 < len(s) and (
                s[index] == "1" or (s[index] == "2" and s[index + 1] <= "6")
            ):
                answer += decode(index + 2)
            return answer

        return decode(0)
