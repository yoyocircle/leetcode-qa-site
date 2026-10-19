"""## Task

Return the greatest length of a contiguous subarray whose comparison signs alternate between
increasing and decreasing.

## Hints

1. Equal neighbors break every turbulent run crossing them.
2. Keep separate lengths for runs ending with an upward or downward step.

## Approach

### Upward and downward suffix lengths

A greater current value extends the preceding downward run; a smaller value extends the
upward run. Equality resets both to one.

### Alternating-sign window boundary

Keep the start of the longest alternating comparison window. Equal values reset after the
pair; a repeated nonzero comparison restarts at the preceding element.

## Why it works

### Upward and downward suffix lengths

Every turbulent suffix ends with one direction and can extend only the opposite-direction
suffix. Tracking both longest possibilities therefore gives every optimal ending suffix.

### Alternating-sign window boundary

A repeated comparison invalidates every window containing both of its last two steps, while
their shared endpoint can start a new valid pair. The maintained left boundary is thus the
earliest valid start for each right endpoint.

## Walkthrough

For [9,4,2,10,7,8], the suffix [4,2,10,7,8] alternates down/up/down/up and has length 5.

## Cost and pitfalls

Upward and downward suffix lengths: O(n) time; O(1) space.
Alternating-sign window boundary: O(n) time; O(1) space.

Both preserve arr, count elements rather than comparison signs, and return one for all-equal
input. No copied differences or slices are required.
"""


class Solution:
    """Approach: Upward and downward suffix lengths
    Time: O(n)
    Space: O(1)
    """

    def maxTurbulenceSize(self, arr: list[int]) -> int:
        up = down = answer = 1
        for index in range(1, len(arr)):
            if arr[index] > arr[index - 1]:
                up, down = down + 1, 1
            elif arr[index] < arr[index - 1]:
                up, down = 1, up + 1
            else:
                up = down = 1
            answer = max(answer, up, down)
        return answer


class WindowSolution:
    """Approach: Alternating-sign window boundary
    Time: O(n)
    Space: O(1)
    """

    def maxTurbulenceSize(self, arr: list[int]) -> int:
        left = 0
        previous = 0
        answer = 1
        for right in range(1, len(arr)):
            sign = (arr[right] > arr[right - 1]) - (arr[right] < arr[right - 1])
            if sign == 0:
                left = right
            elif sign == previous:
                left = right - 1
            answer = max(answer, right - left + 1)
            previous = sign
        return answer
