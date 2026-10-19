"""
## Task

Return every length-10 DNA substring that appears at least twice. Each repeated sequence appears
once in the output.

## Hints

1. Track previously seen windows and separately track repeated windows.
2. A DNA letter needs only two bits.

## Approach

### Substring sets

Slice each ten-letter window and put it in seen or repeated sets. Fixed L makes slicing a
constant bounded cost.

### Rolling two-bit encoding

Maintain a 20-bit rolling code, dropping all but the last ten letters. Slice a sequence only
when its code becomes repeated for the first time.

## Why it works

### Substring sets

The first occurrence enters seen, the second enters repeated, and later occurrences cannot add a
duplicate set element.

### Rolling two-bit encoding

Two-bit digits give an injective encoding of each fixed-length DNA window. Masking removes
exactly the letter leaving the window, so equal codes mean equal ten-letter strings without hash
collisions.

## Walkthrough

For eleven A characters, the same AAAAAAAAAA window occurs twice, so return it once.

## Cost and pitfalls

Substring sets: O(nL), L=10 time; O(nL), L=10 space.

Rolling two-bit encoding: O(n) time; O(n) space.

Input is unchanged; answer order is arbitrary. Do not start recording rolling codes until ten
letters have arrived.
"""


class Solution:
    """Approach: Substring sets
    Time: O(nL), L=10
    Space: O(nL), L=10
    """

    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        seen, repeated = set(), set()
        for i in range(len(s) - 9):
            sequence = s[i : i + 10]
            if sequence in seen:
                repeated.add(sequence)
            seen.add(sequence)
        return sorted(repeated)


class RollingCodeSolution:
    """Approach: Rolling two-bit encoding
    Time: O(n)
    Space: O(n)
    """

    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        codes = {"A": 0, "C": 1, "G": 2, "T": 3}
        seen, repeated = set(), set()
        result = []
        code = 0
        for i, char in enumerate(s):
            code = ((code << 2) | codes[char]) & ((1 << 20) - 1)
            if i < 9:
                continue
            if code in seen and code not in repeated:
                result.append(s[i - 9 : i + 1])
                repeated.add(code)
            seen.add(code)
        return result
