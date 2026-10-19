"""## Task

Store words and answer membership queries where a dot matches exactly one
arbitrary letter. All other query letters must match themselves.

## Hints

1. Reuse a trie for shared prefixes.
2. A wildcard means exploring all outgoing edges at the current depth.

## Approach

### Trie frontier

Insertion builds a normal trie. Search maintains the frontier of nodes compatible
with the consumed query prefix. A letter follows that edge from each frontier
node; a dot expands all children. At the end, require a terminal node.

### Length-grouped word sets

Group distinct stored words by length. Search compares the pattern only with words of that
length, accepting a position when letters match or the query has a dot. This simpler baseline
can be slower than prefix pruning.

## Why it works

### Trie frontier

Initially the root matches the empty prefix. Each transition enumerates exactly
the edges accepted by the next pattern character. By induction, the frontier
contains precisely the compatible prefixes; terminal membership enforces full-word
length.

### Length-grouped word sets

Length filtering enforces the number of matched characters. The positional predicate accepts
exactly the words allowed by dot semantics, so finding any accepted candidate is equivalent to
dictionary membership.

## Walkthrough

After adding "cat" and "car", search("ca.") is True, search("c..") is True,
and search("ca") is False unless "ca" was also added.

## Cost and pitfalls

Default approach costs and behavior:

Add takes O(L) expected time and at most O(L) new nodes. Search without dots
takes O(L); with dots it may visit O(T) nodes and use O(T) frontier space for
T stored trie nodes. The dictionary owns its mutations. A dot is one character,
not zero or many, and successful prefix matching alone is insufficient.

Alternative tradeoff: O(L) expected add; O(W_L*L) search time; O(S) space.
"""

from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = {}
        self.terminal = False


class WordDictionary:
    """Approach: Trie frontier
    Time: O(L) add; O(T) wildcard search
    Space: O(T)
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.terminal = True

    def search(self, word: str) -> bool:
        frontier = [self.root]
        for char in word:
            if char == ".":
                frontier = [child for node in frontier for child in node.children.values()]
            else:
                frontier = [node.children[char] for node in frontier if char in node.children]
            if not frontier:
                return False
        return any(node.terminal for node in frontier)


class LengthBucketsDictionary:
    """Approach: Length-grouped word sets
    Time: O(L) expected add; O(W_L*L) search
    Space: O(S)
    """

    def __init__(self):
        self.words = defaultdict(set)

    def addWord(self, word: str) -> None:
        self.words[len(word)].add(word)

    def search(self, word: str) -> bool:
        return any(
            all(query == "." or query == char for query, char in zip(word, candidate, strict=True))
            for candidate in self.words[len(word)]
        )
