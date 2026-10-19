"""## Task

Return the kth lexicographic permutation of the digits 1 through n, using one-based k. n is at
most nine.

## Hints

1. Each first-digit block contains (n-1)! permutations.
2. Convert k to zero-based rank before taking quotient and remainder.

## Approach

### Factorial block selection

Compute factorial block sizes. At each position, divide the remaining rank by the next block
size, remove that indexed available digit, and continue with the remainder.

### Repeated next permutation

Start at ascending digits and apply the standard lexicographic successor k-1 times: find a
rising pivot, swap with its smallest larger suffix digit, and reverse the suffix.

## Why it works

### Factorial block selection

Lexicographic permutations form equal blocks by their next digit. Quotient selects the
containing block and remainder selects the same relative rank inside it.

### Repeated next permutation

The descending suffix is already maximal. Increasing its preceding pivot minimally and resetting
the suffix minimally produces exactly the next lexicographic sequence.

## Walkthrough

For n=3 and k=4, zero-based rank 3 selects digit 2, then digit 3, then digit 1: "231".

## Cost and pitfalls

Factorial block selection: O(n^2) time; O(n) space.
Repeated next permutation: O(k*n) time; O(n) space.
Inputs are unchanged. Python list deletion and suffix reversal cost linear time, included above.
The successor baseline is much slower at large k; factorial selection skips complete permutation
blocks.
"""


class Solution:
    """Approach: Factorial block selection
    Time: O(n^2)
    Space: O(n)
    """

    def getPermutation(self, n: int, k: int) -> str:
        factorials = [1] * (n + 1)
        for index in range(1, n + 1):
            factorials[index] = factorials[index - 1] * index
        available = list(map(str, range(1, n + 1)))
        k -= 1
        result = []
        for remaining in range(n, 0, -1):
            index, k = divmod(k, factorials[remaining - 1])
            result.append(available.pop(index))
        return "".join(result)


class SuccessorSolution:
    """Approach: Repeated next permutation
    Time: O(k*n)
    Space: O(n)
    """

    def getPermutation(self, n: int, k: int) -> str:
        values = list(range(1, n + 1))
        for _ in range(k - 1):
            pivot = n - 2
            while values[pivot] >= values[pivot + 1]:
                pivot -= 1
            successor = n - 1
            while values[successor] <= values[pivot]:
                successor -= 1
            values[pivot], values[successor] = values[successor], values[pivot]
            values[pivot + 1 :] = reversed(values[pivot + 1 :])
        return "".join(map(str, values))
