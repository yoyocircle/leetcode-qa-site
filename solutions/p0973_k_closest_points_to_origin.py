"""## Task

Return the k points closest to the origin by Euclidean distance. Output order
does not matter.

## Hints

1. Squared distance preserves distance ordering without square roots.
2. Among the retained points, expose the farthest one so it can be replaced.

## Approach

### Size-k distance heap

Use a size-k max-heap represented by negative squared distances in Python's
min-heap. Store each point's index to identify it and resolve heap ties.
Replace the farthest retained point when a closer one appears.

### Sort by squared distance

Sort a new list of point references by squared distance, select its first k entries, and copy
their coordinates. This trades a simpler implementation for sorting all n points.

## Why it works

### Size-k distance heap

After each point, the heap contains k closest candidates from the processed
prefix, or all points if fewer than k were seen. A farther candidate cannot
improve that set; a closer one replaces its worst member.

### Sort by squared distance

Squared distance has the same order as Euclidean distance. The first k sorted entries therefore
have no greater distance than any omitted point; ties permit either choice.

## Walkthrough

For [[1,2],[4,0],[-1,0]] and k=2, squared distances are 5,16,1.
The last point replaces distance 16, so return the points at distances 1 and 5.

## Cost and pitfalls

Default approach costs and behavior:

O(n log(k+1)) time and O(k) auxiliary space, plus O(k) output. Input points are
unchanged and output coordinates are copied. Negative heap priorities reverse the
comparison: a better point has a larger stored priority. Comparing actual square
roots adds work without changing the selection.

Alternative tradeoff: O(n log n) time; O(n) auxiliary; O(k) output space.
"""

from heapq import heappush, heapreplace


class Solution:
    """Approach: Size-k distance heap
    Time: O(n log(k+1))
    Space: O(k)
    """

    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        heap = []
        for i, (x, y) in enumerate(points):
            entry = (-(x * x + y * y), i)
            if len(heap) < k:
                heappush(heap, entry)
            elif entry > heap[0]:
                heapreplace(heap, entry)
        return [points[i][:] for _, i in heap]


class SortingSolution:
    """Approach: Sort by squared distance
    Time: O(n log n)
    Space: O(n) auxiliary; O(k) output
    """

    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        ordered = sorted(points, key=lambda point: point[0] ** 2 + point[1] ** 2)
        return [point.copy() for point in ordered[:k]]
