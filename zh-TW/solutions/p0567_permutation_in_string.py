"""
## Task

Decide whether the second lowercase string contains a contiguous rearrangement
of the first. Character multiplicities must match exactly.

## Hints

1. Every candidate substring has the same length as the first string.
2. Compare frequency vectors instead of generating permutations.

## Approach

### Fixed frequency-vector window

Build the first string's 26 counts. Slide a fixed-length window over the second,
adding the new character and removing the character that falls out. Compare
the two count arrays whenever a full window exists.

### Deficit-count window

Track character deficits and the total missing characters. A window with the required width and
zero missing characters is a permutation; arbitrary alphabet symbols work too.

## Why it works

### Fixed frequency-vector window

A length-m substring is a permutation exactly when all letter counts agree.
The maintained counts always describe the current length-m window, and every
such window is examined.

### Deficit-count window

Adding a character decreases missing only while that character is still needed. Removing one
increases missing only if it creates a deficit. Equal total window and pattern lengths turn full
coverage into exact equality.

## Walkthrough

For s1="aab" and s2="cbaad", the windows are "cba", "baa", and "aad".
The second has two a's and one b, so return True.

## Cost and pitfalls

Default approach (Fixed frequency-vector window):

O(m + 26n)=O(m+n) time and O(26) space, where m and n are string lengths.
Inputs are unchanged. Return False if m exceeds n. Removing the departing
character at index right-m keeps the window size correct. A set would confuse
"aab" with "abb"; counts are required.

Fixed frequency-vector window: O(26n) time; O(26) space.
Deficit-count window: O(n+m) expected time; O(alphabet) space. Track character deficits and the
total missing characters. A window with the required width and zero missing characters is a
permutation; arbitrary alphabet symbols work too.
"""


class Solution:
    """Approach: Fixed frequency-vector window
    Time: O(26n)
    Space: O(26)
    """

    def checkInclusion(self, s1: str, s2: str) -> bool:
        width = len(s1)
        if width > len(s2):
            return False
        need, window = [0] * 26, [0] * 26
        for char in s1:
            need[ord(char) - ord("a")] += 1
        for right, char in enumerate(s2):
            window[ord(char) - ord("a")] += 1
            if right >= width:
                window[ord(s2[right - width]) - ord("a")] -= 1
            if right >= width - 1 and window == need:
                return True
        return False


class DeficitSolution:
    """Approach: Deficit-count window
    Time: O(n+m) expected
    Space: O(alphabet)
    """

    def checkInclusion(self, s1: str, s2: str) -> bool:
        need = {}
        for char in s1:
            need[char] = need.get(char, 0) + 1
        missing = len(s1)
        left = 0
        for right, char in enumerate(s2):
            if need.get(char, 0) > 0:
                missing -= 1
            need[char] = need.get(char, 0) - 1
            if right - left + 1 > len(s1):
                outgoing = s2[left]
                need[outgoing] = need.get(outgoing, 0) + 1
                if need[outgoing] > 0:
                    missing += 1
                left += 1
            if right - left + 1 == len(s1) and missing == 0:
                return True
        return False
