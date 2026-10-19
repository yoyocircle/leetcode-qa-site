"""## Task

Decide whether a string can be split into one or more dictionary words.
Words can be reused, and all dictionary words are nonempty.

## Hints

1. A valid prefix followed by one dictionary word creates another valid prefix.
2. Only dictionary word lengths can be the length of that final piece.

## Approach

### Reachable prefixes and word lengths

Build a word set and sorted distinct word lengths. Let reachable[end] mean
the prefix ending just before end can be segmented. Initialize reachable[0]
to true. For every end position, try candidate word lengths up to end.
If reachable[end-length] and the intervening substring belongs to the word
set, mark this prefix reachable and stop. Return the final prefix state.

### Trie walks from reachable starts

Build a character trie with terminal markers. From each reachable prefix, walk forward
through matching trie edges and mark every word ending reached. A failed edge stops that
start without allocating substrings.

## Why it works

### Reachable prefixes and word lengths

A successful transition appends a dictionary word to an already valid
segmentation. Conversely, any segmentation has a final dictionary word;
its length is tried, and its preceding prefix is valid. Increasing end
positions ensures that earlier prefix is already solved. Thus the table
contains exactly the segmentable prefixes.

### Trie walks from reachable starts

Trie terminal nodes correspond exactly to dictionary words. Every marked endpoint appends
one such word to a valid prefix, and every valid final word is explored from its reachable
start.

## Walkthrough

For "redredblue" and ["red","blue"], positions 3, 6, and 10 become
reachable. The second "red" reuses a word, which is allowed. A prefix
such as "redr" remains unreachable.

## Cost and pitfalls

For the default Reachable prefixes and word lengths approach:

Let n be string length, D distinct lengths, L maximum word length, and W
total dictionary characters. Expected time is O(W + D log D + n*D*L):
Python slicing and hashing each new substring cost its length. Space is
O(n+D+number_of_words+L), including a temporary slice; word strings are
referenced. Inputs stay unchanged. Greedy longest-word selection can miss a
valid split that starts with a shorter word.

Reachable prefixes and word lengths: O(W + D log D + n*D*L) time; O(n+D+K+L) space.
Trie walks from reachable starts: O(W+n*L) time; O(W+n) space.
W is total dictionary characters, D distinct lengths, K word count, and L maximum word
length. Trie walks avoid substring copy/hash costs but allocate dictionaries per trie node.
"""


class Solution:
    """Approach: Reachable prefixes and word lengths
    Time: O(W + D log D + n*D*L)
    Space: O(n+D+K+L)
    """

    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        lengths = sorted({len(word) for word in words})
        reachable = [False] * (len(s) + 1)
        reachable[0] = True
        for end in range(1, len(s) + 1):
            for length in lengths:
                if length > end:
                    break
                if reachable[end - length] and s[end - length : end] in words:
                    reachable[end] = True
                    break
        return reachable[-1]


class TrieSolution:
    """Approach: Trie walks from reachable starts
    Time: O(W+n*L)
    Space: O(W+n)
    """

    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        trie = {}
        for word in wordDict:
            node = trie
            for character in word:
                node = node.setdefault(character, {})
            node[None] = True
        reachable = [False] * (len(s) + 1)
        reachable[0] = True
        for start in range(len(s)):
            if not reachable[start]:
                continue
            node = trie
            for end in range(start, len(s)):
                character = s[end]
                if character not in node:
                    break
                node = node[character]
                if None in node:
                    reachable[end + 1] = True
        return reachable[-1]
