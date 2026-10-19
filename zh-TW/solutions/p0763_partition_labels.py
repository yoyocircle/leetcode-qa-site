"""
## Task

Partition a string into the maximum number of contiguous pieces such that each letter occurs in
only one piece. Return piece lengths.

## Hints

1. A piece containing a letter must include its last occurrence.
2. Overlapping first-to-last letter intervals belong to one piece.

## Approach

### Greedy last-occurrence boundary

Record each letter's last index. Extend the current piece end to include every letter
encountered and close when the scan reaches that end.

### Merge character-span intervals

Build one first-to-last interval per character and merge intersecting intervals. The merged
lengths are the maximal partition lengths.

## Why it works

### Greedy last-occurrence boundary

Every piece must include the last occurrence of each of its letters. The maintained end is
therefore a necessary lower bound; reaching it makes the earliest possible valid cut, maximizing
the number of pieces.

### Merge character-span intervals

A character's entire span must be in one piece. Intersecting spans force the same piece
transitively; separate span components have no shared letter, so each component can be cut
apart.

## Walkthrough

"ababcbacadefegdehijhklij" closes its forced span components at indices 8,15,23, giving [9,7,8].

## Cost and pitfalls

Greedy last-occurrence boundary: O(n) expected time; O(A) space.

Merge character-span intervals: O(n+A log A) time; O(A) space.

Input is unchanged. A is distinct-letter count. Do not close a piece at a letter's last
occurrence unless it is also the farthest required end of the whole piece.
"""


class Solution:
    """Approach: Greedy last-occurrence boundary
    Time: O(n) expected
    Space: O(A)
    """

    def partitionLabels(self, s: str) -> list[int]:
        last = {char: i for i, char in enumerate(s)}
        start = end = 0
        answer = []
        for i, char in enumerate(s):
            end = max(end, last[char])
            if i == end:
                answer.append(i - start + 1)
                start = i + 1
        return answer


class IntervalSolution:
    """Approach: Merge character-span intervals
    Time: O(n+A log A)
    Space: O(A)
    """

    def partitionLabels(self, s: str) -> list[int]:
        spans = {}
        for i, char in enumerate(s):
            if char not in spans:
                spans[char] = [i, i]
            spans[char][1] = i
        answer = []
        start = end = -1
        for left, right in sorted(spans.values()):
            if left > end:
                if end >= 0:
                    answer.append(end - start + 1)
                start, end = left, right
            else:
                end = max(end, right)
        if end >= 0:
            answer.append(end - start + 1)
        return answer
