"""
## Task

Simulate a round-based senate of Radiant (R) and Dire (D) senators. Each active senator bans an
opponent who loses all future turns. Return the winning party under optimal play.

## Hints

1. Banning the earliest upcoming opponent is always at least as good as banning a later one.
2. Keep the future turn order either as two index queues or as one queue with pending bans.

## Approach

### Competing queues of future turn indices

Queue positions of each party. Pop their next senators; the earlier one bans the later one and
reenters its queue with index increased by n.

### One turn queue with deferred ban counts

Track living senators and pending bans by party. A banned queued senator disappears; an unbanned
one creates an opposite-party ban and queues its next turn.

## Why it works

### Competing queues of future turn indices

The earlier senator can remove the opponent with the soonest potential action, preventing at
least as much opposition as any later ban. Requeueing at index+n preserves round order; every
comparison removes one senator permanently.

### One turn queue with deferred ban counts

A pending ban always applies to the next opponent in turn order, realizing the same earliest-
opponent greedy choice. Every surviving action creates a ban; consumed bans remove senators, so
total queue work is linear in the initial population.

## Walkthrough

"RDD": the first R bans the next D, but the final D bans R on its own turn, so Dire wins.

## Cost and pitfalls

Competing queues of future turn indices: O(n) time; O(n) space.

One turn queue with deferred ban counts: O(n) time; O(n) space.

Input is unchanged. Requeued indices may exceed n and must keep increasing rather than wrapping
modulo n. Pending bans do not themselves consume an opponent turn until that senator is reached.
"""

from collections import deque


class Solution:
    """Approach: Competing queues of future turn indices
    Time: O(n)
    Space: O(n)
    """

    def predictPartyVictory(self, senate: str) -> str:
        radiant = deque(i for i, party in enumerate(senate) if party == "R")
        dire = deque(i for i, party in enumerate(senate) if party == "D")
        while radiant and dire:
            r, d = radiant.popleft(), dire.popleft()
            if r < d:
                radiant.append(r + len(senate))
            else:
                dire.append(d + len(senate))
        return "Radiant" if radiant else "Dire"


class DeferredBanSolution:
    """Approach: One turn queue with deferred ban counts
    Time: O(n)
    Space: O(n)
    """

    def predictPartyVictory(self, senate: str) -> str:
        queue = deque(senate)
        alive = {"R": senate.count("R"), "D": senate.count("D")}
        bans = {"R": 0, "D": 0}
        while alive["R"] and alive["D"]:
            party = queue.popleft()
            if bans[party]:
                bans[party] -= 1
                alive[party] -= 1
            else:
                opponent = "D" if party == "R" else "R"
                bans[opponent] += 1
                queue.append(party)
        return "Radiant" if alive["R"] else "Dire"
