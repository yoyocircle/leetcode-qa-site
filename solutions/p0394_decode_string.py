"""
## Task

Decode a valid expression where k[expression] repeats the expression k times; encodings may nest
and counts may have multiple digits.

## Hints

1. Save the outer prefix and repetition count when opening a bracket.
2. A parser can instead return the decoded contents of each bracket pair.

## Approach

### Stack of suspended output chunks

Accumulate character chunks. An opening bracket saves the outer chunks and count; closing it
repeats the completed inner string into the restored outer chunks.

### Recursive descent by bracket scope

Parse a scope until its closing bracket. A repetition count recursively parses one nested scope
and appends its repeated result.

## Why it works

### Stack of suspended output chunks

Each saved frame represents exactly the decoded prefix before its matching bracket. Replacing a
completed inner expression by its repeated value preserves the decoded value of the outer
expression.

### Recursive descent by bracket scope

Induction on nesting depth shows that each parser call returns exactly its scope value.
Concatenating literal letters and correctly decoded repeated scopes gives the whole expression.

## Walkthrough

"3[a2[c]]" decodes the inner scope to "acc", then repeats it three times to obtain "accaccacc".

## Cost and pitfalls

Stack of suspended output chunks: O(n+L*d) worst case time; O(n+L*d) worst case space.

Recursive descent by bracket scope: O(n+L*d) worst case time; O(n+L*d) worst case space.

Input is unchanged. L is decoded length and d nesting depth; immutable strings may be recopied
at each nested level. Recursive descent uses O(d) call frames, safe for the stated short encoded
input.
"""


class Solution:
    """Approach: Stack of suspended output chunks
    Time: O(n+L*d) worst case
    Space: O(n+L*d) worst case
    """

    def decodeString(self, s: str) -> str:
        stack = []
        chunks = []
        count = 0
        for char in s:
            if char.isdigit():
                count = count * 10 + int(char)
            elif char == "[":
                stack.append((chunks, count))
                chunks, count = [], 0
            elif char == "]":
                text = "".join(chunks)
                chunks, repetitions = stack.pop()
                chunks.append(text * repetitions)
            else:
                chunks.append(char)
        return "".join(chunks)


class RecursiveDescentSolution:
    """Approach: Recursive descent by bracket scope
    Time: O(n+L*d) worst case
    Space: O(n+L*d) worst case
    """

    def decodeString(self, s: str) -> str:
        index = 0

        def parse():
            nonlocal index
            pieces = []
            while index < len(s) and s[index] != "]":
                if s[index].isdigit():
                    count = 0
                    while s[index].isdigit():
                        count = count * 10 + int(s[index])
                        index += 1
                    index += 1
                    inner = parse()
                    index += 1
                    pieces.append(inner * count)
                else:
                    pieces.append(s[index])
                    index += 1
            return "".join(pieces)

        return parse()
