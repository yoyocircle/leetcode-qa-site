"""## Task

Return any longest contiguous palindromic substring.

## Hints

1. A palindrome grows from a character or a gap.
2. Mirror symmetry avoids repeating expansions already known to match.

## Approach

### Expand odd and even centers

Expand every character and gap center while endpoints match, retaining the longest interval
rather than copying each candidate.

### Manacher transformed-string radii

Insert separators so odd and even palindromes share one representation. Initialize each
radius from its mirrored center inside the rightmost known palindrome, then expand beyond
the guaranteed part.

## Why it works

### Expand odd and even centers

Every palindrome has exactly one center. Expanding that center discovers it, and the longest
discovered interval is therefore globally optimal.

### Manacher transformed-string radii

Mirror symmetry gives all radius comparisons already inside the known boundary. Every
additional successful expansion advances the right boundary, bounding total work linearly.
Transformed radius equals original substring length.

## Walkthrough

For "caba", the longest palindrome is "aba"; for "babad", either "bab" or "aba" is accepted.

## Cost and pitfalls

Expand odd and even centers: O(n^2) time; O(n) including returned substring space.
Manacher transformed-string radii: O(n) time; O(n) space.

Input contains only letters and digits, so the chosen separators/sentinels cannot collide
with it. Both preserve s; final slicing allocates the output. The center variant uses O(1)
auxiliary space excluding that output.
"""


class Solution:
    """Approach: Expand odd and even centers
    Time: O(n^2)
    Space: O(n) including returned substring
    """

    def longestPalindrome(self, s: str) -> str:
        start, length = 0, 1
        for center in range(2 * len(s) - 1):
            left, right = center // 2, (center + 1) // 2
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if right - left + 1 > length:
                    start, length = left, right - left + 1
                left -= 1
                right += 1
        return s[start : start + length]


class ManacherSolution:
    """Approach: Manacher transformed-string radii
    Time: O(n)
    Space: O(n)
    """

    def longestPalindrome(self, s: str) -> str:
        transformed = "^#" + "#".join(s) + "#$"
        radii = [0] * len(transformed)
        center = right = best_center = best_radius = 0
        for index in range(1, len(transformed) - 1):
            if index < right:
                radii[index] = min(right - index, radii[2 * center - index])
            while transformed[index + radii[index] + 1] == transformed[index - radii[index] - 1]:
                radii[index] += 1
            if index + radii[index] > right:
                center, right = index, index + radii[index]
            if radii[index] > best_radius:
                best_center, best_radius = index, radii[index]
        start = (best_center - best_radius) // 2
        return s[start : start + best_radius]
