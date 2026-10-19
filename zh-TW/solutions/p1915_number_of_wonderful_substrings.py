"""
## Task

Count nonempty substrings of a word over letters a through j in which at most one letter occurs
an odd number of times.

## Hints

1. A ten-bit mask records prefix occurrence parities.
2. Two prefix masks can differ in zero or one bits for a qualifying substring.

## Approach

### Online parity-mask neighbors

For each new prefix mask, add counts of that same earlier mask and its ten one-bit neighbors,
then record this prefix.

### Batch mask-pair counting

Count all prefix masks first. Equal masks contribute c choose 2; differing one-bit mask groups
contribute their frequency product, counted only in one direction.

## Why it works

### Online parity-mask neighbors

The XOR of two prefix masks gives exactly the substring parity mask. Zero or one set bits are
precisely the wonderful condition; each earlier prefix defines a distinct substring.

### Batch mask-pair counting

Every unordered pair of distinct prefix positions determines one earlier/later substring. Since
XOR is symmetric, mask frequencies suffice without retaining index order. Group pairs at Hamming
distance at most one count exactly all wonderful substrings.

## Walkthrough

"aba" has prefix masks 0,1,3,2. Its three singleton substrings and full substring "aba" qualify,
giving four.

## Cost and pitfalls

Online parity-mask neighbors: O(10n) time; O(2^10) space.

Batch mask-pair counting: O(n+10*2^10) time; O(2^10) space.

Input is unchanged. Include the empty prefix. Count different mask pairs only once; summing both
directions would double the one-odd-letter cases.
"""


class Solution:
    """Approach: Online parity-mask neighbors
    Time: O(10n)
    Space: O(2^10)
    """

    def wonderfulSubstrings(self, word: str) -> int:
        counts = [0] * 1024
        counts[0] = 1
        mask = answer = 0
        for char in word:
            mask ^= 1 << (ord(char) - 97)
            answer += counts[mask]
            for bit in range(10):
                answer += counts[mask ^ (1 << bit)]
            counts[mask] += 1
        return answer


class BatchMaskSolution:
    """Approach: Batch mask-pair counting
    Time: O(n+10*2^10)
    Space: O(2^10)
    """

    def wonderfulSubstrings(self, word: str) -> int:
        counts = [0] * 1024
        counts[0] = 1
        mask = 0
        for char in word:
            mask ^= 1 << (ord(char) - 97)
            counts[mask] += 1
        answer = sum(count * (count - 1) // 2 for count in counts)
        for mask, count in enumerate(counts):
            for bit in range(10):
                neighbor = mask ^ (1 << bit)
                if mask < neighbor:
                    answer += count * counts[neighbor]
        return answer
