"""
## Task

A bank is a grid of 0/1 strings. Count laser beams between devices in consecutive nonempty rows;
empty rows do not block beams.

## Hints

1. Only device counts per row matter.
2. Each adjacent pair of nonempty rows contributes the product of their counts.

## Approach

### Streaming previous nonempty count

Count ones in each row. Skip empty rows and add previous_count*current_count for every next
nonempty row.

### Filtered device-count sequence

First collect all nonzero row counts, then multiply neighboring entries. This materializes the
reduced data model for easy inspection.

## Why it works

### Streaming previous nonempty count

The previous count always belongs to the nearest nonempty row above. Every device pair between
those two rows has exactly one beam, giving their count product.

### Filtered device-count sequence

Removing empty rows preserves exactly the allowed row adjacencies. Every neighboring pair in the
filtered sequence contributes all cross-row device pairs and no forbidden beam.

## Walkthrough

["011001","000000","010100","001000"] has nonempty row counts [3,2,1], producing 3*2+2*1=8
beams.

## Cost and pitfalls

Streaming previous nonempty count: O(mn) time; O(1) space.

Filtered device-count sequence: O(mn) time; O(m) space.

Inputs are unchanged. Empty rows must preserve the previous nonempty count rather than reset it.
m and n are bank dimensions.
"""


class Solution:
    """Approach: Streaming previous nonempty count
    Time: O(mn)
    Space: O(1)
    """

    def numberOfBeams(self, bank: list[str]) -> int:
        previous = answer = 0
        for row in bank:
            count = row.count("1")
            if count:
                answer += previous * count
                previous = count
        return answer


class CountListSolution:
    """Approach: Filtered device-count sequence
    Time: O(mn)
    Space: O(m)
    """

    def numberOfBeams(self, bank: list[str]) -> int:
        counts = [count for row in bank if (count := row.count("1"))]
        return sum(counts[i - 1] * counts[i] for i in range(1, len(counts)))
