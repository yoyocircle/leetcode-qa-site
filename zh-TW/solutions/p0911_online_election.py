"""## Task

Record a chronological sequence of votes and answer who leads at time t. Votes at t count, and
equal vote counts favor the candidate with the most recent vote.

## Hints

1. Only the candidate receiving a new vote can become a new leader.
2. Store the leader after each vote, then binary-search query time.

## Approach

### Precomputed leader timeline

Scan votes, updating counts and replacing the leader whenever the current candidate ties or
exceeds its count. Store the leader at every timestamp.

### Per-candidate vote histories

Group timestamps by candidate. For each query binary-search every candidate's vote count and
last included vote, then maximize (count,last_vote_time).

## Why it works

### Precomputed leader timeline

The previous leader still beats every unchanged candidate. If the updated candidate ties it,
that candidate has the most recent vote, so the greater-or-equal update exactly preserves the
leader rule.

### Per-candidate vote histories

Each binary search computes the exact prefix count at t. The pair directly expresses the count
and recency rule, so maximizing it over candidates returns the correct leader.

## Walkthrough

Votes for [1,2,2,1] at times [0,3,5,8] produce leaders [1,2,2,1]. Queries at 4 and 8 return 2
and 1.

## Cost and pitfalls

Precomputed leader timeline: O(V) constructor; O(log(V+1)) query time; O(V) space.
Per-candidate vote histories: O(V) constructor; O(U log(V+1)) query; may time out time; O(V)
space.
Constructor inputs are copied or read into owned histories. Query times are at least the first
vote time. U is candidate count; the scan baseline may time out on large query batches. Use
bisect_right so a vote exactly at t is included.
"""

from bisect import bisect_right


class TopVotedCandidate:
    """Approach: Precomputed leader timeline
    Time: O(V) constructor; O(log(V+1)) query
    Space: O(V)
    """

    def __init__(self, persons: list[int], times: list[int]):
        self.times = times.copy()
        self.leaders = []
        counts = {}
        leader = persons[0]
        for person in persons:
            counts[person] = counts.get(person, 0) + 1
            if counts[person] >= counts.get(leader, 0):
                leader = person
            self.leaders.append(leader)

    def q(self, t: int) -> int:
        return self.leaders[bisect_right(self.times, t) - 1]


class CandidateHistoryElection:
    """Approach: Per-candidate vote histories
    Time: O(V) constructor; O(U log(V+1)) query; may time out
    Space: O(V)
    """

    def __init__(self, persons: list[int], times: list[int]):
        self.histories = {}
        for person, time in zip(persons, times, strict=True):
            self.histories.setdefault(person, []).append(time)

    def q(self, t: int) -> int:
        winner = None
        best = (-1, -1)
        for person, history in self.histories.items():
            count = bisect_right(history, t)
            if count and (count, history[count - 1]) > best:
                best = (count, history[count - 1])
                winner = person
        return winner
