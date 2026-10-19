"""## Task

Find every dictionary word formable by an orthogonal path through a character board. A cell
cannot repeat within one word path; return each word at most once.

## Hints

1. Many words share prefixes, so searching them independently repeats work.
2. A trie can discard a branch as soon as no dictionary prefix matches.

## Approach

### Shared trie search with pruning

Insert words into a trie, then backtrack board paths through trie edges. Consume a terminal
marker after reporting a word and delete exhausted trie branches.

### Independent word searches

For each word run an independent path-local DFS and stop at its first success. This educational
baseline uses less shared dictionary state but repeats work across common prefixes.

## Why it works

### Shared trie search with pruning

The current trie node represents exactly the board path's prefix. Missing edges cannot lead to a
word. Terminal removal suppresses repeated discoveries, while pruning only empty branches
preserves undiscovered words.

### Independent word searches

Every word search enumerates exactly legal nonrepeating board paths from every possible start.
Reporting that word after any success therefore matches dictionary membership in the board
language.

## Walkthrough

For board [["c","a"],["t","r"]] and words ["car","cat","art"], "car" and "art" follow orthogonal
paths; "cat" would require a diagonal move.

## Cost and pitfalls

Shared trie search with pruning: O(S + R*C*4^L) loose bound time; O(S+L) auxiliary plus output
space.
Independent word searches: O(W*R*C*4^L) loose bound; may time out time; O(L) auxiliary plus
output space.
The board and words are unchanged. S is total dictionary characters and L maximum word length,
at most 10, so recursive path depth is bounded. The baseline may time out at the full dictionary
limit.
"""


class Solution:
    """Approach: Shared trie search with pruning
    Time: O(S + R*C*4^L) loose bound
    Space: O(S+L) auxiliary plus output
    """

    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        trie = {}
        for word in words:
            node = trie
            for char in word:
                node = node.setdefault(char, {})
            node[None] = word
        rows, cols = len(board), len(board[0])
        used, result = set(), []

        def visit(row, col, parent):
            char = board[row][col]
            if char not in parent:
                return
            node = parent[char]
            if None in node:
                result.append(node.pop(None))
            used.add((row, col))
            for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in used:
                    visit(nr, nc, node)
            used.remove((row, col))
            if not node:
                del parent[char]

        for row in range(rows):
            for col in range(cols):
                visit(row, col, trie)
        return result


class PerWordSolution:
    """Approach: Independent word searches
    Time: O(W*R*C*4^L) loose bound; may time out
    Space: O(L) auxiliary plus output
    """

    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        rows, cols = len(board), len(board[0])

        def exists(word):
            used = set()

            def visit(row, col, index):
                if board[row][col] != word[index]:
                    return False
                if index == len(word) - 1:
                    return True
                used.add((row, col))
                found = any(
                    visit(nr, nc, index + 1)
                    for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1))
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in used
                )
                used.remove((row, col))
                return found

            return any(visit(row, col, 0) for row in range(rows) for col in range(cols))

        return [word for word in words if exists(word)]
