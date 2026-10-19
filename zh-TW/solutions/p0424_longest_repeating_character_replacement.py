"""
## Task

Find the longest substring that can become one repeated uppercase letter after
changing at most k characters.

## Hints

1. Which existing character should you keep within a chosen window?
2. Express the required replacements using window length and a frequency.

## Approach

### Exact-frequency window

Maintain 26 character counts. A window needs length minus its largest count
replacements. Expand right and shrink left until this cost is at most k.
Recompute the true maximum over 26 counts to keep the window invariant direct.

### Binary search a feasible length

Binary-search the answer length. For each tested width, slide a fixed window and check whether
its size minus its highest frequency fits the budget.

## Why it works

### Exact-frequency window

Keeping the most frequent letter minimizes replacements. Extending a window
cannot decrease the required replacements; removing a left character cannot
increase them. Therefore a discarded left boundary cannot become useful for a
longer window later, and each right endpoint yields its longest valid window.

### Binary search a feasible length

A valid length-L window contains a valid length-(L-1) subwindow after deleting one endpoint: the
minimum replacement count cannot increase. Feasible lengths therefore form a prefix for binary
search.

## Walkthrough

For "ABBA" with k=1, "ABB" needs one replacement and has length 3.
"ABBA" needs two, so discard its first A; "BBA" again has length 3.

## Cost and pitfalls

Default approach (Exact-frequency window):

O(26n)=O(n) time and O(26)=O(1) space; input is unchanged. Count letters in the
current window, including decrements on removal. This implementation uses the
actual maximum, avoiding the extra proof needed for a stale historical maximum.

Exact-frequency window: O(26n) time; O(26) space.
Binary search a feasible length: O(26n log n) time; O(26) space. Binary-search the answer
length. For each tested width, slide a fixed window and check whether its size minus its highest
frequency fits the budget.
"""


class Solution:
    """Approach: Exact-frequency window
    Time: O(26n)
    Space: O(26)
    """

    def characterReplacement(self, s: str, k: int) -> int:
        counts = [0] * 26
        left = best = 0
        for right, char in enumerate(s):
            counts[ord(char) - ord("A")] += 1
            while right - left + 1 - max(counts) > k:
                counts[ord(s[left]) - ord("A")] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


class BinarySearchSolution:
    """Approach: Binary search a feasible length
    Time: O(26n log n)
    Space: O(26)
    """

    def characterReplacement(self, s: str, k: int) -> int:
        def feasible(width):
            counts = [0] * 26
            for right, char in enumerate(s):
                counts[ord(char) - ord("A")] += 1
                if right >= width:
                    counts[ord(s[right - width]) - ord("A")] -= 1
                if right >= width - 1 and width - max(counts) <= k:
                    return True
            return False

        low, high = 0, len(s)
        while low < high:
            middle = (low + high + 1) // 2
            if feasible(middle):
                low = middle
            else:
                high = middle - 1
        return low
