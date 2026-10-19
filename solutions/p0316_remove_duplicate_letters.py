"""## Task

Remove repeated letters so every distinct lowercase letter appears once, producing the
lexicographically smallest subsequence.

## Hints

1. A larger chosen letter may be removed if another copy remains later.
2. The first chosen position must leave all remaining distinct letters available.

## Approach

### Monotone stack with remaining counts

Skip letters already chosen. Before adding a new letter, pop larger suffix letters only when
they can be chosen again later.

### Choose the smallest feasible first letter recursively

The first chosen letter must appear by the earliest last occurrence of any remaining letter.
Choose the smallest character in that feasible prefix, then remove its later copies and
solve the suffix.

## Why it works

### Monotone stack with remaining counts

Popping creates a smaller first differing letter while preserving feasibility through a
later occurrence. A letter with no remaining copy cannot be removed. These exchange steps
maintain the smallest feasible chosen prefix.

### Choose the smallest feasible first letter recursively

Choosing after the boundary would lose a required letter. Every position up to it leaves all
other letters attainable, so the smallest character is optimal lexicographically; recursion
repeats the same argument on remaining letters.

## Walkthrough

For "cbacdcbc", the optimal unique-letter subsequence is "acdb".

## Cost and pitfalls

Monotone stack with remaining counts: O(n) time; O(A) space.
Choose the smallest feasible first letter recursively: O(A*n) time; O(A*n) including
retained slices space.

A is alphabet size, at most 26. The recursive variant has bounded alphabet-depth, not
input-length depth, but repeatedly copies suffix strings. The stack saves these allocations.
Both preserve input and count distinct letters, not distinct positions.
"""


class Solution:
    """Approach: Monotone stack with remaining counts
    Time: O(n)
    Space: O(A)
    """

    def removeDuplicateLetters(self, s: str) -> str:
        from collections import Counter

        remaining = Counter(s)
        stack, used = [], set()
        for character in s:
            remaining[character] -= 1
            if character in used:
                continue
            while stack and stack[-1] > character and remaining[stack[-1]]:
                used.remove(stack.pop())
            stack.append(character)
            used.add(character)
        return "".join(stack)


class GreedyPrefixSolution:
    """Approach: Choose the smallest feasible first letter recursively
    Time: O(A*n)
    Space: O(A*n) including retained slices
    """

    def removeDuplicateLetters(self, s: str) -> str:
        def choose(text):
            if not text:
                return ""
            last = {character: index for index, character in enumerate(text)}
            boundary = min(last.values())
            position = min(range(boundary + 1), key=lambda index: text[index])
            character = text[position]
            return character + choose(text[position + 1 :].replace(character, ""))

        return choose(s)
