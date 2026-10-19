"""
## Task

Find the longest contiguous subarray containing at most two different fruit types. Each value
names a fruit type.

## Hints

1. Keep a window with at most two distinct values.
2. Alternatively track the last run of one value and the preceding two-type suffix.

## Approach

### Frequency-map window

Count the current window and shrink until it contains at most two types.

### Last-run state compression

Track the latest type, the other type, the length of the latest equal run, and the best two-type
suffix ending here.

## Why it works

### Frequency-map window

After shrinking, every suffix of the current window is valid and every earlier start would
include a third type. Recording the largest window therefore captures the optimum.

### Last-run state compression

A third type can extend only the immediately preceding equal run. A known type extends the whole
suffix. Updating the latest run preserves exactly the information needed for the next element.

## Walkthrough

For [1,2,3,2,2], introducing 3 discards the initial 1. The suffix [2,3,2,2] uses two types and
has length 4.

## Cost and pitfalls

Frequency-map window: O(n) expected time; O(1) space.

Last-run state compression: O(n) time; O(1) space.

Inputs are unchanged. Zero-count keys must leave the frequency map. The compressed method tracks
a contiguous run, not the total count of the latest type.
"""


class Solution:
    """Approach: Frequency-map window
    Time: O(n) expected
    Space: O(1)
    """

    def totalFruit(self, fruits: list[int]) -> int:
        counts = {}
        left = best = 0
        for right, value in enumerate(fruits):
            counts[value] = counts.get(value, 0) + 1
            while len(counts) > 2:
                outgoing = fruits[left]
                counts[outgoing] -= 1
                if counts[outgoing] == 0:
                    del counts[outgoing]
                left += 1
            best = max(best, right - left + 1)
        return best


class RunStateSolution:
    """Approach: Last-run state compression
    Time: O(n)
    Space: O(1)
    """

    def totalFruit(self, fruits: list[int]) -> int:
        latest = other = None
        run = current = best = 0
        for value in fruits:
            current = current + 1 if value in (latest, other) else run + 1
            if value == latest:
                run += 1
            else:
                other, latest = latest, value
                run = 1
            best = max(best, current)
        return best
