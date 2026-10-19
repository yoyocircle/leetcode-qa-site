"""
## Task

Give every child at least one candy. A child with a higher rating than an adjacent child must
receive more candies. Return the minimum total.

## Hints

1. Left and right neighbor requirements can be solved in separate passes.
2. A monotone rating run forces candy counts 1,2,3,...; peaks must satisfy both sides.

## Approach

### Two directional candy passes

Assign the minimum candies satisfying left neighbors, then scan backward and raise counts only
as needed for right neighbors.

### Slope lengths with peak correction

Track lengths of the current rising and falling runs and the preceding peak height. Rising
values add an increasing count; falling values add their run contribution, correcting the shared
peak once.

## Why it works

### Two directional candy passes

The forward count is a necessary lower bound from each increasing prefix run. The backward pass
takes the maximum with the necessary decreasing-run bound. These maxima satisfy both neighbors
and are componentwise minimal.

### Slope lengths with peak correction

An increasing run needs successive counts 1 through up+1; a decreasing run has the symmetric
forced counts. Their shared peak needs the larger requirement, not their sum. The peak>=down
correction removes its duplicate contribution until the descending requirement exceeds it.

## Walkthrough

[1,0,2] needs candies [2,1,2], totaling 5. For [1,2,3,2,1], the peak count 3 serves both slopes
rather than being counted twice.

## Cost and pitfalls

Two directional candy passes: O(n) time; O(n) space.

Slope lengths with peak correction: O(n) time; O(1) space.

Inputs are unchanged and there is at least one child. Equal ratings impose no inequality and
reset both slope runs. The constant-space variant returns only the total, not a full assignment.
"""


class Solution:
    """Approach: Two directional candy passes
    Time: O(n)
    Space: O(n)
    """

    def candy(self, ratings: list[int]) -> int:
        candies = [1] * len(ratings)
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        for i in range(len(ratings) - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)


class SlopeSolution:
    """Approach: Slope lengths with peak correction
    Time: O(n)
    Space: O(1)
    """

    def candy(self, ratings: list[int]) -> int:
        total = 1
        up = down = peak = 0
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                up += 1
                peak = up
                down = 0
                total += up + 1
            elif ratings[i] == ratings[i - 1]:
                up = down = peak = 0
                total += 1
            else:
                up = 0
                down += 1
                total += down + 1
                if peak >= down:
                    total -= 1
        return total
