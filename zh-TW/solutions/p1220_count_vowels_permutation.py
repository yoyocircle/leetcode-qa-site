"""## Task

Count length-n strings over a,e,i,o,u following the given next-vowel restrictions, modulo
1,000,000,007.

## Hints

1. Track how many strings end with each vowel.
2. The fixed five-state transition can be exponentiated for long lengths.

## Approach

### Five rolling ending-vowel counts

Initialize one string ending at each vowel. Update counts using incoming allowed
transitions: a from e/i/u, e from a/i, i from e/o, o from i, and u from i/o.

### Five-state transition exponentiation

Represent one extension as a 5x5 matrix with destination rows and predecessor columns. Apply
binary powers to the initial all-one vector for n-1 extensions.

## Why it works

### Five rolling ending-vowel counts

Every valid next string has one preceding ending vowel that permits its new final vowel.
Summing exactly those predecessor counts counts all valid strings once.

### Five-state transition exponentiation

Matrix multiplication composes transition counts over consecutive lengths. Binary
exponentiation computes exactly the required transition power, and multiplying the initial
vector sums every permitted starting vowel.

## Walkthrough

For n=1, every single vowel is allowed, giving 5; for n=2, the restrictions permit 10 strings.

## Cost and pitfalls

Five rolling ending-vowel counts: O(n) time; O(1) space.
Five-state transition exponentiation: O(5^3*log n) time; O(5^2) space.

Neither mutates inputs. Matrix dimensions are fixed, so O(5^2) is constant space. The matrix
method reduces dependence on n but performs more arithmetic for short strings; modulo
reduction bounds intermediate integers.
"""


class Solution:
    """Approach: Five rolling ending-vowel counts
    Time: O(n)
    Space: O(1)
    """

    def countVowelPermutation(self, n: int) -> int:
        modulus = 1_000_000_007
        a = e = i = o = u = 1
        for _ in range(n - 1):
            a, e, i, o, u = (
                (e + i + u) % modulus,
                (a + i) % modulus,
                (e + o) % modulus,
                i,
                (i + o) % modulus,
            )
        return (a + e + i + o + u) % modulus


class MatrixSolution:
    """Approach: Five-state transition exponentiation
    Time: O(5^3*log n)
    Space: O(5^2)
    """

    def countVowelPermutation(self, n: int) -> int:
        modulus = 1_000_000_007
        transition = [
            [0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
        ]

        def multiply(first, second):
            return [
                [sum(first[r][k] * second[k][c] for k in range(5)) % modulus for c in range(5)]
                for r in range(5)
            ]

        power = n - 1
        counts = [[1] for _ in range(5)]
        while power:
            if power & 1:
                counts = [
                    [sum(transition[r][c] * counts[c][0] for c in range(5)) % modulus]
                    for r in range(5)
                ]
            transition = multiply(transition, transition)
            power >>= 1
        return sum(row[0] for row in counts) % modulus
