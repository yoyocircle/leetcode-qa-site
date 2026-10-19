"""## Task

Count distinct nonempty substrings of s appearing in the infinite wraparound alphabet
...zabcdefghijklmnopqrstuvwxyz....

## Hints

1. Track a maximal consecutive-alphabet run ending at each position.
2. For a fixed final letter, longer valid runs contain all shorter suffixes.

## Approach

### Longest valid run per ending letter

Extend a run when the alphabet step is one modulo 26. Record only the maximum run ending
with each letter, then sum these maxima.

### Longest valid run per starting letter

Scan backward and retain the longest valid run beginning with each letter. Sum all
represented prefix lengths.

## Why it works

### Longest valid run per ending letter

A wraparound substring is uniquely determined by its final letter and length. An observed
run of length L supplies every length 1 through L for that letter, so the maximum represents
exactly its distinct possibilities.

### Longest valid run per starting letter

A starting letter and length also determine exactly one wraparound string. Every run
supplies all its prefixes, and runs with the same starting letter contribute only up to
their maximum length.

## Walkthrough

For "zab", the distinct valid substrings are z,a,b,za,ab,zab, giving 6.

## Cost and pitfalls

Longest valid run per ending letter: O(n) time; O(26) space.
Longest valid run per starting letter: O(n) time; O(26) space.

Both preserve s and use no substring copies or distinct-string set. The modulo comparison
admits z followed by a. Counting occurrences instead of letter-and-length possibilities
would overcount repeated text.
"""


class Solution:
    """Approach: Longest valid run per ending letter
    Time: O(n)
    Space: O(26)
    """

    def findSubstringInWraproundString(self, s: str) -> int:
        best = [0] * 26
        run = 0
        for index, character in enumerate(s):
            run = run + 1 if index and (ord(character) - ord(s[index - 1])) % 26 == 1 else 1
            letter = ord(character) - ord("a")
            best[letter] = max(best[letter], run)
        return sum(best)


class StartingLetterSolution:
    """Approach: Longest valid run per starting letter
    Time: O(n)
    Space: O(26)
    """

    def findSubstringInWraproundString(self, s: str) -> int:
        best = [0] * 26
        run = 0
        for index in range(len(s) - 1, -1, -1):
            run = (
                run + 1
                if index + 1 < len(s) and (ord(s[index + 1]) - ord(s[index])) % 26 == 1
                else 1
            )
            letter = ord(s[index]) - ord("a")
            best[letter] = max(best[letter], run)
        return sum(best)
