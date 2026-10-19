"""## Task

Partition a string into palindromic substrings using the fewest cuts.

## Hints

1. The final palindrome extends the best partition of a shorter prefix.
2. Discover palindromes either by intervals or by expanding their centers.

## Approach

### Palindrome table and prefix cuts

Recognize palindromes by matching endpoints and a palindromic interior. For every ending
position, relax its prefix cut count from each palindromic suffix. Set empty-prefix cuts to
-1.

### Expand centers while relaxing prefix cuts

Expand odd and even palindromes by increasing center. Each discovered interval relaxes the
cut count immediately, without retaining a palindrome table.

## Why it works

### Palindrome table and prefix cuts

Every partition has one final palindrome, and all such suffixes are considered after their
prefix optima are settled. The -1 seed makes a whole-prefix palindrome require zero cuts.

### Expand centers while relaxing prefix cuts

When a palindrome starts at left, all palindromes ending before left have centers smaller
than the current one. Thus cuts[left] is already final. Every possible final palindrome is
discovered and relaxes its endpoint.

## Walkthrough

For "aab", split "aa|b" and use one cut.

## Cost and pitfalls

Palindrome table and prefix cuts: O(n^2) time; O(n^2) space.
Expand centers while relaxing prefix cuts: O(n^2) time; O(n) space.

Both preserve the string and use no substring copies. The center version saves quadratic
storage; retaining a table may help a later partition reconstruction.
"""


class Solution:
    """Approach: Palindrome table and prefix cuts
    Time: O(n^2)
    Space: O(n^2)
    """

    def minCut(self, s: str) -> int:
        palindrome = [[False] * len(s) for _ in s]
        cuts = list(range(-1, len(s)))
        for end in range(len(s)):
            for start in range(end + 1):
                if s[start] == s[end] and (end - start < 2 or palindrome[start + 1][end - 1]):
                    palindrome[start][end] = True
                    cuts[end + 1] = min(cuts[end + 1], cuts[start] + 1)
        return cuts[-1]


class CenterSolution:
    """Approach: Expand centers while relaxing prefix cuts
    Time: O(n^2)
    Space: O(n)
    """

    def minCut(self, s: str) -> int:
        cuts = list(range(-1, len(s)))
        for center in range(len(s)):
            for left, right in ((center, center), (center - 1, center)):
                while left >= 0 and right < len(s) and s[left] == s[right]:
                    cuts[right + 1] = min(cuts[right + 1], cuts[left] + 1)
                    left -= 1
                    right += 1
        return cuts[-1]
