"""## Task

Return all ways to place n queens on an n-by-n board so no two share a row,
column, or diagonal. Each answer is a list of board-row strings.

## Hints

1. Place exactly one queen per row.
2. Cells on a diagonal share either row+column or row-column.

## Approach

### Column and diagonal sets

Backtrack row by row with occupied-column and two diagonal sets. For each safe
column, record the queen, mark its three constraints, recurse, then undo them.
Construct board strings only for complete arrangements.

### Shifted attack masks

Represent columns and diagonal attacks on the next row with bitmasks. Intersect their
complements with the n-column mask to obtain legal positions, then take one low bit at a time.
Diagonal masks shift when descending a row.

## Why it works

### Column and diagonal sets

One queen per row satisfies the row constraint automatically. The three sets
exclude exactly the remaining attacks. Every valid board has one sequence of
row-wise column choices, so the recursion visits it once.

### Shifted attack masks

A queen's two diagonal attacks move one column in opposite directions in the next row. Shifting
masks therefore maintains exactly the forbidden columns, and choosing only free bits enumerates
every safe board once.

## Walkthrough

For n=4, columns [1,3,0,2] give [".Q..","...Q","Q...","..Q."].
The other solution uses columns [2,0,3,1]. For n=2 there is no solution.

## Cost and pitfalls

Default approach costs and behavior:

A loose search bound is O(n * n!), plus O(S * n^2) to materialize S boards.
Auxiliary search space is O(n); output space is O(S * n^2). All state is local.
Undo all three constraints after recursion. Store diagonal identifiers separately:
row+column and row-column describe different diagonal families.

Alternative tradeoff: O(n*n! + S*n^2) loose bound time; O(n) auxiliary; O(S*n^2) output space.
"""


class Solution:
    """Approach: Column and diagonal sets
    Time: O(n*n! + S*n^2) loose bound
    Space: O(n) auxiliary; O(S*n^2) output
    """

    def solveNQueens(self, n: int) -> list[list[str]]:
        result = []
        path = []
        columns, ascending, descending = set(), set(), set()

        def visit(row):
            if row == n:
                result.append(["." * col + "Q" + "." * (n - col - 1) for col in path])
                return
            for col in range(n):
                if col in columns or row + col in ascending or row - col in descending:
                    continue
                columns.add(col)
                ascending.add(row + col)
                descending.add(row - col)
                path.append(col)
                visit(row + 1)
                path.pop()
                columns.remove(col)
                ascending.remove(row + col)
                descending.remove(row - col)

        visit(0)
        return result


class BitmaskQueensSolution:
    """Approach: Shifted attack masks
    Time: O(n*n! + S*n^2) loose bound
    Space: O(n) auxiliary; O(S*n^2) output
    """

    def solveNQueens(self, n: int) -> list[list[str]]:
        full = (1 << n) - 1
        result, path = [], []

        def visit(columns, left, right):
            if columns == full:
                result.append(["." * col + "Q" + "." * (n - col - 1) for col in path])
                return
            free = full & ~(columns | left | right)
            while free:
                bit = free & -free
                free -= bit
                path.append(bit.bit_length() - 1)
                visit(columns | bit, ((left | bit) << 1) & full, (right | bit) >> 1)
                path.pop()

        visit(0, 0, 0)
        return result
