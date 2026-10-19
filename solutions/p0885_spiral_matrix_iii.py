"""
## Task

Start at (rStart,cStart) in a rows by cols grid and walk an expanding clockwise spiral, even
outside the grid. Return in-grid coordinates in visit order.

## Hints

1. Step lengths are 1,1,2,2,3,3,... in east,south,west,north order.
2. Each cell also has a closed-form rank on its square ring around the start.

## Approach

### Expanding step simulation

Walk two directions at each step length and record only coordinates inside the grid.

### Sort by square-ring spiral rank

Compute each cell's Chebyshev ring and offset along that ring, then sort all in-grid cells by
that rank. This avoids walking outside a very thin grid.

## Why it works

### Expanding step simulation

Pairs of equal-length perpendicular legs complete successively larger square boundaries around
the start. Every grid coordinate eventually lies on a visited boundary and is recorded exactly
once.

### Sort by square-ring spiral rank

Ring k starts after (2k-1)^2 visited positions. The four edge formulas assign offsets 0 through
8k-1 in clockwise order, so rank sorting exactly reproduces the infinite spiral subsequence.

## Walkthrough

rows=1, cols=4, start=(0,0) returns [[0,0],[0,1],[0,2],[0,3]], although the underlying walk
spends time outside the only row.

## Cost and pitfalls

Expanding step simulation: O(R squared), R=max(rows,cols) time; O(1) auxiliary plus output
space.

Sort by square-ring spiral rank: O(rows*cols log(rows*cols)) time; O(rows*cols) space.

The output contains exactly rows*cols distinct coordinates. The simulation may continue a short
leg after the last in-grid visit, but cannot record a coordinate twice.
"""


class Solution:
    """Approach: Expanding step simulation
    Time: O(R squared), R=max(rows,cols)
    Space: O(1) auxiliary plus output
    """

    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> list[list[int]]:
        answer = [[rStart, cStart]]
        row, col, length, direction = rStart, cStart, 1, 0
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        while len(answer) < rows * cols:
            for _ in range(2):
                dr, dc = directions[direction % 4]
                for _ in range(length):
                    row, col = row + dr, col + dc
                    if 0 <= row < rows and 0 <= col < cols:
                        answer.append([row, col])
                direction += 1
            length += 1
        return answer


class RankSolution:
    """Approach: Sort by square-ring spiral rank
    Time: O(rows*cols log(rows*cols))
    Space: O(rows*cols)
    """

    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> list[list[int]]:
        def rank(cell):
            dr, dc = cell[0] - rStart, cell[1] - cStart
            ring = max(abs(dr), abs(dc))
            if ring == 0:
                return 0
            if dc == ring and dr > -ring:
                offset = dr + ring - 1
            elif dr == ring:
                offset = 2 * ring + ring - 1 - dc
            elif dc == -ring:
                offset = 4 * ring + ring - 1 - dr
            else:
                offset = 6 * ring + dc + ring - 1
            return (2 * ring - 1) ** 2 + offset

        cells = [[row, col] for row in range(rows) for col in range(cols)]
        cells.sort(key=rank)
        return cells
