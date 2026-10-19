"""## Task

Starting inside room zero, use each visited room's keys to unlock other rooms. Decide whether
every room can eventually be visited.

## Hints

1. A key is a directed edge from its room to the room it opens.
2. Visit each newly unlocked room once; repeated keys need no repeated work.

## Approach

### Iterative key-reachability DFS

Keep a stack of discovered rooms and a visited set seeded with zero. Add each unseen keyed room
immediately when pushing it.

### Layered key-reachability BFS

Use a FIFO queue and a boolean array of unlocked rooms. Queue each room once when its key first
becomes available.

## Why it works

### Iterative key-reachability DFS

Every visited room has a legal key chain from zero. Conversely, following all outgoing keys
inductively discovers every room with such a chain, so full reachability exactly decides the
task.

### Layered key-reachability BFS

The queue processes reachable rooms by increasing key-chain length. Marking upon discovery
preserves exactly the reachable set while preventing duplicate processing from repeated keys.

## Walkthrough

For rooms [[1],[2],[]], keys from zero open 1 and then 2, so return true. For [[1],[],[0]], room
2 remains unreachable.

## Cost and pitfalls

Iterative key-reachability DFS: O(V+E) time; O(V) space.
Layered key-reachability BFS: O(V+E) time; O(V) space.
The input room/key lists are unchanged. E counts key entries, including repeated keys. Neither
algorithm treats edges as undirected: possessing a key inside an unreachable room does not help.
"""

from collections import deque


class Solution:
    """Approach: Iterative key-reachability DFS
    Time: O(V+E)
    Space: O(V)
    """

    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        seen = {0}
        stack = [0]
        while stack:
            room = stack.pop()
            for key in rooms[room]:
                if key not in seen:
                    seen.add(key)
                    stack.append(key)
        return len(seen) == len(rooms)


class BreadthFirstSolution:
    """Approach: Layered key-reachability BFS
    Time: O(V+E)
    Space: O(V)
    """

    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        unlocked = [False] * len(rooms)
        unlocked[0] = True
        queue = deque([0])
        while queue:
            room = queue.popleft()
            for key in rooms[room]:
                if not unlocked[key]:
                    unlocked[key] = True
                    queue.append(key)
        return all(unlocked)
