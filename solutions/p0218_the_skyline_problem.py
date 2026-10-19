"""
## Task

Return the key points of the skyline formed by rectangular buildings [left,right,height]. Omit
adjacent equal-height points and end at ground level.

## Hints

1. Only building start and end coordinates can change the skyline.
2. A skyline can also be merged from the skylines of two building groups.

## Approach

### Coordinate sweep with lazy max heap

Sweep sorted endpoint coordinates. Add every building starting by the coordinate and remove
expired heap maxima. Emit a key point only when the visible height changes.

### Divide and merge skylines

Recursively split buildings into groups, then merge their skyline change streams by taking the
maximum of their current heights.

## Why it works

### Coordinate sweep with lazy max heap

After expired maxima are removed, the heap top is the tallest active building; any expired
hidden building cannot affect it until later removal. Visibility is constant between endpoints,
so all and only height changes are emitted.

### Divide and merge skylines

At any x, the union's height is the maximum of the two group heights. Consuming all events at
the same x before emitting a change avoids transient points and preserves a canonical skyline.

## Walkthrough

[[2,9,10],[3,7,15],[5,12,12]] changes at [2,10],[3,15],[7,12],[12,0]. The height-10 building's
end at 9 stays hidden.

## Cost and pitfalls

Coordinate sweep with lazy max heap: O(n log n) time; O(n) space.

Divide and merge skylines: O(n log n) time; O(n) space.

Inputs are unchanged. Treat right endpoints as inactive at that x. Merge equal-coordinate events
together and suppress equal adjacent heights.
"""

from heapq import heappop, heappush


class Solution:
    """Approach: Coordinate sweep with lazy max heap
    Time: O(n log n)
    Space: O(n)
    """

    def getSkyline(self, buildings: list[list[int]]) -> list[list[int]]:
        ordered = sorted(buildings)
        coordinates = sorted({point for left, right, _ in buildings for point in (left, right)})
        heap = []
        index = 0
        answer = []
        for x in coordinates:
            while index < len(ordered) and ordered[index][0] <= x:
                _, right, height = ordered[index]
                heappush(heap, (-height, right))
                index += 1
            while heap and heap[0][1] <= x:
                heappop(heap)
            height = -heap[0][0] if heap else 0
            if not answer or answer[-1][1] != height:
                answer.append([x, height])
        return answer


class DivideMergeSolution:
    """Approach: Divide and merge skylines
    Time: O(n log n)
    Space: O(n)
    """

    def getSkyline(self, buildings: list[list[int]]) -> list[list[int]]:
        def merge(first, second):
            i = j = left_height = right_height = 0
            answer = []
            while i < len(first) or j < len(second):
                x = min(
                    first[i][0] if i < len(first) else float("inf"),
                    second[j][0] if j < len(second) else float("inf"),
                )
                while i < len(first) and first[i][0] == x:
                    left_height = first[i][1]
                    i += 1
                while j < len(second) and second[j][0] == x:
                    right_height = second[j][1]
                    j += 1
                height = max(left_height, right_height)
                if not answer or answer[-1][1] != height:
                    answer.append([x, height])
            return answer

        def build(low, high):
            if low == high:
                return []
            if high - low == 1:
                left, right, height = buildings[low]
                return [[left, height], [right, 0]]
            middle = (low + high) // 2
            return merge(build(low, middle), build(middle, high))

        return build(0, len(buildings))
