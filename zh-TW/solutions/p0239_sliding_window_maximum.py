"""
## Task

Return the maximum value in each consecutive length-k window. The window size
is between 1 and the array length.

## Hints

1. If a newer value is at least as large as an older one, when could the older win?
2. Store indices so expired candidates can be removed.

## Approach

### Monotonic index deque

A fresh maximum scan costs O(nk). Maintain a deque of candidate indices whose
values decrease from front to back. Remove expired indices at the front and
dominated values at the back before adding the current index.

### Block prefix and suffix maxima

Partition into width-k blocks. Compute prefix maxima within each block and suffix maxima in
reverse. A window maximum is the maximum of its left block suffix and right block prefix.

### Lazy max heap

Store negative values with indices in a heap. Remove expired entries only when they reach the
top, then report the top value. This general priority-queue baseline is slower and can retain
hidden expired entries.

## Why it works

### Monotonic index deque

A dominated older value can never be a maximum while the newer, larger value is
present, and it expires earlier. Every removed candidate is therefore irrelevant.
The deque's front is the largest surviving value in the current window.

### Block prefix and suffix maxima

A width-k window crosses at most two blocks. The two stored segments cover exactly that window;
when it aligns to one block both summaries still give its maximum.

### Lazy max heap

Every live value has a heap entry. Once expired top entries are removed, the heap top is live
and no live value is larger, so it is exactly the current window maximum.

## Walkthrough

For [4, 1, 3, 2] with k=2, maxima are [4, 3, 3]. When 3 arrives it removes
1 from the back; expired 4 is removed from the front.

## Cost and pitfalls

Default approach (Monotonic index deque):

O(n) time: each index enters and leaves at most once. Auxiliary space is O(k),
plus O(n-k+1) output. Input is unchanged. Expire indices at or before right-k.
Repeated values are safe to discard from the back because the newer copy lasts
longer.

Monotonic index deque: O(n) time; O(k) plus output space.
Block prefix and suffix maxima: O(n) time; O(n) space. Partition into width-k blocks. Compute
prefix maxima within each block and suffix maxima in reverse. A window maximum is the maximum of
its left block suffix and right block prefix.

Lazy max heap: O(n log n) time; O(n) plus output space. Store negative values with indices in a
heap. Remove expired entries only when they reach the top, then report the top value. This
general priority-queue baseline is slower and can retain hidden expired entries.
"""

from collections import deque
from heapq import heappop, heappush


class Solution:
    """Approach: Monotonic index deque
    Time: O(n)
    Space: O(k) plus output
    """

    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        candidates = deque()
        result = []
        for right, number in enumerate(nums):
            while candidates and candidates[0] <= right - k:
                candidates.popleft()
            while candidates and nums[candidates[-1]] <= number:
                candidates.pop()
            candidates.append(right)
            if right >= k - 1:
                result.append(nums[candidates[0]])
        return result


class BlockSolution:
    """Approach: Block prefix and suffix maxima
    Time: O(n)
    Space: O(n)
    """

    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        size = len(nums)
        prefix, suffix = [0] * size, [0] * size
        for i, value in enumerate(nums):
            prefix[i] = value if i % k == 0 else max(prefix[i - 1], value)
        for i in range(size - 1, -1, -1):
            suffix[i] = (
                nums[i] if i == size - 1 or (i + 1) % k == 0 else max(suffix[i + 1], nums[i])
            )
        return [max(suffix[i], prefix[i + k - 1]) for i in range(size - k + 1)]


class HeapSolution:
    """Approach: Lazy max heap
    Time: O(n log n)
    Space: O(n) plus output
    """

    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        heap = []
        answer = []
        for i, value in enumerate(nums):
            heappush(heap, (-value, i))
            while heap[0][1] <= i - k:
                heappop(heap)
            if i >= k - 1:
                answer.append(-heap[0][0])
        return answer
