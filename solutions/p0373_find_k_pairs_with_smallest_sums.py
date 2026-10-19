"""## Task

Return k index-distinct pairs with the smallest sums from two ascending arrays. If fewer than k
pairs exist, return all of them; tied pairs may be ordered arbitrarily.

## Hints

1. For a fixed first-array index, pair sums increase along the second array.
2. Merge sorted rows instead of generating the entire Cartesian product.

## Approach

### Heap merge of sum rows

Seed row heads (i,0) for at most k first-array positions. Pop the smallest pair and advance only
its row to (i,j+1).

### Two-dimensional best-first frontier

Start at pair (0,0). After extracting a pair, enqueue unseen right and downward neighbors using
an index-pair set.

## Why it works

### Heap merge of sum rows

Each row is sorted, and the heap holds its smallest unreported pair. Rows beyond the first k
cannot be needed before k earlier row heads, so seeding only k rows is sufficient.

### Two-dimensional best-first frontier

Monotone rows and columns ensure every not-yet-seen minimum has a predecessor no larger than
itself. Expanding the smallest frontier point therefore discovers all pairs in nondecreasing sum
order.

## Walkthrough

For [1,4] and [2,3], the pair sums are 3,4,6,7. With k=3, return [1,2], [1,3], and [4,2].

## Cost and pitfalls

Heap merge of sum rows: O(min(k,m) + k log(min(k,m)+1)) time; O(min(k,m)) auxiliary plus output
space.
Two-dimensional best-first frontier: O(k log(k+1)) time; O(k) auxiliary plus output space.
Both inputs are unchanged. Duplicate values at different indices are distinct pair choices. The
heap bounds use the number of returned pairs, capped by m*n. A seen set is essential in the
two-direction frontier.
"""

from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Heap merge of sum rows
    Time: O(min(k,m) + k log(min(k,m)+1))
    Space: O(min(k,m)) auxiliary plus output
    """

    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            return []
        heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
        heapify(heap)
        result = []
        while heap and len(result) < k:
            _, i, j = heappop(heap)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return result


class FrontierSolution:
    """Approach: Two-dimensional best-first frontier
    Time: O(k log(k+1))
    Space: O(k) auxiliary plus output
    """

    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            return []
        heap = [(nums1[0] + nums2[0], 0, 0)]
        seen = {(0, 0)}
        result = []
        while heap and len(result) < k:
            _, i, j = heappop(heap)
            result.append([nums1[i], nums2[j]])
            for row, col in ((i + 1, j), (i, j + 1)):
                if row < len(nums1) and col < len(nums2) and (row, col) not in seen:
                    seen.add((row, col))
                    heappush(heap, (nums1[row] + nums2[col], row, col))
        return result
