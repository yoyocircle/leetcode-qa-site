"""## Task

Compress consecutive runs in a character list. Write each run's character and,
if its length exceeds one, the decimal count into the same list. Return the
length of the meaningful prefix; anything after that prefix is irrelevant.

## Hints

1. A compressed run never occupies more positions than its original run.
2. Writing count digits from the largest decimal place avoids a temporary string.

## Approach

### In-place read and write pointers

Scan to the end of a run before writing its encoding. Emit its character,
then divide the count by descending decimal place values to emit digits.
The write cursor never passes the next unread run, so no source is lost.

### Buffered run encoding

Collect run encodings into a separate list, then replace the original list's
contents with that buffer. This is a straightforward reference implementation
but uses O(n) extra memory and does not meet the problem's constant-space goal.

## Why it works

Each maximal run is found exactly once. Its encoding is the required character
plus optional count. A run of length one occupies one slot; for length c>1,
1+digits(c)<=c. Thus the in-place writer stays within already-read positions.
The buffered version constructs the same concatenation before copying it back.

## Walkthrough

For [a,a,a,b,c,c], emit a3, then b, then c2. Return 5; the first five slots
are [a,3,b,c,2]. A run of twelve a characters must emit [a,1,2], not [a,12].

## Cost and pitfalls

In-place pointers take O(n) time and O(1) auxiliary space. The integer digit
loop writes at most as many slots as the runs consumed. Buffered encoding
takes O(n) time and O(n) auxiliary space, including Python's list replacement
and temporary strings. Both mutate chars and preserve the identity of the list.
The default leaves its unused suffix intact; the reference shrinks the list,
which is allowed because only the returned prefix matters.
"""

from itertools import groupby


class Solution:
    """Approach: In-place read and write pointers
    Time: O(n)
    Space: O(1) auxiliary
    """

    def compress(self, chars: list[str]) -> int:
        read = write = 0
        while read < len(chars):
            end = read + 1
            while end < len(chars) and chars[end] == chars[read]:
                end += 1
            chars[write] = chars[read]
            write += 1
            count = end - read
            if count > 1:
                place = 1
                while place * 10 <= count:
                    place *= 10
                while place:
                    digit, count = divmod(count, place)
                    chars[write] = chr(ord("0") + digit)
                    write += 1
                    place //= 10
            read = end
        return write


class BufferedSolution:
    """Approach: Buffered run encoding
    Time: O(n)
    Space: O(n); educational baseline exceeding the O(1) auxiliary-space goal
    """

    def compress(self, chars: list[str]) -> int:
        output = []
        for char, group in groupby(chars):
            count = sum(1 for _ in group)
            output.append(char)
            if count > 1:
                output.extend(str(count))
        chars[:] = output
        return len(output)
