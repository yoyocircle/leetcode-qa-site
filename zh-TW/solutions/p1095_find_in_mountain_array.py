"""
## Task

Using only MountainArray.get(index) and length(), return the smallest target index in a strict
mountain array, or -1. At most 100 get calls are allowed, and length is at most 10000.

## Hints

1. Find the unique peak, then search the increasing side before the decreasing side.
2. Cache interface reads, and account for calls rather than only asymptotic runtime.

## Approach

### Cached binary peak and two ordered searches

Binary-search the change from rising to falling slope. Search the increasing prefix first, then
the strictly decreasing suffix, caching every accessed index.

### Cached ternary peak and lower-bound side searches

Use unimodal ternary elimination to reduce the peak interval to at most three cells. Then use
lower bounds on each monotone side. This uses more peak comparisons but remains below the call
budget.

## Why it works

### Cached binary peak and two ordered searches

Slope comparisons retain the unique peak. Ordinary ordered searches cover both sides; searching
the prefix first returns the smaller index if target appears twice. Each binary loop has at most
14 iterations for n<=10000: at most 28 peak reads and 28 side-search reads, before cache
savings.

### Cached ternary peak and lower-bound side searches

Comparing two interior samples discards the outer third that cannot contain the unique maximum;
equal samples retain the middle. At n<=10000, fewer than 25 ternary iterations need at most 50
reads, the final scan at most three, and both side searches at most 30, totaling below 85 even
before cache savings.

## Walkthrough

For [1,2,3,4,5,3,1] and target 3, find peak index 4, then return increasing-side index 2 rather
than the other occurrence at index 5.

## Cost and pitfalls

Cached binary peak and two ordered searches: O(log n) time; O(log n)
space.

Cached ternary peak and lower-bound side searches: O(log n) time; O(log
n) space.

The supplied array is unchanged and is never inspected outside its public interface. The local
MountainArray helper supports ordinary tests; production LeetCode supplies that interface.
Caching reads is allowed; materializing all values would exceed the call budget.
"""

from typing import TYPE_CHECKING


class LocalMountainArray:
    """Local implementation of the judge-supplied read-only interface."""

    def __init__(self, values: list[int]):
        self._values = tuple(values)

    def get(self, index: int) -> int:
        return self._values[index]

    def length(self) -> int:
        return len(self._values)


if TYPE_CHECKING:
    MountainArray = LocalMountainArray


class Solution:
    """Approach: Cached binary peak and two ordered searches
    Time: O(log n)
    Space: O(log n)
    """

    def findInMountainArray(self, target: int, mountainArr: "MountainArray") -> int:
        cache = {}

        def get(index):
            if index not in cache:
                cache[index] = mountainArr.get(index)
            return cache[index]

        size = mountainArr.length()
        low, high = 0, size - 1
        while low < high:
            middle = (low + high) // 2
            if get(middle) < get(middle + 1):
                low = middle + 1
            else:
                high = middle
        peak = low
        for left, right, increasing in ((0, peak, True), (peak + 1, size - 1, False)):
            while left <= right:
                middle = (left + right) // 2
                value = get(middle)
                if value == target:
                    return middle
                if (value < target) == increasing:
                    left = middle + 1
                else:
                    right = middle - 1
        return -1


class TernarySolution:
    """Approach: Cached ternary peak and lower-bound side searches
    Time: O(log n)
    Space: O(log n)
    """

    def findInMountainArray(self, target: int, mountainArr: "MountainArray") -> int:
        cache = {}

        def get(index):
            if index not in cache:
                cache[index] = mountainArr.get(index)
            return cache[index]

        size = mountainArr.length()
        low, high = 0, size - 1
        while high - low > 2:
            left = low + (high - low) // 3
            right = high - (high - low) // 3
            first, second = get(left), get(right)
            if first < second:
                low = left + 1
            elif first > second:
                high = right - 1
            else:
                low, high = left + 1, right - 1
        peak = max(range(low, high + 1), key=get)
        for start, end, increasing in ((0, peak + 1, True), (peak + 1, size, False)):
            left, right = start, end
            while left < right:
                middle = (left + right) // 2
                value = get(middle)
                if value < target if increasing else value > target:
                    left = middle + 1
                else:
                    right = middle
            if left < end and get(left) == target:
                return left
        return -1
