"""
## Task

Translate one binary n by n image horizontally and vertically, without rotation, to maximize the
number of positions where both images contain one.

## Hints

1. Every overlapping pair of one-cells votes for one translation vector.
2. Row bit masks can count overlaps by AND and bit_count.

## Approach

### Translation votes from one-cell pairs

List the one coordinates in both images. Count the displacement between each pair; its frequency
is the overlap for that translation.

### Shifted row bit masks

Encode every row as one integer. For each vertical and horizontal translation, shift row masks
and count their bit intersections.

## Why it works

### Translation votes from one-cell pairs

For a fixed translation, each overlapping cell corresponds uniquely to a pair whose displacement
equals that translation. The vote count is therefore exactly its overlap, and the maximum vote
is optimal.

### Shifted row bit masks

A mask bit represents exactly one image column. Horizontal shifts implement translation and
bitwise AND retains exactly overlapping ones; summing matched rows gives the overlap for the
chosen displacement.

## Walkthrough

Two single one-cells anywhere in their images can always be aligned, producing overlap 1. Empty
images produce zero translation votes and answer zero.

## Cost and pitfalls

Translation votes from one-cell pairs: O(n squared+a*b) time; O(n squared) space.

Shifted row bit masks: O(n cubed) word operations for n<=30 time; O(n) words space.

Inputs are unchanged. a and b are the numbers of one-cells. The bit-row bound uses the stated
n<=30; wider arbitrary-size integers would add a word-length factor.
"""

from collections import Counter


class Solution:
    """Approach: Translation votes from one-cell pairs
    Time: O(n squared+a*b)
    Space: O(n squared)
    """

    def largestOverlap(self, img1: list[list[int]], img2: list[list[int]]) -> int:
        first = [(r, c) for r, row in enumerate(img1) for c, value in enumerate(row) if value]
        second = [(r, c) for r, row in enumerate(img2) for c, value in enumerate(row) if value]
        votes = Counter((r2 - r1, c2 - c1) for r1, c1 in first for r2, c2 in second)
        return max(votes.values(), default=0)


class BitRowSolution:
    """Approach: Shifted row bit masks
    Time: O(n cubed) word operations for n<=30
    Space: O(n) words
    """

    def largestOverlap(self, img1: list[list[int]], img2: list[list[int]]) -> int:
        size = len(img1)
        first = [sum(value << col for col, value in enumerate(row)) for row in img1]
        second = [sum(value << col for col, value in enumerate(row)) for row in img2]
        best = 0
        for dr in range(1 - size, size):
            for dc in range(1 - size, size):
                overlap = 0
                for row in range(size):
                    other = row + dr
                    if 0 <= other < size:
                        shifted = first[row] << dc if dc >= 0 else first[row] >> -dc
                        overlap += (shifted & second[other]).bit_count()
                best = max(best, overlap)
        return best
