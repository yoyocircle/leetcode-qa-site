"""## Task

Return all size-k combinations drawn from the integers 1 through n. Order within each
combination is increasing; answer order is unrestricted.

## Hints

1. Choose future values only after the most recent selection.
2. Stop considering a first choice when too few larger values remain.

## Approach

### Pruned increasing backtracking

Grow increasing paths. Limit each loop's upper bound so enough values remain to fill the
remaining positions. Save a copy at length k.

### Lexicographic combination successor

Start at [1,...,k]. Repeatedly increment the rightmost position that can increase, then reset
its suffix to consecutive successors.

## Why it works

### Pruned increasing backtracking

Increasing choices give each combination one representation. The upper bound discards only
prefixes with insufficient remaining values, so no valid combination is lost.

### Lexicographic combination successor

The rightmost increment changes the smallest possible suffix; filling it minimally produces the
next lexicographic combination. Starting at the minimum and stopping at the maximum visits all
combinations exactly once.

## Walkthrough

For n=4 and k=2, the successor sequence is [1,2], [1,3], [1,4], [2,3], [2,4], [3,4].

## Cost and pitfalls

Pruned increasing backtracking: O(k*C(n,k)) time; O(k) auxiliary plus output space.
Lexicographic combination successor: O(k*C(n,k)) time; O(k) auxiliary plus output space.
All state is local. k=n produces one answer. Output copies dominate storage. The successor bound
at zero-based index i is n-k+i+1, not n for every slot.
"""


class Solution:
    """Approach: Pruned increasing backtracking
    Time: O(k*C(n,k))
    Space: O(k) auxiliary plus output
    """

    def combine(self, n: int, k: int) -> list[list[int]]:
        result, path = [], []

        def visit(start):
            needed = k - len(path)
            if needed == 0:
                result.append(path.copy())
                return
            for value in range(start, n - needed + 2):
                path.append(value)
                visit(value + 1)
                path.pop()

        visit(1)
        return result


class SuccessorSolution:
    """Approach: Lexicographic combination successor
    Time: O(k*C(n,k))
    Space: O(k) auxiliary plus output
    """

    def combine(self, n: int, k: int) -> list[list[int]]:
        current = list(range(1, k + 1))
        result = []
        while True:
            result.append(current.copy())
            index = k - 1
            while index >= 0 and current[index] == n - k + index + 1:
                index -= 1
            if index < 0:
                return result
            current[index] += 1
            for following in range(index + 1, k):
                current[following] = current[following - 1] + 1
