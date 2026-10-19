"""## Task

Rearrange a lowercase string so adjacent characters differ. Return any valid rearrangement, or
the empty string when none exists.

## Hints

1. A most frequent character cannot occupy more than half the rounded-up positions.
2. Either delay reusing the last character or fill separated positions first.

## Approach

### Heap with one delayed character

Pop the most frequent available character. Keep its remaining count outside the heap for one
turn, reinserting the previously delayed character after choosing the next one.

### Fill even then odd positions

Sort characters by decreasing count, fill indices 0,2,4,..., then 1,3,5,... . Reject a count
larger than ceil(n/2).

## Why it works

### Heap with one delayed character

The held character cannot be chosen immediately again. Choosing the most frequent eligible
character consumes the most constrained supply; the frequency feasibility condition ensures the
schedule can finish.

### Fill even then odd positions

The largest block fits entirely in the even positions. Remaining frequency blocks fill separated
slots, and descending block sizes prevent a repeated block from creating adjacent equal
characters across the even/odd boundary.

## Walkthrough

For "aaabbc", one valid answer is "ababac". For "aaaaab", five a characters cannot be separated
by one b, so return an empty string.

## Cost and pitfalls

Heap with one delayed character: O(n log(u+1)) time; O(n+u) space.
Fill even then odd positions: O(n + u log u) time; O(n+u) space.
The input string is immutable. u is the distinct-character count, at most 26 here. Validate
output multiplicities and adjacency rather than requiring one incidental valid arrangement.
"""

from collections import Counter
from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Heap with one delayed character
    Time: O(n log(u+1))
    Space: O(n+u)
    """

    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        if max(counts.values(), default=0) > (len(s) + 1) // 2:
            return ""
        heap = [(-count, char) for char, count in counts.items()]
        heapify(heap)
        previous_count, previous_char = 0, ""
        result = []
        while heap:
            count, char = heappop(heap)
            result.append(char)
            if previous_count < 0:
                heappush(heap, (previous_count, previous_char))
            previous_count, previous_char = count + 1, char
        return "".join(result)


class PositionFillSolution:
    """Approach: Fill even then odd positions
    Time: O(n + u log u)
    Space: O(n+u)
    """

    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        if max(counts.values(), default=0) > (len(s) + 1) // 2:
            return ""
        result = [""] * len(s)
        index = 0
        for char, count in sorted(counts.items(), key=lambda item: -item[1]):
            for _ in range(count):
                if index >= len(s):
                    index = 1
                result[index] = char
                index += 2
        return "".join(result)
