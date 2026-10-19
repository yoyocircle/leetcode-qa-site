"""
## Task

Group lowercase words by whether they contain the same letters with the same
multiplicities. Preserve repeated input words; group order does not matter.

## Hints

1. What information remains unchanged when a word is rearranged?
2. The alphabet has only 26 letters. Can that information be a hashable key?

## Approach

### Frequency signatures

Comparing every pair repeats work. Count the 26 letters in each word and use the
count tuple as a dictionary key. Append the original word to that key's group.

### Sorted signatures

Sort each word into its canonical letter order. This is simpler for arbitrary alphabets, at the
cost of sorting every word.

## Why it works

### Frequency signatures

Two words are anagrams exactly when all 26 counts agree. Therefore each key
collects one complete anagram class, and different classes never mix.

### Sorted signatures

Two words have equal sorted characters exactly when every character has the same multiplicity.
Grouping by this key therefore produces exactly the anagram classes.

## Walkthrough

For ["ab", "ba", "bb"], the first two words have counts a=1, b=1 and share a
group. The last has b=2. The result is [["ab", "ba"], ["bb"]].

## Cost and pitfalls

Default approach (Frequency signatures):

Let C be the total characters and n the number of words. Time is O(C + 26n);
auxiliary key storage is O(26n) in the worst case, plus O(n) output references.
Inputs are unchanged. Use a tuple, not a list, as a key. Empty words correctly
share the all-zero key. A set of letters would lose multiplicity.

Frequency signatures: O(nL) time; O(nL) space.
Sorted signatures: O(nL log L) time; O(nL) space. Sort each word into its canonical letter
order. This is simpler for arbitrary alphabets, at the cost of sorting every word.
"""

from collections import defaultdict


class Solution:
    """Approach: Frequency signatures
    Time: O(nL)
    Space: O(nL)
    """

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = defaultdict(list)
        for word in strs:
            counts = [0] * 26
            for char in word:
                counts[ord(char) - ord("a")] += 1
            groups[tuple(counts)].append(word)
        return list(groups.values())


class SortedSolution:
    """Approach: Sorted signatures
    Time: O(nL log L)
    Space: O(nL)
    """

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = {}
        for word in strs:
            key = "".join(sorted(word))
            groups.setdefault(key, []).append(word)
        return list(groups.values())
