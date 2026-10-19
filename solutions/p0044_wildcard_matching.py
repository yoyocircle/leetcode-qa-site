"""## Task

Match an entire string using "?" for one character and "*" for any sequence, including empty.

## Hints

1. A star either consumes nothing or consumes one more character.
2. A most recent star can absorb characters when later matching fails.

## Approach

### Greedy retry at the latest star

Match ordinary characters eagerly. Remember the latest star and the text position it
currently absorbs through. On mismatch, give that star one more character and retry its
suffix.

### Rolling wildcard prefix table

For each text prefix, compute pattern-prefix matches. A star uses left for zero consumption
or above for one more; ordinary tokens use the matching diagonal.

## Why it works

### Greedy retry at the latest star

For a fixed star, shorter assignments are tried before longer ones. Once a later star is
reached, it can absorb any extra characters that an earlier star could have consumed, so
only the latest retry point is needed.

### Rolling wildcard prefix table

The star cases partition matches by whether its final consumed sequence is empty. Ordinary
tokens consume exactly one character, so the recurrence covers all and only legal
whole-string matches.

## Walkthrough

The pattern "a*b?" matches "axxbz"; the final question mark consumes z.

## Cost and pitfalls

Greedy retry at the latest star: O((m+1)*(n+1)) worst case time; O(1) space.
Rolling wildcard prefix table: O((m+1)*(n+1)) time; O(n) space.

m and n are text and pattern lengths. Greedy retries can rescan a long literal suffix, so
its worst case is not linear. Inputs remain unchanged; glob stars differ from regex stars.
"""


class Solution:
    """Approach: Greedy retry at the latest star
    Time: O((m+1)*(n+1)) worst case
    Space: O(1)
    """

    def isMatch(self, s: str, p: str) -> bool:
        i = j = 0
        star = -1
        consumed = 0
        while i < len(s):
            if j < len(p) and (p[j] == "?" or p[j] == s[i]):
                i += 1
                j += 1
            elif j < len(p) and p[j] == "*":
                star = j
                consumed = i
                j += 1
            elif star >= 0:
                consumed += 1
                i, j = consumed, star + 1
            else:
                return False
        while j < len(p) and p[j] == "*":
            j += 1
        return j == len(p)


class DPSolution:
    """Approach: Rolling wildcard prefix table
    Time: O((m+1)*(n+1))
    Space: O(n)
    """

    def isMatch(self, s: str, p: str) -> bool:
        previous = [True] + [False] * len(p)
        for j, atom in enumerate(p, 1):
            previous[j] = previous[j - 1] and atom == "*"
        for character in s:
            current = [False] * (len(p) + 1)
            for j, atom in enumerate(p, 1):
                current[j] = (
                    current[j - 1] or previous[j]
                    if atom == "*"
                    else previous[j - 1] and atom in ("?", character)
                )
            previous = current
        return previous[-1]
