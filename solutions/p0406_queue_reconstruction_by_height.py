"""
## Task

Each person is [height,k], where k is the number of people at least as tall standing ahead.
Reconstruct any queue satisfying all pairs; a valid queue is guaranteed.

## Hints

1. Place taller people first so inserting a shorter person does not alter their counts.
2. Alternatively place shorter people into free slots that will later be occupied by taller
   people.

## Approach

### Descending heights and list insertion

Sort by descending height and ascending k, then insert each person at index k in the result.

### Ascending heights and Fenwick free-slot selection

Process ascending height, breaking ties by descending k. Put each person in the (k+1)th empty
slot using a Fenwick tree of available positions.

## Why it works

### Descending heights and list insertion

When a person is inserted, all placed people are at least as tall, so index k gives exactly k
qualifying predecessors. Later shorter insertions do not affect that count; equal-height
ordering preserves it as well.

### Ascending heights and Fenwick free-slot selection

All still-empty slots will hold people at least as tall. Selecting the (k+1)th empty slot leaves
exactly k such slots ahead. Equal-height descending k prevents already-placed equal people from
invalidating that free-slot count.

## Walkthrough

[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]] can become [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]. Each k
counts taller-or-equal people, not just taller ones.

## Cost and pitfalls

Descending heights and list insertion: O(n squared) time; O(n) auxiliary plus output space.

Ascending heights and Fenwick free-slot selection: O(n log n) time; O(n) auxiliary plus output
space.

Inputs and nested person lists are unchanged; output pairs are fresh lists. Python list
insertion shifts later entries, giving the first method its quadratic bound. n is positive.
"""


class Solution:
    """Approach: Descending heights and list insertion
    Time: O(n squared)
    Space: O(n) auxiliary plus output
    """

    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        queue = []
        for height, count in sorted(people, key=lambda person: (-person[0], person[1])):
            queue.insert(count, [height, count])
        return queue


class FreeSlotSolution:
    """Approach: Ascending heights and Fenwick free-slot selection
    Time: O(n log n)
    Space: O(n) auxiliary plus output
    """

    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        size = len(people)
        bit = [0] + [i & -i for i in range(1, size + 1)]
        queue = [None] * size
        for height, count in sorted(people, key=lambda person: (person[0], -person[1])):
            rank = count + 1
            index = 0
            step = 1 << (size.bit_length() - 1)
            while step:
                following = index + step
                if following <= size and bit[following] < rank:
                    rank -= bit[following]
                    index = following
                step >>= 1
            queue[index] = [height, count]
            update = index + 1
            while update <= size:
                bit[update] -= 1
                update += update & -update
        return queue
