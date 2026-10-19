"""## Task

Write a string down and diagonally up across the requested number of rows,
then read the rows from top to bottom. Return that reading order.

## Hints

1. The active row moves by one and reverses direction at either endpoint.
2. For r > 1, the row pattern repeats every 2*r-2 input characters.

## Approach

### Row buffers

Append each character to its current row. Reverse the step at row zero and at
row r-1, then concatenate the buffers. Return s directly if only one row is
requested or there are at least as many rows as characters.

### Cycle indices

Visit one output row at a time. Its vertical entries are at row + cycle*t.
Interior rows also have a diagonal entry at cycle*(t+1)-row. Append that entry
only when it exists; endpoint rows have no separate diagonal entry.

## Why it works

Row buffers simulate every move, so each buffer contains exactly its row in
input order. Cycle indices enumerate the same positions algebraically. Their
two progressions are disjoint for interior rows, and every input position
belongs to one row. Both therefore produce the requested row-major reading.

## Walkthrough

For "ABCDEFG" with three rows, the buffers are "AE", "BDF", and "CG".
The result is "AEBDFCG". The cycle length is four; row one takes indices
1, 3, and 5, which explains its alternating vertical and diagonal entries.

## Cost and pitfalls

For n characters, both approaches take O(n) time and O(n) output/buffer space.
The row-buffer version also allocates r lists, but the early return ensures
r < n when they are allocated. Cycle indices use O(1) working state besides
their O(n) output list and joined string. Strings are not modified.
Do not append the diagonal entry for the first or last row: it would duplicate
an endpoint. Handle one row before computing the zero cycle length.
"""


class Solution:
    """Approach: Row buffers
    Time: O(n)
    Space: O(n), including output buffers
    """

    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s
        rows = [[] for _ in range(numRows)]
        row, step = 0, 1
        for char in s:
            rows[row].append(char)
            if row == 0:
                step = 1
            elif row == numRows - 1:
                step = -1
            row += step
        return "".join("".join(row) for row in rows)


class CycleSolution:
    """Approach: Cycle indices
    Time: O(n)
    Space: O(n) output storage; O(1) other state
    """

    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s
        cycle = 2 * numRows - 2
        result = []
        for row in range(numRows):
            for vertical in range(row, len(s), cycle):
                result.append(s[vertical])
                diagonal = vertical + cycle - 2 * row
                if 0 < row < numRows - 1 and diagonal < len(s):
                    result.append(s[diagonal])
        return "".join(result)
