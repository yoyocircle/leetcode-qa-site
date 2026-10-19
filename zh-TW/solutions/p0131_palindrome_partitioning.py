"""## Task

Partition a string into contiguous nonempty substrings, each a palindrome. Return every valid
partition.

## Hints

1. A partition chooses the endpoint of its next piece.
2. Palindrome answers for short interiors can precompute longer ones.

## Approach

### Palindrome-table backtracking

Precompute whether every substring is a palindrome using matching endpoints and its interior.
Backtrack only through endpoints marked true.

### On-demand palindrome checks

At each start position, test candidate ends using two pointers, then recurse only after a
successful test. This avoids the quadratic table but repeats comparisons.

## Why it works

### Palindrome-table backtracking

The recurrence exactly characterizes palindromes. Every partition has one increasing sequence of
cut positions; restricting pieces to true table entries enumerates precisely the valid
sequences.

### On-demand palindrome checks

The two-pointer test accepts exactly mirrored equal characters. Exploring every accepted next
cut covers all valid partitions and excludes any with a nonpalindromic piece.

## Walkthrough

For "aab", the accepted partitions are ["a","a","b"] and ["aa","b"]. The piece "ab" is rejected.

## Cost and pitfalls

Palindrome-table backtracking: O(n^2 + n*2^n) loose bound time; O(n^2) auxiliary plus output
space.
On-demand palindrome checks: O(n^2*2^n) loose bound time; O(n) auxiliary plus output space.
The string is unchanged. Python substring slices copy characters; all output copies are included
in the loose bounds. Recursion is safe for the problem's small maximum string length.
"""


class Solution:
    """Approach: Palindrome-table backtracking
    Time: O(n^2 + n*2^n) loose bound
    Space: O(n^2) auxiliary plus output
    """

    def partition(self, s: str) -> list[list[str]]:
        n = len(s)
        palindrome = [[False] * n for _ in range(n)]
        for left in range(n - 1, -1, -1):
            for right in range(left, n):
                palindrome[left][right] = s[left] == s[right] and (
                    right - left < 2 or palindrome[left + 1][right - 1]
                )
        result, path = [], []

        def visit(start):
            if start == n:
                result.append(path.copy())
                return
            for end in range(start, n):
                if palindrome[start][end]:
                    path.append(s[start : end + 1])
                    visit(end + 1)
                    path.pop()

        visit(0)
        return result


class OnDemandSolution:
    """Approach: On-demand palindrome checks
    Time: O(n^2*2^n) loose bound
    Space: O(n) auxiliary plus output
    """

    def partition(self, s: str) -> list[list[str]]:
        result, path = [], []

        def visit(start):
            if start == len(s):
                result.append(path.copy())
                return
            for end in range(start, len(s)):
                left, right = start, end
                while left < right and s[left] == s[right]:
                    left += 1
                    right -= 1
                if left >= right:
                    path.append(s[start : end + 1])
                    visit(end + 1)
                    path.pop()

        visit(0)
        return result
