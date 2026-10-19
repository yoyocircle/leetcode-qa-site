"""## Task

Return every shortest one-letter word transformation sequence, using dictionary words after
the starting word.

## Hints

1. BFS determines shortest distances, but a word can have several shortest parents.
2. Reconstruct paths only after the shortest-parent DAG is complete.

## Approach

### BFS predecessor DAG and iterative reconstruction

Run BFS once and retain every predecessor exactly one distance layer earlier. Stop expanding
at target depth, then enumerate DAG paths with an explicit stack.

### Layered queues of complete partial routes

Store complete partial routes in a frontier, and remove discovered dictionary words only
after the entire layer. Return all target routes in the first successful layer.

## Why it works

### BFS predecessor DAG and iterative reconstruction

BFS distances are shortest. Retained edges increase distance by exactly one, so every
reconstructed route is shortest and acyclic. Every shortest route supplies such predecessor
edges and is therefore enumerated.

### Layered queues of complete partial routes

Whole-layer deletion preserves different shortest routes arriving at the same word. Later
layers cannot improve their distance. Thus the first target layer contains exactly all
shortest routes.

## Walkthrough

From "hit" to "cog" through ["hot","dot","dog","lot","log","cog"], the two shortest routes
branch through dot/dog and lot/log.

## Cost and pitfalls

BFS predecessor DAG and iterative reconstruction: O(26*N*L^2 + P*D^2) time; O(N*L+E+P*D^2)
space.
Layered queues of complete partial routes: O(H*26*L^2 + H*D) time; O(H*D+N*L) space.

N words have length L, D is shortest-route word count, P output-route count, E
shortest-parent edges, and H the number of generated partial routes. Path copying costs O(D)
references per extension. The complete-route baseline may use exponentially more time/memory
and time out; prefer the DAG default. Inputs stay unchanged.
"""


class Solution:
    """Approach: BFS predecessor DAG and iterative reconstruction
    Time: O(26*N*L^2 + P*D^2)
    Space: O(N*L+E+P*D^2)
    """

    def findLadders(self, beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
        from collections import deque
        from string import ascii_lowercase

        words = set(wordList)
        if endWord not in words:
            return []
        distance = {beginWord: 0}
        parents = {}
        queue = deque([beginWord])
        while queue:
            word = queue.popleft()
            if endWord in distance and distance[word] >= distance[endWord]:
                continue
            for index in range(len(word)):
                for letter in ascii_lowercase:
                    other = word[:index] + letter + word[index + 1 :]
                    if other not in words:
                        continue
                    if other not in distance:
                        distance[other] = distance[word] + 1
                        queue.append(other)
                    if distance[other] == distance[word] + 1:
                        parents.setdefault(other, []).append(word)
        if endWord not in distance:
            return []
        answers = []
        stack = [(endWord, [endWord])]
        while stack:
            word, path = stack.pop()
            if word == beginWord:
                answers.append(path[::-1])
            else:
                stack.extend((parent, path + [parent]) for parent in parents[word])
        return answers


class PathQueueSolution:
    """Approach: Layered queues of complete partial routes
    Time: O(H*26*L^2 + H*D)
    Space: O(H*D+N*L)
    """

    def findLadders(self, beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
        from string import ascii_lowercase

        unused = set(wordList)
        if endWord not in unused:
            return []
        unused.discard(beginWord)
        frontier = [[beginWord]]
        while frontier:
            answers = [path for path in frontier if path[-1] == endWord]
            if answers:
                return answers
            following, discovered = [], set()
            for path in frontier:
                word = path[-1]
                for index in range(len(word)):
                    for letter in ascii_lowercase:
                        other = word[:index] + letter + word[index + 1 :]
                        if other in unused:
                            following.append(path + [other])
                            discovered.add(other)
            unused.difference_update(discovered)
            frontier = following
        return []
