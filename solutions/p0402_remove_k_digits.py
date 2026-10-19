"""
## Task

Remove exactly k digits from a nonnegative decimal string to obtain the smallest possible
numeric value. Return canonical digits without leading zeroes, or "0".

## Hints

1. An earlier larger digit is more expensive than a later smaller digit.
2. If no descent remains, delete from the end.

## Approach

### Monotonic digit stack

Pop larger preceding digits while deletions remain. Remove any remaining budget from the tail,
then strip leading zeroes.

### Greedy next-digit selection

Choose the smallest feasible next retained digit from the positions reachable with the remaining
deletion budget. This educational baseline may time out on long decreasing inputs.

## Why it works

### Monotonic digit stack

At the first larger-before-smaller pair, deleting the larger earlier digit yields a smaller
number than any deletion later in that prefix. Repeating this exchange gives the
lexicographically minimal retained digit sequence.

### Greedy next-digit selection

The next retained digit must lie within the deletion budget. Picking the earliest smallest
candidate minimizes the first unresolved output position while preserving the most remaining
choices.

## Walkthrough

"1432219", k=3 removes 4, then 3, then a 2, leaving "1219". "10200", k=1 becomes "200" after
zero stripping.

## Cost and pitfalls

Monotonic digit stack: O(n) time; O(n) space.

Greedy next-digit selection: O(n squared) time; O(n) space.

Input is unchanged. Deleting equal digits is unnecessary. Avoid stack[:-k] when k=0 because -0
is zero.
"""


class Solution:
    """Approach: Monotonic digit stack
    Time: O(n)
    Space: O(n)
    """

    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        for char in num:
            while k and stack and stack[-1] > char:
                stack.pop()
                k -= 1
            stack.append(char)
        if k:
            del stack[-k:]
        return "".join(stack).lstrip("0") or "0"


class SelectionSolution:
    """Approach: Greedy next-digit selection
    Time: O(n squared)
    Space: O(n)
    """

    def removeKdigits(self, num: str, k: int) -> str:
        keep = len(num) - k
        start = 0
        answer = []
        while keep:
            end = len(num) - keep
            index = min(range(start, end + 1), key=num.__getitem__)
            answer.append(num[index])
            start = index + 1
            keep -= 1
        return "".join(answer).lstrip("0") or "0"
