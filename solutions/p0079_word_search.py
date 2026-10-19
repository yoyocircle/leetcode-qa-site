"""## Task

Decide whether a word can be formed by an orthogonal path through a character
grid. Each cell can be used at most once in that path.

## Hints

1. Try a path starting from each possible first-letter cell.
2. A cell is visited only for the current path, not permanently for the whole search.

## Approach

### Path-set backtracking

Backtrack over row, column, and matched-word index. Reject out-of-bounds,
already-used, or mismatching cells. Add a matching cell to the current path,
try its four neighbors, then remove it even if a branch succeeds.

### Iterative path bitmasks

Keep candidate paths on an explicit stack with a bitmask of used cells. Each branch receives its
own integer mask, so it needs no shared-path undo. The official grid has at most 36 cells,
bounding integer-mask size.

## Why it works

### Path-set backtracking

Each recursive step adds exactly one matching, unused neighboring cell.
The search therefore generates exactly the legal word paths from each start.
Path-local undo lets another branch use cells that an earlier branch abandoned.

### Iterative path bitmasks

The mask records exactly the cells used by a candidate matching prefix. Extending to an unused
matching neighbor generates precisely the legal next paths. Exhausting all starts and extensions
is complete.

## Walkthrough

For board [["A","B"],["C","D"]], "ABDC" follows all four cells and succeeds.
"ABA" fails because returning to the first A would reuse its cell.

## Cost and pitfalls

Default approach costs and behavior:

A loose upper bound is O(rows * cols * 4^L) time for word length L, with
O(L) path and recursion space. Board and word are unchanged on success or failure.
The official word limit keeps recursion shallow. A global visited set would
incorrectly exclude cells from different candidate paths.

Alternative tradeoff: O(R*C*4^L) loose time bound and O(L) auxiliary stack space.
Only a bounded number of sibling states remains pending per path depth; each mask
fits the official grid's at-most-36-cell domain.
"""


class Solution:
    """Approach: Path-set backtracking
    Time: O(R*C*4^L) loose bound
    Space: O(L)
    """

    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        path = set()

        def visit(row, col, index):
            if not (0 <= row < rows and 0 <= col < cols):
                return False
            if (row, col) in path or board[row][col] != word[index]:
                return False
            if index == len(word) - 1:
                return True
            path.add((row, col))
            found = any(
                visit(row + dr, col + dc, index + 1)
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
            )
            path.remove((row, col))
            return found

        return any(visit(row, col, 0) for row in range(rows) for col in range(cols))


class BitmaskSearchSolution:
    """Approach: Iterative path bitmasks
    Time: O(R*C*4^L) loose bound under bounded grid size
    Space: O(L) under the bounded grid size
    """

    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != word[0]:
                    continue
                stack = [(row, col, 0, 1 << (row * cols + col))]
                while stack:
                    r, c, index, mask = stack.pop()
                    if index == len(word) - 1:
                        return True
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols:
                            bit = 1 << (nr * cols + nc)
                            if not mask & bit and board[nr][nc] == word[index + 1]:
                                stack.append((nr, nc, index + 1, mask | bit))
        return False
