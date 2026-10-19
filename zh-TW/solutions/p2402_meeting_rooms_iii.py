"""## Task

Assign meetings to numbered rooms. Use the smallest free room, or delay a meeting until the
earliest room becomes available, breaking equal availability ties by room number. Preserve
duration and original start-time priority; return the most-used room, ties to the smallest
number.

## Hints

1. Free rooms and occupied rooms need different priority orders.
2. Schedule meetings by original start time before applying any delay.

## Approach

### Free-room and finish-time heaps

Sort a copy of meetings. Release rooms finishing by the next original start into an ID heap.
Choose its minimum, or pop the earliest (finish,room) and add the preserved meeting duration.

### Linear room-availability scan

For each sorted meeting, scan room IDs for the first room free at its start. If none is free,
choose the minimum (available_time,room) by scanning all rooms.

## Why it works

### Free-room and finish-time heaps

The two heaps exactly represent free IDs and busy availability. Their ordering implements both
selection rules; chronological scheduling gives earlier original starts first claim on every
future release.

### Linear room-availability scan

The scan directly evaluates the same free-room and delayed-room rules. Updating only the chosen
room with max(start,availability)+duration maintains the next availability invariant.

## Walkthrough

With two rooms and meetings [0,4],[1,3],[2,5], the third meeting waits for room 1 at time 3 and
finishes at 6. Room 1 hosts two meetings and wins.

## Cost and pitfalls

Free-room and finish-time heaps: O(n+M log(M+1)+M log(n+1)) time; O(M+n) space.
Linear room-availability scan: O(M log(M+1)+M*n) time; O(M+n) space.
Meetings are unchanged; sorted copies cost O(M) references. End times are exclusive, so a room
finishing at a meeting's start is free. Delaying shifts both endpoints and must not shorten
duration. Tied final counts favor the smallest room.
"""

from heapq import heapify, heappop, heappush


class Solution:
    """Approach: Free-room and finish-time heaps
    Time: O(n+M log(M+1)+M log(n+1))
    Space: O(M+n)
    """

    def mostBooked(self, n: int, meetings: list[list[int]]) -> int:
        available = list(range(n))
        heapify(available)
        busy = []
        counts = [0] * n
        for start, end in sorted(meetings):
            while busy and busy[0][0] <= start:
                _, room = heappop(busy)
                heappush(available, room)
            if available:
                room = heappop(available)
                finish = end
            else:
                release, room = heappop(busy)
                finish = release + end - start
            counts[room] += 1
            heappush(busy, (finish, room))
        return counts.index(max(counts))


class RoomScanSolution:
    """Approach: Linear room-availability scan
    Time: O(M log(M+1)+M*n)
    Space: O(M+n)
    """

    def mostBooked(self, n: int, meetings: list[list[int]]) -> int:
        free_at = [0] * n
        counts = [0] * n
        for start, end in sorted(meetings):
            room = next((index for index in range(n) if free_at[index] <= start), None)
            if room is None:
                room = min(range(n), key=lambda index: (free_at[index], index))
            free_at[room] = max(start, free_at[room]) + end - start
            counts[room] += 1
        return counts.index(max(counts))
