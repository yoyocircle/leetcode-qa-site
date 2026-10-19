"""## Task

Support inserting lowercase words, testing exact membership, and testing whether
any stored word starts with a given prefix.

## Hints

1. Share the storage for common prefixes.
2. Reaching a prefix node does not necessarily mean a complete word ends there.

## Approach

### Sparse dictionary trie

Each trie node owns a map of character edges and a terminal flag. Insertion
walks or creates the word's path and marks its endpoint terminal. A shared
walking helper supports both exact search and prefix search.

### Fixed-alphabet trie

Use a fixed array of 26 child pointers in every node, indexed by lowercase letter offset. This
avoids hash lookup but reserves empty slots for absent edges. Each node retains a terminal flag.

## Why it works

### Sparse dictionary trie

The path from the root to a node spells exactly one prefix. Existence of that
path proves prefix membership. The terminal flag separately records whether an
inserted word ends there, so exact membership remains distinct.

### Fixed-alphabet trie

Array index i names exactly the edge for letter chr(i+97). Walking characters therefore follows
the same unique prefix path as a map trie, while terminal state distinguishes a full word from a
prefix.

## Walkthrough

Insert "car". startsWith("ca") is True, while search("ca") is False.
After inserting "ca", both queries are True without duplicating the shared path.

## Cost and pitfalls

Default approach costs and behavior:

Each operation takes O(L) expected time for L characters. Total storage is O(S)
nodes/edges for S inserted characters before prefix sharing. Methods mutate only
the trie's owned state. Repeated insertion is idempotent. Iterative walks support
long words without recursion limits. Avoid treating every prefix as a complete word.

Alternative tradeoff: O(L) per operation time; O(26*S) total child slots space.
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.terminal = False


class Trie:
    """Approach: Sparse dictionary trie
    Time: O(L) expected per operation
    Space: O(S) total nodes
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.terminal = True

    def _find(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            node = node.children.get(char)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.terminal

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None


class ArrayTrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.terminal = False


class ArrayTrie:
    """Approach: Fixed-alphabet trie
    Time: O(L) per operation
    Space: O(26*S) total child slots
    """

    def __init__(self):
        self.root = ArrayTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            index = ord(char) - ord("a")
            if node.children[index] is None:
                node.children[index] = ArrayTrieNode()
            node = node.children[index]
        node.terminal = True

    def _find(self, text):
        node = self.root
        for char in text:
            node = node.children[ord(char) - ord("a")]
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.terminal

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None
