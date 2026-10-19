"""## Task

Start with the string "1". Each next term describes consecutive runs in the
previous term as a decimal count followed by the repeated digit. Return term n.

## Hints

1. Count consecutive equal digits, not total digit frequencies.
2. The recurrence can be evaluated iteratively or by first obtaining term n-1.

## Approach

### Iterative run scanning

Keep only the current term. Move two indices across each maximal equal run,
append its length and digit to a pieces list, and join to form the next term.

### Recursive term construction

Recursively obtain the preceding term, with term one as the base case. Use
groupby to consume its runs, count each run, and join its descriptions. No
memoization is needed because each term is requested exactly once.

## Why it works

The indices and groupby both partition a term into maximal consecutive runs.
Each run contributes exactly its length and digit, which defines the next term.
Induction from the common base "1" proves that either evaluation order returns
term n. There is no branching recursion or repeated subproblem work.

## Walkthrough

The first four terms are 1, 11, 21, and 1211. Reading 21 gives one 2 followed
by one 1. A frequency map would discard this run order and cannot replace RLE.

## Cost and pitfalls

Let L be the largest generated term length and T the sum of all generated
term lengths through n. Both take O(T) time, including joins and run counting.
Iterative scanning uses O(L) space. Recursive construction uses O(L+n) space:
the n call frames await smaller terms, but earlier term strings are released
as those calls return. Under the stated n<=30, recursion depth is small.
Do not concatenate one character at a time into an immutable result string.
The input integer is unchanged; the returned string is newly constructed.
"""

from itertools import groupby


class Solution:
    """Approach: Iterative run scanning
    Time: O(T), summed generated term lengths
    Space: O(L), largest term length
    """

    def countAndSay(self, n: int) -> str:
        term = "1"
        for _ in range(n - 1):
            parts = []
            start = 0
            while start < len(term):
                end = start + 1
                while end < len(term) and term[end] == term[start]:
                    end += 1
                parts.extend((str(end - start), term[start]))
                start = end
            term = "".join(parts)
        return term


class RecursiveSolution:
    """Approach: Recursive term construction
    Time: O(T), summed generated term lengths
    Space: O(L+n), largest term plus call frames
    """

    def countAndSay(self, n: int) -> str:
        def term(index):
            if index == 1:
                return "1"
            previous = term(index - 1)
            pieces = []
            for digit, group in groupby(previous):
                pieces.extend((str(sum(1 for _ in group)), digit))
            return "".join(pieces)

        return term(n)
