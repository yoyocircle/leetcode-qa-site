"""## Task

Repeatedly delete a group of k adjacent equal characters. Deletions may expose
new equal neighbors. Return the final string after no such group remains.
The problem guarantees that the final result is unique.

## Hints

1. A deletion can only create a new match at the newly joined boundary.
2. Remember the suffix run length for each surviving prefix.

## Approach

### Run-count stack

Store (character, count) pairs for surviving runs. Extend the top if the next
character matches; otherwise start a new run. Pop a run as soon as its count
reaches k. Expand the remaining runs when constructing the result.

### Character buffer with saved run lengths

Use a writable copy of the characters and a parallel count array. Write each
new character at the current output position, recording its ending run length.
When that length reaches k, rewind the output pointer by k. Previously saved
counts at earlier positions allow an exposed run to continue immediately.

## Why it works

After each input character, the stack or live buffer prefix is the fully
reduced processed prefix. Only the new suffix can become a deletable group.
Removing that suffix restores the previous reduced prefix, and future input
can extend its exposed run. Induction processes all possible boundary merges;
the guaranteed unique reduced string is therefore returned.

## Walkthrough

For "abccba" with k=2, cc disappears, exposing bb; deleting bb exposes aa.
The result is empty. A pass that removes only the groups in the original
string would incorrectly stop at "abba".

## Cost and pitfalls

Both versions take O(n) time and O(n) space including output. Each input
character changes the stack or write cursor once; rewinding removes a known
suffix without rescanning it. The run stack stores fewer entries when runs
are long. The buffer version allocates two arrays of length n regardless.
The input string is immutable; neither changes it. Iterating the buffer is
safe because writes only affect positions already read, never future input.
Repeated whole-string replacement can require quadratic rescanning.
"""


class Solution:
    """Approach: Run-count stack
    Time: O(n)
    Space: O(n), including output
    """

    def removeDuplicates(self, s: str, k: int) -> str:
        stack = []
        for char in s:
            if stack and stack[-1][0] == char:
                stack[-1][1] += 1
            else:
                stack.append([char, 1])
            if stack[-1][1] == k:
                stack.pop()
        return "".join(char * count for char, count in stack)


class BufferSolution:
    """Approach: Character buffer with saved run lengths
    Time: O(n)
    Space: O(n), including output
    """

    def removeDuplicates(self, s: str, k: int) -> str:
        chars = list(s)
        runs = [0] * len(s)
        write = 0
        for char in chars:
            chars[write] = char
            runs[write] = runs[write - 1] + 1 if write and chars[write - 1] == char else 1
            write += 1
            if runs[write - 1] == k:
                write -= k
        return "".join(chars[:write])
