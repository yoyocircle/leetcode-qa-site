"""## Task

Return the longest contiguous subarray whose product is positive without needing to compute
its product.

## Hints

1. Track lengths ending here for positive and negative products.
2. Inside a zero-free run, product sign depends only on negative-count parity.

## Approach

### Positive and negative suffix lengths

Keep longest positive and negative product suffix lengths. Positive factors preserve signs,
negative factors swap them, and zero clears both.

### Zero-separated parity runs

Track the current zero-free run start, its first negative position, and its negative parity.
An even-parity prefix is entirely usable; an odd one drops through the first negative.

## Why it works

### Positive and negative suffix lengths

Every nonempty suffix extends a previous suffix or starts with the current value. These sign
transitions cover all possibilities, so retaining the greatest length for each sign is
sufficient.

### Zero-separated parity runs

For a fixed endpoint, a positive suffix needs an even negative count. With odd run parity,
removing the shortest prefix containing one negative gives the earliest valid suffix start,
hence the longest valid length.

## Walkthrough

For [1,-2,-3,4], two negatives make the entire length-four product positive.

## Cost and pitfalls

Positive and negative suffix lengths: O(n) time; O(1) space.
Zero-separated parity runs: O(n) time; O(1) space.

Both preserve nums and avoid multiplying large values. Zero cannot belong to a
positive-product subarray. A missing negative suffix has length zero, distinct from a
one-element negative suffix.
"""


class Solution:
    """Approach: Positive and negative suffix lengths
    Time: O(n)
    Space: O(1)
    """

    def getMaxLen(self, nums: list[int]) -> int:
        positive = negative = answer = 0
        for value in nums:
            if value > 0:
                positive += 1
                negative = negative + 1 if negative else 0
            elif value < 0:
                positive, negative = (negative + 1 if negative else 0), positive + 1
            else:
                positive = negative = 0
            answer = max(answer, positive)
        return answer


class RunSolution:
    """Approach: Zero-separated parity runs
    Time: O(n)
    Space: O(1)
    """

    def getMaxLen(self, nums: list[int]) -> int:
        start = 0
        first_negative = -1
        negatives = answer = 0
        for index, value in enumerate(nums):
            if value == 0:
                start, first_negative, negatives = index + 1, -1, 0
                continue
            if value < 0:
                negatives += 1
                if first_negative < 0:
                    first_negative = index
            if negatives % 2 == 0:
                answer = max(answer, index - start + 1)
            else:
                answer = max(answer, index - first_negative)
        return answer
