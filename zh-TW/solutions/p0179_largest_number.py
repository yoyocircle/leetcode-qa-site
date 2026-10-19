"""## Task

Arrange nonnegative integers so their concatenation is numerically greatest, returning a
decimal string.

## Hints

1. For two pieces a and b, compare a+b against b+a.
2. Sorting choices can be explored with a comparator or explicit insertion.

## Approach

### Concatenation comparator sort

Convert numbers to strings and sort by which pair concatenation is greater, placing the
preferable piece first.

### Explicit insertion by concatenation order

Insert each new piece into an already ordered list, shifting preceding pieces while the new
pair order improves the result.

## Why it works

### Concatenation comparator sort

Swapping an adjacent inverted pair improves the full concatenation, since its surrounding
text is unchanged. The concatenation comparison defines a consistent order, so eliminating
inversions gives a global optimum.

### Explicit insertion by concatenation order

The inner shifts remove all inversions involving the new piece while preserving earlier
order. Induction yields the same optimal comparator order after every insertion.

## Walkthrough

For [3,30,34,5,9], the greatest concatenation is "9534330"; [0,0] returns "0".

## Cost and pitfalls

Concatenation comparator sort: O(n log n*d) time; O(n*d) space.
Explicit insertion by concatenation order: O(n^2*d) time; O(n*d) space.

d is maximum digit length. Pair concatenations allocate O(d) temporary text per comparison;
sorting/insertion use new lists and preserve nums. Insertion is a viable small-n baseline (n
at most 100), but scales quadratically. Collapse all-zero output to one zero.
"""


class Solution:
    """Approach: Concatenation comparator sort
    Time: O(n log n*d)
    Space: O(n*d)
    """

    def largestNumber(self, nums: list[int]) -> str:
        from functools import cmp_to_key

        def compare(a, b):
            return (b + a > a + b) - (b + a < a + b)

        pieces = sorted(map(str, nums), key=cmp_to_key(compare))
        return "0" if pieces[0] == "0" else "".join(pieces)


class InsertionSolution:
    """Approach: Explicit insertion by concatenation order
    Time: O(n^2*d)
    Space: O(n*d)
    """

    def largestNumber(self, nums: list[int]) -> str:
        pieces = []
        for number in nums:
            current = str(number)
            position = len(pieces)
            pieces.append(current)
            while position and current + pieces[position - 1] > pieces[position - 1] + current:
                pieces[position] = pieces[position - 1]
                position -= 1
            pieces[position] = current
        return "0" if pieces[0] == "0" else "".join(pieces)
