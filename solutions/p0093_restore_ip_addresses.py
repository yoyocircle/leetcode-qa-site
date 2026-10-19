"""## Task

Insert three dots into a digit string to form all valid four-part IPv4 addresses. Each part is 0
through 255 and cannot have a leading zero unless it is exactly "0".

## Hints

1. Each address part contains one to three digits.
2. Prune when the remaining digits cannot fill the remaining parts.

## Approach

### Four-part backtracking

Choose each next part length from one through three, reject invalid values or leading zeros, and
use remaining-length bounds before recursing.

### Enumerate the three cut lengths

Enumerate lengths of the first three parts independently from one through three. The remainder
is the fourth part; validate all four pieces together.

## Why it works

### Four-part backtracking

Every valid address has one sequence of four legal part lengths. The search tries each such
sequence once and rejects only violations of the address rules.

### Enumerate the three cut lengths

Every placement of three dots uniquely determines its first three part lengths. Enumerating them
therefore covers every possible address, while validation enforces the full contract.

## Walkthrough

For "101023", accepted examples include "1.0.10.23" and "10.10.2.3". A piece "023" is invalid.

## Cost and pitfalls

Four-part backtracking: O(3^4*n) loose bound time; O(n) auxiliary plus output space.
Enumerate the three cut lengths: O(27*n) time; O(n) auxiliary plus output space.
The input is unchanged. String slices and joined addresses copy characters. There are only four
parts; the small constant search does not depend exponentially on unbounded n. Lengths outside
4..12 have no answer.
"""


class Solution:
    """Approach: Four-part backtracking
    Time: O(3^4*n) loose bound
    Space: O(n) auxiliary plus output
    """

    def restoreIpAddresses(self, s: str) -> list[str]:
        result, path = [], []

        def visit(start):
            missing = 4 - len(path)
            if not missing <= len(s) - start <= 3 * missing:
                return
            if missing == 0:
                result.append(".".join(path))
                return
            for length in range(1, 4):
                piece = s[start : start + length]
                if len(piece) != length or (length > 1 and piece[0] == "0") or int(piece) > 255:
                    continue
                path.append(piece)
                visit(start + length)
                path.pop()

        visit(0)
        return result


class CutEnumerationSolution:
    """Approach: Enumerate the three cut lengths
    Time: O(27*n)
    Space: O(n) auxiliary plus output
    """

    def restoreIpAddresses(self, s: str) -> list[str]:
        result = []
        for first in range(1, 4):
            for second in range(1, 4):
                for third in range(1, 4):
                    a, b, c = first, first + second, first + second + third
                    pieces = [s[:a], s[a:b], s[b:c], s[c:]]
                    if all(
                        1 <= len(piece) <= 3
                        and (len(piece) == 1 or piece[0] != "0")
                        and int(piece) <= 255
                        for piece in pieces
                    ):
                        result.append(".".join(pieces))
        return result
