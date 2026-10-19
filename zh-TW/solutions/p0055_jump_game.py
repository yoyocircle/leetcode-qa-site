"""
## Task

Each array value is the maximum forward jump from that position. Starting at
index 0, decide whether the final index can be reached.

## Hints

1. All reachable positions form a prefix as you scan.
2. Keep only the farthest reachable position instead of all possible paths.

## Approach

### Forward reachable frontier

Scan left to right with a farthest-reachable boundary. If the current index lies
beyond it, return False. Otherwise extend the boundary using the current index
plus its jump length.

### Backward goal movement

Start with the final index as the goal. Move the goal left whenever an earlier position can jump
to it.

## Why it works

### Forward reachable frontier

A jump permits any shorter distance, so reaching an endpoint also makes all
intermediate positions reachable. Processing a reachable position adds exactly
the interval it can reach. The maintained prefix is therefore all reachability
known from processed positions.

### Backward goal movement

The goal is always a position known to reach the end. Any earlier index that reaches the goal
also reaches the end, and any valid start-to-end path must eventually join this backward
reachable set.

## Walkthrough

For [2,0,1,0], index 0 reaches through 2. Index 2 extends reach to 3,
so the answer is True. For [1,0,2], index 2 lies beyond reach 1: False.

## Cost and pitfalls

Default approach (Forward reachable frontier):

O(n) time and O(1) space; input is unchanged. Never use a jump from an unreachable
position to extend reach. A one-element array is already at the destination,
even when its value is zero. This asks for existence, not the number of jumps.

Forward reachable frontier: O(n) time; O(1) space.
Backward goal movement: O(n) time; O(1) space. Start with the final index as the goal. Move the
goal left whenever an earlier position can jump to it.
"""


class Solution:
    """Approach: Forward reachable frontier
    Time: O(n)
    Space: O(1)
    """

    def canJump(self, nums: list[int]) -> bool:
        farthest = 0
        for i, distance in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + distance)
        return True


class BackwardSolution:
    """Approach: Backward goal movement
    Time: O(n)
    Space: O(1)
    """

    def canJump(self, nums: list[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0
