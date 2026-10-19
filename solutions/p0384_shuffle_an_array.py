"""## Task

Store an integer array, return its original configuration with reset(), and return a uniform
random permutation with shuffle().

## Hints

1. Preserve an owned original snapshot.
2. At each step choose uniformly among the positions still eligible for that item.

## Approach

### Forward Fisher-Yates swaps

Copy the original values. Shuffle a fresh copy by choosing a random position from i through n-1
and swapping into position i.

### Inside-out permutation construction

Build a new array incrementally. For the ith original item choose a position in 0..i, move that
position's previous item to the new end, and place the new item there.

## Why it works

### Forward Fisher-Yates swaps

Each next position receives a uniform choice from the remaining values. Every permutation has
probability 1/n times 1/(n-1) through 1, hence 1/n!.

### Inside-out permutation construction

Inductively the previous prefix is uniform. Inserting the new item into any of i+1 equally
likely positions yields each larger permutation with equal probability.

## Walkthrough

For [2,4,6], every one of its six permutations has equal probability. Reset returns [2,4,6]
after any number of shuffles.

## Cost and pitfalls

Forward Fisher-Yates swaps: O(n) constructor/reset/shuffle time; O(n) space.
Inside-out permutation construction: O(n) constructor/reset/shuffle time; O(n) space.
The constructor copies the input and every returned array is fresh, so caller mutations cannot
alter the stored original. Both use linear output memory and exact uniform integer draws, rather
than sorting approximate random keys.
"""

from random import randrange


class Solution:
    """Approach: Forward Fisher-Yates swaps
    Time: O(n) constructor/reset/shuffle
    Space: O(n)
    """

    def __init__(self, nums: list[int]):
        self.original = tuple(nums)

    def reset(self) -> list[int]:
        return list(self.original)

    def shuffle(self) -> list[int]:
        result = list(self.original)
        for index in range(len(result)):
            chosen = randrange(index, len(result))
            result[index], result[chosen] = result[chosen], result[index]
        return result


class InsideOutSolution:
    """Approach: Inside-out permutation construction
    Time: O(n) constructor/reset/shuffle
    Space: O(n)
    """

    def __init__(self, nums: list[int]):
        self.original = tuple(nums)

    def reset(self) -> list[int]:
        return list(self.original)

    def shuffle(self) -> list[int]:
        result = []
        for index, value in enumerate(self.original):
            chosen = randrange(index + 1)
            result.append(value)
            result[index] = result[chosen]
            result[chosen] = value
        return result
