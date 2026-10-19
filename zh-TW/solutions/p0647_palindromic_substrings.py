"""## Task

Count all palindromic substrings, counting equal text at different positions separately.

## Hints

1. A palindrome has a character center or a gap center.
2. Mirror symmetry can reuse an already-known palindrome radius.

## Approach

### Expand around all centers

Visit every odd and even center and expand while endpoints agree. Each successful expansion
contributes one positional substring.

### Manacher odd and even radii

Maintain separate odd and even radius arrays. Mirror a radius within the rightmost known
palindrome, then expand only beyond the guaranteed region.

## Why it works

### Expand around all centers

Every palindrome has one unique center and radius. Expansion visits exactly those endpoint
pairs with matching interiors, so every palindrome is counted once.

### Manacher odd and even radii

Reflection supplies a valid radius bounded by the current right edge. Every further
successful comparison advances that edge, yielding linear total expansion work. Each radius
counts all shorter palindromes with that center.

## Walkthrough

For "aaa", three singles, two "aa" substrings, and one "aaa" give 6.

## Cost and pitfalls

Expand around all centers: O(n^2) time; O(1) space.
Manacher odd and even radii: O(n) time; O(n) space.

Inputs are unchanged. Odd radii include the center; even radii count matched pairs across a
gap. Counting unique string values would answer a different question.
"""


class Solution:
    """Approach: Expand around all centers
    Time: O(n^2)
    Space: O(1)
    """

    def countSubstrings(self, s: str) -> int:
        answer = 0
        for center in range(2 * len(s) - 1):
            left, right = center // 2, (center + 1) // 2
            while left >= 0 and right < len(s) and s[left] == s[right]:
                answer += 1
                left -= 1
                right += 1
        return answer


class ManacherSolution:
    """Approach: Manacher odd and even radii
    Time: O(n)
    Space: O(n)
    """

    def countSubstrings(self, s: str) -> int:
        odd = [0] * len(s)
        left, right = 0, -1
        for i in range(len(s)):
            radius = 1 if i > right else min(odd[left + right - i], right - i + 1)
            while i - radius >= 0 and i + radius < len(s) and s[i - radius] == s[i + radius]:
                radius += 1
            odd[i] = radius
            if i + radius - 1 > right:
                left, right = i - radius + 1, i + radius - 1
        even = [0] * len(s)
        left, right = 0, -1
        for i in range(len(s)):
            radius = 0 if i > right else min(even[left + right - i + 1], right - i + 1)
            while (
                i - radius - 1 >= 0 and i + radius < len(s) and s[i - radius - 1] == s[i + radius]
            ):
                radius += 1
            even[i] = radius
            if i + radius - 1 > right:
                left, right = i - radius, i + radius - 1
        return sum(odd) + sum(even)
