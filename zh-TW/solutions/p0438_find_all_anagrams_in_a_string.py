"""
## Task

Return starting indices of all substrings of s that are anagrams of nonempty lowercase pattern
p.

## Hints

1. All candidate windows have length len(p).
2. Comparing counts or tracking exact matches both avoid generating permutations.

## Approach

### Fixed count vectors

Slide a width-m frequency vector and compare it with the pattern vector after each full window.

### Deficit-based window

Count missing pattern characters and maintain a fixed-width window. Zero missing characters
identifies a full anagram.

## Why it works

### Fixed count vectors

Two equal-length strings are anagrams exactly when all character counts agree. Each length-m
substring is visited once.

### Deficit-based window

The deficit counts account for duplicate letters. Once window length equals pattern length, full
multiset coverage implies exact equality, including the absence of extra letters.

## Walkthrough

s="cbaebabacd", p="abc": windows at 0 and 6 have the exact multiset {a,b,c}, so return [0,6].

## Cost and pitfalls

Fixed count vectors: O(26n+m) time; O(26) plus output space.

Deficit-based window: O(n+m) expected time; O(alphabet) plus output space.

Inputs are unchanged. A pattern longer than the text yields no full window. Repeated pattern
letters require counts, not a character set.
"""

from collections import Counter


class Solution:
    """Approach: Fixed count vectors
    Time: O(26n+m)
    Space: O(26) plus output
    """

    def findAnagrams(self, s: str, p: str) -> list[int]:
        need, have = [0] * 26, [0] * 26
        for char in p:
            need[ord(char) - 97] += 1
        answer = []
        for i, char in enumerate(s):
            have[ord(char) - 97] += 1
            if i >= len(p):
                have[ord(s[i - len(p)]) - 97] -= 1
            if i >= len(p) - 1 and have == need:
                answer.append(i - len(p) + 1)
        return answer


class DeficitSolution:
    """Approach: Deficit-based window
    Time: O(n+m) expected
    Space: O(alphabet) plus output
    """

    def findAnagrams(self, s: str, p: str) -> list[int]:
        need = Counter(p)
        missing = len(p)
        answer = []
        for i, char in enumerate(s):
            if need[char] > 0:
                missing -= 1
            need[char] -= 1
            if i >= len(p):
                outgoing = s[i - len(p)]
                need[outgoing] += 1
                if need[outgoing] > 0:
                    missing += 1
            if i >= len(p) - 1 and missing == 0:
                answer.append(i - len(p) + 1)
        return answer
