"""## Task

A printer can print one repeated character over any contiguous interval, overwriting
existing characters. Find the minimum turns to print s.

## Hints

1. Equal characters can share a turn even when other characters must be fixed between them
later.
2. Consecutive equal characters never require separate turns.

## Approach

### Compressed bottom-up left-end intervals

Collapse equal adjacent letters, then fill intervals. Either print the left letter
separately or merge its turn with a matching later letter while printing the intervening
interval afterward.

### Memoized right-end turn merging

Work from the right endpoint without preprocessing. Print it separately or extend a turn
printing an equal earlier character through that endpoint, solving the middle separately.

## Why it works

### Compressed bottom-up left-end intervals

A shared-character turn can span both equal positions, with intervening cells repaired
independently. Conversely, in an optimal schedule the leftmost letter is either isolated
from all later equal positions or shares such a turn, yielding one tested split.

### Memoized right-end turn merging

Extending the equal-character turn need not add a turn; any unwanted middle characters can
be restored by the independent middle schedule. The final turn covering the right endpoint
identifies a matching earlier position or a standalone case, making the alternatives
exhaustive.

## Walkthrough

For "aba", print aaa in one turn and overwrite the middle with b, totaling 2.

## Cost and pitfalls

Compressed bottom-up left-end intervals: O(n^3) time; O(n^2) space.
Memoized right-end turn merging: O(n^3) time; O(n^2) space.

n is original string length; compression can reduce actual DP size. Both preserve s. The
default builds an O(n) copied compressed string; memo uses index ranges and depth at most
100, within the stated limit. Ordinary run counting misses useful overwrite merges.
"""


class Solution:
    """Approach: Compressed bottom-up left-end intervals
    Time: O(n^3)
    Space: O(n^2)
    """

    def strangePrinter(self, s: str) -> int:
        text = "".join(
            character
            for index, character in enumerate(s)
            if index == 0 or character != s[index - 1]
        )
        n = len(text)
        dp = [[0] * n for _ in range(n)]
        for left in range(n - 1, -1, -1):
            dp[left][left] = 1
            for right in range(left + 1, n):
                dp[left][right] = 1 + dp[left + 1][right]
                for same in range(left + 1, right + 1):
                    if text[same] == text[left]:
                        middle = dp[left + 1][same - 1] if same > left + 1 else 0
                        dp[left][right] = min(dp[left][right], middle + dp[same][right])
        return dp[0][-1]


class MemoSolution:
    """Approach: Memoized right-end turn merging
    Time: O(n^3)
    Space: O(n^2)
    """

    def strangePrinter(self, s: str) -> int:
        from functools import cache

        @cache
        def turns(left, right):
            if left > right:
                return 0
            answer = turns(left, right - 1) + 1
            for same in range(left, right):
                if s[same] == s[right]:
                    answer = min(answer, turns(left, same) + turns(same + 1, right - 1))
            return answer

        return turns(0, len(s) - 1)
