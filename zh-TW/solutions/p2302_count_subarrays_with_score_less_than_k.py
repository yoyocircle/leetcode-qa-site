"""
## Task

The score of a positive-integer subarray is its sum times its length. Count nonempty subarrays
whose score is strictly less than k.

## Hints

1. Extending a positive window strictly increases its score.
2. For a fixed right endpoint, valid left endpoints form a suffix.

## Approach

### Shrinking score window

Extend right and remove left values until sum*length is below k. Add the number of surviving
starting positions.

### Prefix sums and binary-searched starts

Build prefix sums, then binary-search the earliest valid start for every exclusive right
endpoint.

## Why it works

### Shrinking score window

Deleting a positive left value decreases both sum and length, so every shorter suffix is valid
once the window is valid. Earlier starts are invalid, making right-left+1 the exact
contribution.

### Prefix sums and binary-searched starts

For a fixed end, moving the start right strictly decreases the score of nonempty windows; the
empty window is a valid sentinel because k is positive. Lower bound therefore identifies exactly
all valid starts.

## Walkthrough

[2,1,4,3,5], k=10 has six qualifying subarrays. [2,1] scores 3*2=6, while [1,4] scores 5*2=10
and is excluded.

## Cost and pitfalls

Shrinking score window: O(n) time; O(1) space.

Prefix sums and binary-searched starts: O(n log n) time; O(n) space.

Inputs are unchanged. Python integers handle scores beyond 32-bit range. Do not replace the
strict comparison with <=, and allow an empty surviving window when even a singleton fails.
"""


class Solution:
    """Approach: Shrinking score window
    Time: O(n)
    Space: O(1)
    """

    def countSubarrays(self, nums: list[int], k: int) -> int:
        left = total = answer = 0
        for right, value in enumerate(nums):
            total += value
            while left <= right and total * (right - left + 1) >= k:
                total -= nums[left]
                left += 1
            answer += right - left + 1
        return answer


class PrefixSearchSolution:
    """Approach: Prefix sums and binary-searched starts
    Time: O(n log n)
    Space: O(n)
    """

    def countSubarrays(self, nums: list[int], k: int) -> int:
        prefix = [0]
        for value in nums:
            prefix.append(prefix[-1] + value)
        answer = 0
        for end in range(1, len(prefix)):
            low, high = 0, end
            while low < high:
                middle = (low + high) // 2
                if (prefix[end] - prefix[middle]) * (end - middle) < k:
                    high = middle
                else:
                    low = middle + 1
            answer += end - low
        return answer
