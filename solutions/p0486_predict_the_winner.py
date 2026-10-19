"""## Task

Two players alternately take either endpoint of an integer array and maximize their own
score. Decide whether the first can finish with at least the second player score.

## Hints

1. Evaluate score advantage for the player whose turn it is.
2. Alternatively retain that player's absolute maximum score for an interval.

## Approach

### Rolling interval score differences

Start with single-cell advantages. Fill left endpoints backward and right endpoints forward,
choosing an endpoint value minus the opponent advantage on the remaining interval.

### Absolute best score and interval totals

Store the best absolute score the current player can obtain from each interval. Its score
equals interval total minus the opponent optimum after the selected endpoint is removed.

## Why it works

### Rolling interval score differences

After taking an endpoint, player roles swap, so the child advantage must be subtracted. The
greater of the two legal choices is exactly the current player optimal score difference.

### Absolute best score and interval totals

All stones in an interval are eventually claimed, so player score plus opponent score is
fixed. Maximizing own score is therefore minimizing the opponent best attainable score over
the two remainders.

## Walkthrough

For [1,5,2], either first choice lets the opponent take 5, so the first player loses.

## Cost and pitfalls

Rolling interval score differences: O(n^2) time; O(n) space.
Absolute best score and interval totals: O(n^2) time; O(n^2) space.

Both preserve nums. The rolling variant copies the input into owned difference states and
must update right endpoints forward. A tie counts as a first-player win, hence the
non-strict final comparison.
"""


class Solution:
    """Approach: Rolling interval score differences
    Time: O(n^2)
    Space: O(n)
    """

    def predictTheWinner(self, nums: list[int]) -> bool:
        dp = nums.copy()
        for left in range(len(nums) - 2, -1, -1):
            for right in range(left + 1, len(nums)):
                dp[right] = max(nums[left] - dp[right], nums[right] - dp[right - 1])
        return dp[-1] >= 0


class ScoreTableSolution:
    """Approach: Absolute best score and interval totals
    Time: O(n^2)
    Space: O(n^2)
    """

    def predictTheWinner(self, nums: list[int]) -> bool:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        dp = [[0] * len(nums) for _ in nums]
        for left in range(len(nums) - 1, -1, -1):
            dp[left][left] = nums[left]
            for right in range(left + 1, len(nums)):
                total = prefix[right + 1] - prefix[left]
                dp[left][right] = total - min(dp[left + 1][right], dp[left][right - 1])
        return 2 * dp[0][-1] >= prefix[-1]
