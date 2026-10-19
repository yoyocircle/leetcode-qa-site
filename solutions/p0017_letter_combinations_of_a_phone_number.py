"""## Task

Return all strings formed by selecting one telephone-keypad letter for each supplied digit 2
through 9. Empty input yields no combinations.

## Hints

1. Each digit contributes one independent letter choice.
2. The Cartesian product can be enumerated by recursion or a mixed-radix counter.

## Approach

### Digit-by-digit backtracking

Choose one mapped letter at each digit, append it to a shared path, recurse, and undo. Join the
path only at full length.

### Mixed-radix enumeration

Treat each digit's letter count as a radix. Enumerate integers below their product and decode
each into one letter index per position.

## Why it works

### Digit-by-digit backtracking

Every output corresponds to one choice at every position. Trying every mapped letter at each
depth enumerates those choice vectors exactly once.

### Mixed-radix enumeration

Mixed-radix representation gives a bijection between the counter range and all position-wise
letter selections, including digits with four rather than three letters.

## Walkthrough

For digits "27", choose one of abc and one of pqrs, producing 12 strings such as "ap" and "cs".

## Cost and pitfalls

Digit-by-digit backtracking: O(d*4^d) loose bound time; O(d) auxiliary plus output space.
Mixed-radix enumeration: O(d*4^d) loose bound time; O(d) auxiliary plus output space.
The input is unchanged. d is at most four, so recursion is shallow. Avoid returning [""] for
empty input; that is an internal product seed, not the requested answer.
"""

LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


class Solution:
    """Approach: Digit-by-digit backtracking
    Time: O(d*4^d) loose bound
    Space: O(d) auxiliary plus output
    """

    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        result, path = [], []

        def visit(index):
            if index == len(digits):
                result.append("".join(path))
                return
            for char in LETTERS[digits[index]]:
                path.append(char)
                visit(index + 1)
                path.pop()

        visit(0)
        return result


class MixedRadixSolution:
    """Approach: Mixed-radix enumeration
    Time: O(d*4^d) loose bound
    Space: O(d) auxiliary plus output
    """

    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        count = 1
        for digit in digits:
            count *= len(LETTERS[digit])
        result = []
        for number in range(count):
            chars = []
            for digit in reversed(digits):
                number, index = divmod(number, len(LETTERS[digit]))
                chars.append(LETTERS[digit][index])
            result.append("".join(reversed(chars)))
        return result
