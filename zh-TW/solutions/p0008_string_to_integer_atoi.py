"""## Task

Parse optional leading ASCII spaces, one optional sign, and a decimal digit prefix; clamp
the resulting integer to signed 32-bit range.

## Hints

1. Stop at the first non-digit after the optional sign.
2. Clamp during accumulation to avoid constructing an unbounded parsed integer.

## Approach

### Character scanner with early clamp

Scan spaces and sign, then accumulate digits. Test the next multiplication against the
sign-specific limit before performing it.

### Anchored prefix regular expression

Match exactly a valid leading signed digit prefix, convert its captured decimal digits, then
clamp.

## Why it works

### Character scanner with early clamp

The accumulator equals the already parsed digit prefix. If another digit would exceed the
limit, further decimal digits cannot restore range, so early clamping gives the required
result.

### Anchored prefix regular expression

Anchoring at the beginning prevents skipping invalid leading text. The capture ends at the
first non-digit and optional sign is consumed once, so conversion receives exactly the
specified prefix.

## Walkthrough

"  -0042tail" gives -42; "words 42" gives 0; "2147483648" clamps to 2147483647.

## Cost and pitfalls

Character scanner with early clamp: O(n) time; O(1) space.
Anchored prefix regular expression: O(n) time; O(n) space.

The regex variant allocates digit captures and an integer; input length is at most 200, so
Python integer-conversion digit limits are irrelevant. Inputs stay unchanged. Use ASCII
digit tests rather than broader Unicode isdigit semantics.
"""


class Solution:
    """Approach: Character scanner with early clamp
    Time: O(n)
    Space: O(1)
    """

    def myAtoi(self, s: str) -> int:
        index = 0
        while index < len(s) and s[index] == " ":
            index += 1
        sign = 1
        if index < len(s) and s[index] in "+-":
            sign = -1 if s[index] == "-" else 1
            index += 1
        limit = 2**31 if sign < 0 else 2**31 - 1
        number = 0
        while index < len(s) and "0" <= s[index] <= "9":
            digit = ord(s[index]) - ord("0")
            if number > (limit - digit) // 10:
                return sign * limit
            number = number * 10 + digit
            index += 1
        return sign * number


class RegexSolution:
    """Approach: Anchored prefix regular expression
    Time: O(n)
    Space: O(n)
    """

    def myAtoi(self, s: str) -> int:
        import re

        match = re.match(r" *([+-]?)([0-9]+)", s)
        if match is None:
            return 0
        number = int(match.group(2))
        if match.group(1) == "-":
            number = -number
        return max(-(2**31), min(2**31 - 1, number))
