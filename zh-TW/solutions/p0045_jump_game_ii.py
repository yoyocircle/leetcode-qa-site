"""
## Task

Return the fewest forward jumps needed to reach the last array index. Each
value is a maximum jump distance, and reaching the last index is guaranteed.

## Hints

1. Think of positions reachable with one jump, then two, as BFS layers.
2. Represent a whole layer by its rightmost boundary.

## Approach

### Greedy jump-layer frontier

Scan all positions in the current jump layer and track the farthest index any
can reach. At the current layer's end, take one more jump and make that farthest
index the next boundary. Do not process the destination as a jumping position.

### Dynamic programming over destinations

Store the minimum jumps to each position and relax all reachable destinations from each index.
This educational baseline may time out on long dense-jump inputs.

## Why it works

### Greedy jump-layer frontier

Before increasing the jump count, every position reachable with the current
count has contributed its outgoing reach. The next boundary is thus exactly the
farthest reach with one extra jump. First reaching the destination gives a
minimum number of layers.

### Dynamic programming over destinations

Every jump enters a larger index, so processing indices in increasing order finalizes all
predecessor distances before their outgoing relaxations. The smallest relaxed distance is the
optimal jump count.

## Walkthrough

For [2,3,1,1,1], the first jump covers indices 1 and 2. Their best reach
is 4, so the second jump can reach the destination. Return 2.

## Cost and pitfalls

Default approach (Greedy jump-layer frontier):

O(n) time and O(1) space; input is unchanged. Loop only through n-2 to avoid an
extra jump at the destination. The reachability guarantee matters: this method
does not define a failure result for unreachable inputs.

Greedy jump-layer frontier: O(n) time; O(1) space.
Dynamic programming over destinations: O(n squared) time; O(n) space. Store the minimum jumps to
each position and relax all reachable destinations from each index. This educational baseline
may time out on long dense-jump inputs.
"""


class Solution:
    """Approach: Greedy jump-layer frontier
    Time: O(n)
    Space: O(1)
    """

    def jump(self, nums: list[int]) -> int:
        jumps = end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                jumps += 1
                end = farthest
        return jumps


class DynamicProgrammingSolution:
    """Approach: Dynamic programming over destinations
    Time: O(n squared)
    Space: O(n)
    """

    def jump(self, nums: list[int]) -> int:
        distance = [len(nums)] * len(nums)
        distance[0] = 0
        for i, value in enumerate(nums):
            for destination in range(i + 1, min(len(nums), i + value + 1)):
                distance[destination] = min(distance[destination], distance[i] + 1)
        return distance[-1]
