"""## Task

Replace each word in a sentence by the shortest dictionary root that is its
prefix. Leave a word unchanged when no root matches. Preserve word order.

## Hints

1. The first terminal node reached in a prefix trie is the shortest root.
2. A simpler comparison strategy checks roots in increasing length order.

## Approach

### Prefix trie

Insert roots into nested dictionaries with a terminal marker. For each word,
walk its characters from the trie root. Stop at the first terminal node,
or abandon the search on a missing edge. Slice only the selected replacement.

### Length-ordered root scan

Sort a copy of the dictionary by root length. For each word, choose the first
root satisfying startswith. Break early when a root is longer than the word.
This avoids a trie but repeatedly compares roots and is a slower learning
baseline for large dictionaries and long sentences.

## Why it works

A trie path spells exactly a dictionary prefix. The first terminal along a
word's path has the smallest possible length. The sorted scan tests candidate
lengths in increasing order, so its first matching root is also shortest.
If neither finds a root, no dictionary prefix exists and the original word stays.

## Walkthrough

With roots ["a", "ab", "cat"] and sentence "about cattle dog", the result
is "a cat dog". Both a and ab match about, but only the shortest is selected.

## Cost and pitfalls

Let D be total dictionary characters, R its root count, W the number of words,
and L the sentence length. Trie construction and replacement take O(D+L) time
and O(D+L) space including split words and output. The scan takes
O(R log R+W*D+L) worst-case time and O(R+L) extra space. Length sorting uses
constant-size keys, but each startswith comparison can inspect its whole root.
The dictionary and sentence are unchanged. Check the terminal before trying
longer roots; replacing by any matching prefix is not sufficient.
"""


class Solution:
    """Approach: Prefix trie
    Time: O(D+L)
    Space: O(D+L), including split words and output
    """

    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        trie = {}
        for root in dictionary:
            node = trie
            for char in root:
                node = node.setdefault(char, {})
            node[""] = True
        result = []
        for word in sentence.split():
            node = trie
            replacement = word
            for end, char in enumerate(word, 1):
                if char not in node:
                    break
                node = node[char]
                if "" in node:
                    replacement = word[:end]
                    break
            result.append(replacement)
        return " ".join(result)


class SortedRootsSolution:
    """Approach: Length-ordered root scan
    Time: O(R log R+W*D+L); slower dictionary-scan baseline
    Space: O(R+L), including output
    """

    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        roots = sorted(dictionary, key=len)
        words = sentence.split()
        for index, word in enumerate(words):
            for root in roots:
                if len(root) > len(word):
                    break
                if word.startswith(root):
                    words[index] = root
                    break
        return " ".join(words)
