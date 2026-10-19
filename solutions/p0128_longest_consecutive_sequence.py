"""
## Task

Find the length of the longest run of consecutive integer values in an unsorted
array. Positions need not be adjacent. Duplicates do not extend a run.

## Hints

1. A hash set can answer whether the next integer exists.
2. Which numbers should start a scan so that no run is scanned repeatedly?

## Approach

### Hash-set run starts

Sorting costs O(n log n). Build a set and start a forward scan only from values
whose predecessor is absent. Such a value is the beginning of its run.

### Sort and scan

Sort a copy, skip duplicate values, and extend runs when adjacent distinct values differ by one.
This misses the mandated linear-time bound but is a useful deterministic baseline.

## Why it works

### Hash-set run starts

Every nonempty run has exactly one smallest value. Only that value starts a scan,
so every distinct number is visited within exactly one run. The maximum run
length is therefore found without repeated scans.

### Sort and scan

Every consecutive run is contiguous in sorted order. Ignoring equal neighbors prevents
duplicates from ending or extending a run.

## Walkthrough

For [8, 3, 5, 4, 3], only 3 and 8 start runs. Scanning from 3 reaches 4 and 5;
scanning from 8 stops immediately. The answer is 3.

## Cost and pitfalls

Default approach (Hash-set run starts):

Expected O(n) time and O(n) auxiliary space, using expected constant-time hashing.
Inputs are unchanged. Iterate over the set, not the original array: repeated
start values in the original could trigger repeated long scans. An empty input
returns 0.

Hash-set run starts: O(n) expected time; O(n) space.
Sort and scan: O(n log n) time; O(n) space. Sort a copy, skip duplicate values, and extend runs
when adjacent distinct values differ by one. This misses the mandated linear-time bound but is a
useful deterministic baseline.
"""


class Solution:
    """Approach: Hash-set run starts
    Time: O(n) expected
    Space: O(n)
    """

    def longestConsecutive(self, nums: list[int]) -> int:
        values = set(nums)
        best = 0
        for value in values:
            if value - 1 in values:
                continue
            end = value
            while end in values:
                end += 1
            best = max(best, end - value)
        return best


class SortingSolution:
    """Approach: Sort and scan
    Time: O(n log n)
    Space: O(n)
    """

    def longestConsecutive(self, nums: list[int]) -> int:
        previous = None
        run = best = 0
        for value in sorted(nums):
            if value == previous:
                continue
            run = run + 1 if previous is not None and value == previous + 1 else 1
            best = max(best, run)
            previous = value
        return best
