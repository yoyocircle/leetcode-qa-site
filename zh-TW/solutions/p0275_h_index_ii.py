"""
## Task

Given sorted nondecreasing citation counts, return the largest h such that at least h papers
have at least h citations. Required time is logarithmic.

## Hints

1. At position i, there are n-i papers with at least citations[i] citations.
2. Find the first index where citations[i] is at least n-i.

## Approach

### Binary search the qualifying suffix

Lower-bound the monotone condition citations[i]>=n-i. The suffix length from that boundary is
the h-index.

### Descending paper-count scan

Read papers from highest citation count downward, extending h while the next paper supports the
next count. This educational baseline misses the mandated logarithmic-time bound.

## Why it works

### Binary search the qualifying suffix

Once the condition holds, larger indices have no smaller citations and need fewer qualifying
papers. The first true position gives the largest possible suffix length and therefore the
maximum h.

### Descending paper-count scan

After accepting h papers, each of them has at least h citations. The first failure at h+1 also
rules out every larger h because all remaining citation counts are no greater.

## Walkthrough

[0,1,3,5,6] first satisfies citations[i]>=5-i at i=2, giving h=3. A single uncited paper gives
h=0.

## Cost and pitfalls

Binary search the qualifying suffix: O(log(n+1)) time; O(1) space.

Descending paper-count scan: O(n) time; O(1) space.

Inputs are unchanged. The number of papers is not the maximum citation count, and h cannot
exceed n. The scan uses reversed iteration without making a copied slice.
"""


class Solution:
    """Approach: Binary search the qualifying suffix
    Time: O(log(n+1))
    Space: O(1)
    """

    def hIndex(self, citations: list[int]) -> int:
        low, high = 0, len(citations)
        while low < high:
            middle = (low + high) // 2
            if citations[middle] >= len(citations) - middle:
                high = middle
            else:
                low = middle + 1
        return len(citations) - low


class ScanSolution:
    """Approach: Descending paper-count scan
    Time: O(n)
    Space: O(1)
    """

    def hIndex(self, citations: list[int]) -> int:
        h = 0
        for value in reversed(citations):
            if value < h + 1:
                break
            h += 1
        return h
