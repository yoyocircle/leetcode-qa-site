"""
## Task

Decide whether a card multiset can be partitioned into groups of groupSize consecutive integer
values, with duplicates assigned to different groups.

## Hints

1. The smallest unused value must start a group.
2. Multiple copies of that minimum force multiple identical group starts.

## Approach

### Sorted frequency consumption

Visit card values in increasing order. If a value has c remaining copies, consume c copies of
every value in its length-g consecutive group.

### Sweep active consecutive groups

Sort distinct values. Maintain how many groups require the current value, and a queue of new-
group counts that expire after g values.

## Why it works

### Sorted frequency consumption

No smaller unused card remains, so all copies of the current minimum must begin new groups.
Failure to supply a required successor proves no valid partition exists; otherwise these forced
groups can be removed.

### Sweep active consecutive groups

Every previously opened unfinished group requires exactly one current card. Any surplus must
start new groups. A missing value while groups are active or a deficit at a value makes
completion impossible.

## Walkthrough

[1,2,3,6,2,3,4,7,8], g=3 forms [1,2,3], [2,3,4], and [6,7,8].

## Cost and pitfalls

Sorted frequency consumption: O(n log n+n*g) worst case time; O(n) space.

Sweep active consecutive groups: O(n+u log u) time; O(u) space.

Inputs are unchanged. g is groupSize and u the distinct-card count. Frequency consumption
usually performs O(n) successful removals, but its displayed bound also covers early failed
checks.
"""

from collections import Counter, deque


class Solution:
    """Approach: Sorted frequency consumption
    Time: O(n log n+n*g) worst case
    Space: O(n)
    """

    def isNStraightHand(self, hand: list[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False
        counts = Counter(hand)
        for start in sorted(counts):
            count = counts[start]
            if not count:
                continue
            for value in range(start, start + groupSize):
                if counts[value] < count:
                    return False
                counts[value] -= count
        return True


class ActiveGroupsSolution:
    """Approach: Sweep active consecutive groups
    Time: O(n+u log u)
    Space: O(u)
    """

    def isNStraightHand(self, hand: list[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False
        counts = Counter(hand)
        opened = deque()
        active = 0
        previous = None
        for value in sorted(counts):
            if active and previous is not None and value != previous + 1:
                return False
            if counts[value] < active:
                return False
            opened.append(counts[value] - active)
            active = counts[value]
            if len(opened) == groupSize:
                active -= opened.popleft()
            previous = value
        return active == 0
