"""## Task

Turn a four-wheel decimal lock from "0000" to target using one-step wheel changes while
avoiding deadends.

## Hints

1. The lock positions form an unweighted graph with eight neighbors per state.
2. Search from both endpoints to reduce frontier size.

## Approach

### Single-source lock BFS

Use a queue of lock states and move counts. Seed visited with deadends and mark new
combinations when enqueued.

### Two frontier distance maps

Maintain independent distance maps from start and target. Expand the smaller complete
frontier and join when a generated state exists in the opposite map.

## Why it works

### Single-source lock BFS

Each edge is one turn and BFS processes nondecreasing turn counts. Blocked states never
enter the queue, so first target arrival is the shortest legal route.

### Two frontier distance maps

Each map records shortest distances from its endpoint. The first crossing while advancing
BFS layers joins two shortest prefixes; no shorter complete route could avoid an earlier
crossing.

## Walkthrough

From "0000" to "0009" with no deadends takes one backward turn.

## Cost and pitfalls

Single-source lock BFS: O(10^4) states with fixed four-digit work time; O(10^4) space.
Two frontier distance maps: O(10^4) states with fixed four-digit work time; O(10^4) space.

Inputs remain unchanged. The wheel slices and hashing cost O(4), included in the fixed-width
work. A dead starting position is invalid even when it equals target.
"""


class Solution:
    """Approach: Single-source lock BFS
    Time: O(10^4) states with fixed four-digit work
    Space: O(10^4)
    """

    def openLock(self, deadends: list[str], target: str) -> int:
        from collections import deque

        seen = set(deadends)
        if "0000" in seen:
            return -1
        seen.add("0000")
        queue = deque([("0000", 0)])
        while queue:
            state, steps = queue.popleft()
            if state == target:
                return steps
            for index in range(4):
                for change in (-1, 1):
                    following = (
                        state[:index] + str((int(state[index]) + change) % 10) + state[index + 1 :]
                    )
                    if following not in seen:
                        seen.add(following)
                        queue.append((following, steps + 1))
        return -1


class BidirectionalSolution:
    """Approach: Two frontier distance maps
    Time: O(10^4) states with fixed four-digit work
    Space: O(10^4)
    """

    def openLock(self, deadends: list[str], target: str) -> int:
        blocked = set(deadends)
        if "0000" in blocked or target in blocked:
            return -1
        if target == "0000":
            return 0
        front, back = {"0000"}, {target}
        first, second = {"0000": 0}, {target: 0}
        while front and back:
            if len(front) > len(back):
                front, back, first, second = back, front, second, first
            following = set()
            for state in front:
                for index in range(4):
                    for change in (-1, 1):
                        other = (
                            state[:index]
                            + str((int(state[index]) + change) % 10)
                            + state[index + 1 :]
                        )
                        if other in blocked or other in first:
                            continue
                        if other in second:
                            return first[state] + 1 + second[other]
                        first[other] = first[state] + 1
                        following.add(other)
            front = following
        return -1
