"""## Task

Find the shortest sequence from beginWord to endWord using one-letter changes.
Every word after the start must belong to wordList. Return its number of words,
or zero when unreachable.

## Hints

1. Words are vertices, and a one-letter change creates an unweighted edge.
2. Group words by wildcard patterns, such as "c*t", to find neighbors efficiently.

## Approach

### Wildcard-bucket BFS

Build wildcard buckets for the dictionary and start. Breadth-first search
stores sequence lengths, initially one. For each pattern of a dequeued word,
visit unseen bucket members, then remove that bucket. Reject an absent target.

### Bidirectional character-mutation BFS

Search from both endpoints and expand the smaller current layer. Generate one-letter
mutations directly rather than storing wildcard buckets, removing dictionary words when
discovered.

## Why it works

### Wildcard-bucket BFS

Distinct words share a pattern exactly when they differ only at that position,
so buckets supply all valid neighbors. BFS first reaches each word by a
shortest sequence. Expanding a bucket discovers all its members at the earliest
possible next layer; later scans cannot improve their distances.

### Bidirectional character-mutation BFS

Both frontiers advance by complete unit-distance layers. The first edge joining the two
explored layers yields a shortest connecting path. Dictionary removal prevents repeated
exploration without removing the opposite frontier meeting test.

## Walkthrough

With start "cat", target "dog", and dictionary ["cot","cog","dog"],
the successive words are cat, cot, cog, dog. Return 4, counting the start.

## Cost and pitfalls

For the default Wildcard-bucket BFS approach:

For N distinct words of length L, Python slicing and string hashing give
O(N * L^2) time and worst-case bucket-key storage. Bucket entries themselves
use O(N * L) references. Inputs are unchanged. Repeated bucket scans can be
quadratic in N. Returning edge count would be one smaller than the required length.

Wildcard-bucket BFS: O(N*L^2) time; O(N*L^2) space.
Bidirectional character-mutation BFS: O(26*N*L^2) time; O(N*L) space.
N is dictionary size and L word length. Slicing, concatenation, and hashing each mutation
cost O(L); the factor 26 is explicit. Both preserve the original word list.
"""

from collections import defaultdict, deque


class Solution:
    """Approach: Wildcard-bucket BFS
    Time: O(N*L^2)
    Space: O(N*L^2)
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        words.add(beginWord)
        length = len(beginWord)
        buckets = defaultdict(list)
        for word in words:
            for index in range(length):
                pattern = word[:index] + "*" + word[index + 1 :]
                buckets[pattern].append(word)
        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, distance = queue.popleft()
            if word == endWord:
                return distance
            for index in range(length):
                pattern = word[:index] + "*" + word[index + 1 :]
                for neighbor in buckets.pop(pattern, ()):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, distance + 1))
        return 0


class BidirectionalSolution:
    """Approach: Bidirectional character-mutation BFS
    Time: O(26*N*L^2)
    Space: O(N*L)
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        from string import ascii_lowercase

        unused = set(wordList)
        if endWord not in unused:
            return 0
        front, back = {beginWord}, {endWord}
        unused.discard(beginWord)
        unused.discard(endWord)
        distance = 1
        while front and back:
            if len(front) > len(back):
                front, back = back, front
            following = set()
            for word in front:
                for index in range(len(word)):
                    for letter in ascii_lowercase:
                        candidate = word[:index] + letter + word[index + 1 :]
                        if candidate in back:
                            return distance + 1
                        if candidate in unused:
                            unused.remove(candidate)
                            following.add(candidate)
            front = following
            distance += 1
        return 0
