"""## Task

Find unique combinations of distinct positive candidate values that sum to
target. A candidate may be used repeatedly; ordering within a combination
does not create a new answer.

## Hints

1. Require choices to have nondecreasing candidate indices.
2. After using a value, recurse from its same index to permit reuse.

## Approach

### Nondecreasing backtracking

Sort a copy of the candidates. Backtrack with a starting index and remaining
sum. Stop and save a copy at remaining zero. Stop scanning when a candidate
exceeds the remaining sum, since all later candidates are larger.

### Bottom-up combination lists

Keep a list of combinations for each subtotal. Process sorted candidates outside an ascending
subtotal loop, extending combinations at subtotal-value. This stores intermediate answers and
can use much more space than backtracking.

## Why it works

### Nondecreasing backtracking

Positive values strictly reduce the remainder, so every branch terminates.
Every valid multiset has one nondecreasing index sequence, which the search
visits. Restricting indices removes alternate orderings without losing a combination.

### Bottom-up combination lists

When processing value v, each new combination appends v to a combination made only from
processed values. Ascending subtotals permit reuse of v. A combination is created once when its
largest value is processed.

## Walkthrough

For candidates [2,3,5] and target 7, the successful paths are [2,2,3]
and [2,5]. The path [3,2,2] is excluded as a duplicate ordering.

## Cost and pitfalls

Default approach costs and behavior:

Let C be candidate count and D=target//min(candidates). A loose time bound is
O(C log C + C^D * (D+1)), including path copies. Auxiliary space is O(C+D),
plus output. Inputs are unchanged. Recurse at i rather than i+1 to allow reuse.
Nonpositive candidates would invalidate the termination argument and are excluded.

Alternative tradeoff: O(C*T + total intermediate path-copy work) time; O(T + total intermediate
path lengths) space.
"""


class Solution:
    """Approach: Nondecreasing backtracking
    Time: O(C log C + C^D*(D+1)) loose bound
    Space: O(C+D) auxiliary plus output
    """

    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        values = sorted(candidates)
        result = []
        path = []

        def visit(start, remaining):
            if remaining == 0:
                result.append(path.copy())
                return
            for i in range(start, len(values)):
                value = values[i]
                if value > remaining:
                    break
                path.append(value)
                visit(i, remaining - value)
                path.pop()

        visit(0, target)
        return result


class CombinationDPSolution:
    """Approach: Bottom-up combination lists
    Time: O(C*T + total intermediate path-copy work)
    Space: O(T + total intermediate path lengths)
    """

    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        combinations = [[] for _ in range(target + 1)]
        combinations[0] = [[]]
        for value in sorted(candidates):
            for total in range(value, target + 1):
                combinations[total].extend(path + [value] for path in combinations[total - value])
        return combinations[target]
