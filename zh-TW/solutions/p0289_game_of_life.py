"""
## Task

Advance a finite binary Game of Life board by one simultaneous generation in place. A live cell
survives with two or three live neighbors; a dead cell is born with three.

## Hints

1. Every neighbor count must use the old generation.
2. Two bits can store old and new state in the same cell.

## Approach

### Two-bit in-place generation

Keep the old state in bit zero and write the next state in bit one. After all neighbor counts,
shift every cell right once.

### Snapshot neighbor counting

Copy the original board, count neighbors from the copy, and write each next-state value directly
into the original.

## Why it works

### Two-bit in-place generation

Masking neighbor values with one always reads the original state regardless of earlier writes.
The second bit stores exactly the transition rule, and shifting commits the simultaneous
generation.

### Snapshot neighbor counting

The snapshot never changes, so every transition uses precisely the same original generation.
Applying the rule independently to each cell therefore realizes a simultaneous update.

## Walkthrough

A vertical blinker [[0,1,0],[0,1,0],[0,1,0]] becomes the horizontal row
[[0,0,0],[1,1,1],[0,0,0]].

## Cost and pitfalls

Two-bit in-place generation: O(mn) time; O(1) space.

Snapshot neighbor counting: O(mn) time; O(mn) space.

Both methods mutate the existing board and row objects. Out-of-bounds neighbors are dead.
Counting already-updated binary cells without encoding or a snapshot would be incorrect.
"""


class Solution:
    """Approach: Two-bit in-place generation
    Time: O(mn)
    Space: O(1)
    """

    def gameOfLife(self, board: list[list[int]]) -> None:
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                live = sum(
                    board[r][c] & 1
                    for r in range(max(0, row - 1), min(rows, row + 2))
                    for c in range(max(0, col - 1), min(cols, col + 2))
                    if (r, c) != (row, col)
                )
                if live == 3 or (board[row][col] & 1 and live == 2):
                    board[row][col] |= 2
        for row in board:
            for col in range(cols):
                row[col] >>= 1


class SnapshotSolution:
    """Approach: Snapshot neighbor counting
    Time: O(mn)
    Space: O(mn)
    """

    def gameOfLife(self, board: list[list[int]]) -> None:
        old = [row[:] for row in board]
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                live = 0
                for dr, dc in (
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ):
                    r, c = row + dr, col + dc
                    if 0 <= r < rows and 0 <= c < cols:
                        live += old[r][c]
                board[row][col] = int(live == 3 or (old[row][col] == 1 and live == 2))
