"""
## Task

Decide whether the filled cells of a 9 by 9 Sudoku board obey row, column, and 3 by 3 box
uniqueness. Dots are empty; completion is not required.

## Hints

1. A filled digit belongs to three independent groups.
2. Identify a box by row // 3 and column // 3.

## Approach

### Sets of occupied digits

Keep nine sets each for rows, columns, and boxes. Reject a digit already seen in any of its
groups.

### Bit masks for occupied digits

Represent each group by a nine-bit integer. A digit maps to one bit; test with AND and record
with OR.

## Why it works

### Sets of occupied digits

Before each cell, each set contains exactly the earlier filled digits in that group. A repeated
membership is therefore exactly a rule violation.

### Bit masks for occupied digits

Each bit is set exactly when the digit has appeared in that group. Bit intersection detects
precisely the same duplicate condition as set membership.

## Walkthrough

A 5 at (0,0) and another 5 at (1,1) collide in box 0 even though their rows and columns differ.

## Cost and pitfalls

Sets of occupied digits: O(81) time; O(81) space.

Bit masks for occupied digits: O(81) time; O(27) space.

The board is unchanged. The dimensions and digit alphabet are fixed, so both methods use
constant bounded storage. Empty cells must not enter any group.
"""


class Solution:
    """Approach: Sets of occupied digits
    Time: O(81)
    Space: O(81)
    """

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows, cols, boxes = (
            [set() for _ in range(9)],
            [set() for _ in range(9)],
            [set() for _ in range(9)],
        )
        for r in range(9):
            for c in range(9):
                value = board[r][c]
                if value == ".":
                    continue
                box = r // 3 * 3 + c // 3
                if value in rows[r] or value in cols[c] or value in boxes[box]:
                    return False
                rows[r].add(value)
                cols[c].add(value)
                boxes[box].add(value)
        return True


class BitMaskSolution:
    """Approach: Bit masks for occupied digits
    Time: O(81)
    Space: O(27)
    """

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                bit = 1 << (int(board[r][c]) - 1)
                box = r // 3 * 3 + c // 3
                if rows[r] & bit or cols[c] & bit or boxes[box] & bit:
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[box] |= bit
        return True
