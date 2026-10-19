"""## Task

Count length-n attendance records with at most one absence A and no three consecutive late L
symbols, modulo 1,000,000,007.

## Hints

1. Only absence count and trailing late-run length affect future validity.
2. The six-state automaton can be counted by matrix powers.

## Approach

### Six rolling attendance states

Track zero/one absence and trailing late count zero through two. P resets lateness, A
increments absence and resets lateness, and L extends only runs shorter than two.

### Six-state transition exponentiation

Encode each (absence count, trailing late count) as one of six indices. Build all legal
one-symbol transitions and apply the nth matrix power to the empty-record state.

## Why it works

### Six rolling attendance states

These states retain every fact relevant to whether another symbol is valid. Each allowed
symbol extends exactly one prefix into its corresponding next state, so summing final states
counts all valid records.

### Six-state transition exponentiation

A matrix entry counts transitions between states, and multiplication composes successive
choices. Raising it to n counts exactly length-n paths through the validity automaton.

## Walkthrough

For n=2, all nine strings over P,L,A are allowed except AA, giving 8.

## Cost and pitfalls

Six rolling attendance states: O(n) time; O(1) space.
Six-state transition exponentiation: O(6^3*log n) time; O(6^2) space.

Inputs are unchanged. Both avoid input-length recursion, important for n=100000. Fixed
matrix dimensions make auxiliary space constant, while modular arithmetic keeps integer
sizes bounded.
"""


class Solution:
    """Approach: Six rolling attendance states
    Time: O(n)
    Space: O(1)
    """

    def checkRecord(self, n: int) -> int:
        modulus = 1_000_000_007
        counts = [[1, 0, 0], [0, 0, 0]]
        for _ in range(n):
            following = [[0] * 3 for _ in range(2)]
            for absences in range(2):
                for late in range(3):
                    count = counts[absences][late]
                    following[absences][0] = (following[absences][0] + count) % modulus
                    if absences == 0:
                        following[1][0] = (following[1][0] + count) % modulus
                    if late < 2:
                        following[absences][late + 1] = (
                            following[absences][late + 1] + count
                        ) % modulus
            counts = following
        return sum(map(sum, counts)) % modulus


class MatrixSolution:
    """Approach: Six-state transition exponentiation
    Time: O(6^3*log n)
    Space: O(6^2)
    """

    def checkRecord(self, n: int) -> int:
        modulus = 1_000_000_007
        transition = [[0] * 6 for _ in range(6)]
        for absences in range(2):
            for late in range(3):
                source = absences * 3 + late
                transition[absences * 3][source] += 1
                if absences == 0:
                    transition[3][source] += 1
                if late < 2:
                    transition[source + 1][source] += 1
        counts = [1, 0, 0, 0, 0, 0]

        def square(matrix):
            return [
                [sum(matrix[r][k] * matrix[k][c] for k in range(6)) % modulus for c in range(6)]
                for r in range(6)
            ]

        power = n
        while power:
            if power & 1:
                counts = [
                    sum(transition[r][c] * counts[c] for c in range(6)) % modulus for r in range(6)
                ]
            transition = square(transition)
            power >>= 1
        return sum(counts) % modulus
