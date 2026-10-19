"""## Task

Reach the final square in the fewest dice rolls on a boustrophedon board, applying at most
one snake or ladder per move.

## Hints

1. Map a square number to its alternating row direction.
2. After applying a jump, do not chain another jump during the same roll.

## Approach

### BFS over post-jump squares

Construct each outgoing dice edge on demand, applying its landing-cell jump exactly once.
BFS counts rolls and visits each resulting square once.

### Repeated relaxation of fixed move edges

Materialize up to six directed move edges per square and apply Bellman-Ford relaxation,
stopping at a fixed point.

## Why it works

### BFS over post-jump squares

Each edge represents precisely one legal roll, regardless of jump distance. BFS therefore
finds a shortest roll sequence and exhaustion proves the goal unreachable.

### Repeated relaxation of fixed move edges

A shortest walk can be chosen simple in the post-jump state graph and thus uses at most n²-1
edges. That many relaxation rounds cover it, including backward snakes and cycles.

## Walkthrough

On an empty 2x2 board, square 1 reaches square 4 in one roll.

## Cost and pitfalls

BFS over post-jump squares: O(n^2) time; O(n^2) space.
Repeated relaxation of fixed move edges: O(n^4) time; O(n^2) space.

Both preserve the board. Relaxation is a slower educational baseline with a conservative
quartic side-length bound; BFS is preferred. Count rolls, not squares skipped by a ladder.
"""


class Solution:
    """Approach: BFS over post-jump squares
    Time: O(n^2)
    Space: O(n^2)
    """

    def snakesAndLadders(self, board: list[list[int]]) -> int:
        from collections import deque

        n = len(board)

        def destination(square):
            row, column = divmod(square - 1, n)
            value = board[n - row - 1][column if row % 2 == 0 else n - column - 1]
            return square if value == -1 else value

        queue, seen = deque([(1, 0)]), {1}
        while queue:
            square, rolls = queue.popleft()
            if square == n * n:
                return rolls
            for landing in range(square + 1, min(square + 6, n * n) + 1):
                following = destination(landing)
                if following not in seen:
                    seen.add(following)
                    queue.append((following, rolls + 1))
        return -1


class RelaxationSolution:
    """Approach: Repeated relaxation of fixed move edges
    Time: O(n^4)
    Space: O(n^2)
    """

    def snakesAndLadders(self, board: list[list[int]]) -> int:
        n = len(board)
        edges = []
        for start in range(1, n * n):
            for square in range(start + 1, min(start + 6, n * n) + 1):
                row, column = divmod(square - 1, n)
                value = board[n - row - 1][column if row % 2 == 0 else n - column - 1]
                edges.append((start, square if value == -1 else value))
        distance = [float("inf")] * (n * n + 1)
        distance[1] = 0
        for _ in range(n * n - 1):
            changed = False
            for a, b in edges:
                if distance[a] + 1 < distance[b]:
                    distance[b] = distance[a] + 1
                    changed = True
            if not changed:
                break
        return -1 if distance[-1] == float("inf") else distance[-1]
