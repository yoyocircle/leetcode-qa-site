"""
## Task

Return the length of the longest contiguous substring with no repeated character.
The input may be empty and may contain spaces and symbols.

## Hints

1. Maintain a window that already has no duplicates.
2. On seeing a repeated character, how far must its left boundary move?

## Approach

### Last-occurrence jumps

Checking every substring repeats character scans. Store each character's latest
index. When it reappears, move left past that index if it lies inside the current
window. Record the new index and the longest valid window.

### Set-based shrinking window

Keep the actual characters in the window. On a repeated incoming character, remove from the left
until its previous occurrence leaves.

## Why it works

### Last-occurrence jumps

Before adding a character, the window is unique. Only that new character can
create a duplicate, and excluding its previous occurrence removes the conflict.
The earliest valid left boundary gives the longest valid window ending here.

### Set-based shrinking window

The set equals the current window and has no duplicates after each insertion. Every longer
candidate ending at the current right index starts before the minimal valid left boundary and is
invalid.

## Walkthrough

For "abba", the second b moves left from 0 to 2. The final a previously
appeared at 0, outside the current window, so left stays 2. The answer is 2.

## Cost and pitfalls

Default approach (Last-occurrence jumps):

Expected O(n) time and O(min(n, alphabet size)) space; the string is unchanged.
Use max when updating left: moving it backward would reintroduce duplicates.
A substring must be contiguous. For the empty string, the answer is 0.

Last-occurrence jumps: O(n) expected time; O(min(n, alphabet)) space.
Set-based shrinking window: O(n) expected time; O(min(n, alphabet)) space. Keep the actual
characters in the window. On a repeated incoming character, remove from the left until its
previous occurrence leaves.
"""


class Solution:
    """Approach: Last-occurrence jumps
    Time: O(n) expected
    Space: O(min(n, alphabet))
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = best = 0
        for right, char in enumerate(s):
            left = max(left, last.get(char, -1) + 1)
            last[char] = right
            best = max(best, right - left + 1)
        return best


class SetWindowSolution:
    """Approach: Set-based shrinking window
    Time: O(n) expected
    Space: O(min(n, alphabet))
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        chars = set()
        left = best = 0
        for right, char in enumerate(s):
            while char in chars:
                chars.remove(s[left])
                left += 1
            chars.add(char)
            best = max(best, right - left + 1)
        return best
