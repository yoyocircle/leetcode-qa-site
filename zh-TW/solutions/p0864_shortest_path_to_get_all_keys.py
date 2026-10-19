"""## Task

Find the fewest steps to collect every key in a maze, passing a door only after obtaining
its matching lowercase key.

## Hints

1. A cell reached with a different key set is a different state.
2. Compress moves into shortest reachable-next-key transitions for a Dijkstra search.

## Approach

### Cell and key-mask BFS

Run BFS over cell coordinates plus a key bitmask. Doors test the incoming mask; entering a
key cell adds its bit.

### Dijkstra between newly collected keys

For each settled key-endpoint state, BFS through currently passable cells until an
uncollected key is encountered. Use those distances as weighted transitions in a
higher-level Dijkstra search.

## Why it works

### Cell and key-mask BFS

The mask records every history fact needed for future legal moves. Each edge is one step, so
first reaching the complete-key mask is the shortest collecting walk.

### Dijkstra between newly collected keys

Every collecting walk splits at newly obtained keys. The inner BFS finds shortest legal
segments before the next new key, and stopping there preserves its required mask update.
Dijkstra therefore minimizes total segment length over all key orders.

## Walkthrough

For ["@.a","##A","..b"], collect a before crossing A to reach b.

## Cost and pitfalls

Cell and key-mask BFS: O(R*C*2^K) time; O(R*C*2^K) space.
Dijkstra between newly collected keys: O(K*2^K*R*C + K^2*2^K*log(K*2^K+1)) time;
O(R*C+K^2*2^K) space.

K is key count, at most six. Inputs stay unchanged. Keys already held remain traversable; an
uncollected key must update state before continuing. The compressed variant uses fewer
endpoint states but repeats grid searches.
"""


class Solution:
    """Approach: Cell and key-mask BFS
    Time: O(R*C*2^K)
    Space: O(R*C*2^K)
    """

    def shortestPathAllKeys(self, grid: list[str]) -> int:
        from collections import deque

        rows, columns = len(grid), len(grid[0])
        goal = 0
        start = None
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char == "@":
                    start = (r, c)
                elif "a" <= char <= "z":
                    goal |= 1 << (ord(char) - ord("a"))
        queue = deque([(*start, 0, 0)])
        seen = {(*start, 0)}
        while queue:
            r, c, mask, steps = queue.popleft()
            if mask == goal:
                return steps
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if not (0 <= nr < rows and 0 <= nc < columns) or grid[nr][nc] == "#":
                    continue
                char = grid[nr][nc]
                if "A" <= char <= "Z" and not mask & (1 << (ord(char) - ord("A"))):
                    continue
                following = mask | (1 << (ord(char) - ord("a"))) if "a" <= char <= "z" else mask
                if (nr, nc, following) not in seen:
                    seen.add((nr, nc, following))
                    queue.append((nr, nc, following, steps + 1))
        return -1


class KeyDijkstraSolution:
    """Approach: Dijkstra between newly collected keys
    Time: O(K*2^K*R*C + K^2*2^K*log(K*2^K+1))
    Space: O(R*C+K^2*2^K)
    """

    def shortestPathAllKeys(self, grid: list[str]) -> int:
        from collections import deque
        from heapq import heappop, heappush

        rows, columns = len(grid), len(grid[0])
        start = next((r, c) for r in range(rows) for c in range(columns) if grid[r][c] == "@")
        goal = 0
        for row in grid:
            for char in row:
                if "a" <= char <= "z":
                    goal |= 1 << (ord(char) - ord("a"))
        best = {(*start, 0): 0}
        heap = [(0, *start, 0)]
        while heap:
            cost, r, c, mask = heappop(heap)
            if cost != best[(r, c, mask)]:
                continue
            if mask == goal:
                return cost
            queue, seen = deque([(r, c, 0)]), {(r, c)}
            while queue:
                row, column, steps = queue.popleft()
                for nr, nc in (
                    (row - 1, column),
                    (row + 1, column),
                    (row, column - 1),
                    (row, column + 1),
                ):
                    if (
                        not (0 <= nr < rows and 0 <= nc < columns)
                        or (nr, nc) in seen
                        or grid[nr][nc] == "#"
                    ):
                        continue
                    char = grid[nr][nc]
                    if "A" <= char <= "Z" and not mask & (1 << (ord(char) - ord("A"))):
                        continue
                    seen.add((nr, nc))
                    bit = 1 << (ord(char) - ord("a")) if "a" <= char <= "z" else 0
                    if bit and not mask & bit:
                        state, candidate = (nr, nc, mask | bit), cost + steps + 1
                        if candidate < best.get(state, float("inf")):
                            best[state] = candidate
                            heappush(heap, (candidate, *state))
                    else:
                        queue.append((nr, nc, steps + 1))
        return -1
