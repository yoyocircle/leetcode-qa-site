"""
## Task

Maintain an integer array under update(index,val) and inclusive sumRange(left,right) queries.
Constructors must not mutate the supplied list.

## Hints

1. A point update can be propagated as its value difference.
2. A Fenwick tree and a segment tree both summarize aligned ranges.

## Approach

### Fenwick tree with value snapshots

Keep copied values and a one-indexed Fenwick sum tree. Updates add the difference to all
containing blocks; queries subtract two prefix sums.

### Iterative segment tree

Place values in the leaves of a flat binary tree. Rebuild ancestors on updates and cover the
query range with disjoint tree nodes.

## Why it works

### Fenwick tree with value snapshots

Each Fenwick entry stores the sum over its lowbit-sized suffix block. Update ancestors are
exactly the blocks containing the index, and a prefix query partitions its range into disjoint
such blocks.

### Iterative segment tree

Every internal node equals the sum of its descendant leaves. Query boundary movement selects
disjoint fully enclosed nodes until no interval remains, so their sum equals the requested
range.

## Walkthrough

Start [1,3,5]: sumRange(0,2)=9. update(1,2) changes that result to 8 while the caller's original
list remains [1,3,5].

## Cost and pitfalls

Fenwick tree with value snapshots: O(n log n) construction; O(log n) operation time; O(n) space.

Iterative segment tree: O(n) construction; O(log n) operation time; O(n) space.

Each object owns its copied state. Query endpoints are inclusive; convert the right boundary to
exclusive in the iterative segment tree. Repeated updates replace values rather than append
differences blindly.
"""


class NumArray:
    """Approach: Fenwick tree with value snapshots
    Time: O(n log n) construction; O(log n) operation
    Space: O(n)
    """

    def __init__(self, nums: list[int]):
        self.values = nums[:]
        self.bit = [0] * (len(nums) + 1)
        for index, value in enumerate(nums, 1):
            while index < len(self.bit):
                self.bit[index] += value
                index += index & -index

    def update(self, index: int, val: int) -> None:
        difference = val - self.values[index]
        self.values[index] = val
        index += 1
        while index < len(self.bit):
            self.bit[index] += difference
            index += index & -index

    def sumRange(self, left: int, right: int) -> int:
        def prefix(end):
            answer = 0
            while end:
                answer += self.bit[end]
                end -= end & -end
            return answer

        return prefix(right + 1) - prefix(left)


class SegmentNumArray:
    """Approach: Iterative segment tree
    Time: O(n) construction; O(log n) operation
    Space: O(n)
    """

    def __init__(self, nums: list[int]):
        self.size = len(nums)
        self.tree = [0] * self.size + nums[:]
        for index in range(self.size - 1, 0, -1):
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def update(self, index: int, val: int) -> None:
        index += self.size
        self.tree[index] = val
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def sumRange(self, left: int, right: int) -> int:
        left += self.size
        right += self.size + 1
        answer = 0
        while left < right:
            if left & 1:
                answer += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                answer += self.tree[right]
            left //= 2
            right //= 2
        return answer
