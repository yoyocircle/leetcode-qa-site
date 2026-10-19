"""## Task

Return all orderings of an array of distinct integers. Every ordering uses every
input position exactly once.

## Hints

1. A permutation chooses one unused value for each successive position.
2. Unlike subsets, later choices can come from any still-unused input index.

## Approach

### Unused-index backtracking

Maintain a path and a set of used indices. Try each unused index, append its
value, recurse, then undo both the path and used-set change. Save a copy only
when the path contains all values.

### Iterative insertion

Start with the empty permutation. For each next value, insert it into every possible position of
every existing permutation. Each stage owns fresh lists, so no undo bookkeeping is needed.

## Why it works

### Unused-index backtracking

At depth d, the path consists of d distinct input positions. Trying every unused
position covers all possible next choices. Every complete ordering has one
unique choice sequence, so all n! permutations appear once.

### Iterative insertion

Removing the newest value from any permutation gives exactly one previous-stage permutation and
insertion position. This bijection proves that each full ordering is produced once.

## Walkthrough

For [1,3], choosing index 0 first gives [1,3]. Undo it, choose index 1
first, and obtain [3,1].

## Cost and pitfalls

Default approach costs and behavior:

O(n * n!) time including output copies and candidate scans, O(n) auxiliary
space, and O(n * n!) output storage. Input is unchanged. Restore the used set
after every recursive call. A start-index restriction would generate combinations,
not all orderings. This solution relies on the distinct-values contract.

Alternative tradeoff: O(n*n!) time; O(n*n!) space.
"""


class Solution:
    """Approach: Unused-index backtracking
    Time: O(n*n!)
    Space: O(n) auxiliary; O(n*n!) output
    """

    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []
        path = []
        used = set()

        def visit():
            if len(path) == len(nums):
                result.append(path.copy())
                return
            for i, value in enumerate(nums):
                if i in used:
                    continue
                used.add(i)
                path.append(value)
                visit()
                path.pop()
                used.remove(i)

        visit()
        return result


class InsertionSolution:
    """Approach: Iterative insertion
    Time: O(n*n!)
    Space: O(n*n!)
    """

    def permute(self, nums: list[int]) -> list[list[int]]:
        result = [[]]
        for value in nums:
            result = [
                path[:index] + [value] + path[index:]
                for path in result
                for index in range(len(path) + 1)
            ]
        return result
