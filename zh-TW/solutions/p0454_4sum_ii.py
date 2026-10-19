"""
## Task

Count index quadruples, one index from each of four equal-length arrays, whose values sum to
zero. Different indices count separately.

## Hints

1. Split four choices into two independent pairs.
2. Repeated pair sums must retain their multiplicity.

## Approach

### Hash pair-sum frequencies

Count all sums from the first two arrays, then add the frequency of the negated sum of each
remaining pair.

### Sorted pair sums with run counting

Sort both pair-sum lists and scan from opposite ends. When sums cancel, multiply equal-run
lengths.

## Why it works

### Hash pair-sum frequencies

Each quadruple decomposes uniquely into one first-pair and one second-pair choice. The frequency
product counts exactly the compatible index choices.

### Sorted pair sums with run counting

If the current total is negative, the smallest left run cannot match any remaining right value;
the symmetric argument removes too-large right values. Equal runs contribute all and only their
cross product.

## Walkthrough

With four arrays [0,0], all 2^4 = 16 index quadruples qualify. Counting only distinct sums would
lose those choices.

## Cost and pitfalls

Hash pair-sum frequencies: O(n squared) expected time; O(n squared) space.

Sorted pair sums with run counting: O(n squared log n) time; O(n squared) space.

Inputs are unchanged. n is each array length. Python integers avoid overflow in pair sums and
counts.
"""

from collections import Counter


class Solution:
    """Approach: Hash pair-sum frequencies
    Time: O(n squared) expected
    Space: O(n squared)
    """

    def fourSumCount(self, nums1, nums2, nums3, nums4) -> int:
        counts = Counter(a + b for a in nums1 for b in nums2)
        return sum(counts[-c - d] for c in nums3 for d in nums4)


class SortedPairsSolution:
    """Approach: Sorted pair sums with run counting
    Time: O(n squared log n)
    Space: O(n squared)
    """

    def fourSumCount(self, nums1, nums2, nums3, nums4) -> int:
        left = sorted(a + b for a in nums1 for b in nums2)
        right = sorted(c + d for c in nums3 for d in nums4)
        i, j, answer = 0, len(right) - 1, 0
        while i < len(left) and j >= 0:
            total = left[i] + right[j]
            if total < 0:
                i += 1
            elif total > 0:
                j -= 1
            else:
                start, end = i, j
                a, b = left[i], right[j]
                while i < len(left) and left[i] == a:
                    i += 1
                while j >= 0 and right[j] == b:
                    j -= 1
                answer += (i - start) * (end - j)
        return answer
