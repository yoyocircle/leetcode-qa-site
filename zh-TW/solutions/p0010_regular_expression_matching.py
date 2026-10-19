"""## Task

Match an entire string against a valid pattern containing lowercase letters,
"." for any single character, and "*" for zero or more repetitions of the
preceding atom. Matching only a substring is insufficient.

## Hints

1. Define a state for matching a string prefix with a pattern prefix.
2. A starred atom either contributes zero characters or consumes one while staying available.

## Approach

### Rolling pattern-prefix DP

Keep one Boolean row for each processed string prefix. Initialize the
empty-string row with true at the empty pattern; starred pairs may extend
an empty match by contributing zero repetitions. For each character, build
a fresh row. An ordinary atom uses the preceding row's diagonal if it
matches. A star uses the current row two columns back for zero repetitions,
or the preceding row at the same column if its atom consumes this character.

### Active pattern states with epsilon closure

Tokenize the pattern into atoms with a starred flag. Track active automaton positions; a
starred token may be skipped through an epsilon transition or consume a matching character
while staying in place.

## Why it works

### Rolling pattern-prefix DP

An unstarred atom must consume exactly the final character, leaving the
diagonal prefix pair. A starred atom either consumes nothing or consumes
the final character after an earlier match of the same pattern prefix.
These cases cover every repetition count and construct only legal matches.
Induction over prefixes proves the final state represents a whole-string match.

### Active pattern states with epsilon closure

Epsilon closure includes every zero-repetition choice. Character transitions include exactly
the tokens able to consume that character, retaining starred tokens for further repetitions.
Thus active states are precisely all partial pattern matches after each prefix.

## Walkthrough

For "aab" and "a*b", the empty prefix matches a* with zero repetitions.
The next two rows keep a* true by consuming each a. The b row succeeds
through the diagonal preceding b, completing the match.

## Cost and pitfalls

For the default Rolling pattern-prefix DP approach:

O((string_length+1)*(pattern_length+1)) time and O(pattern_length) space;
inputs are unchanged. Each fresh row has a false empty-pattern state.
"*" repeats its preceding atom, not arbitrary text. Valid patterns guarantee
every star has a preceding atom. Do not confuse this syntax with glob matching.

Rolling pattern-prefix DP: O((m+1)*(n+1)) time; O(n) space.
Active pattern states with epsilon closure: O((m+1)*(n+1)) time; O(n) space.
Automaton simulation retains a set rather than a Boolean DP row and demonstrates zero-width
transitions. Neither is the unrestricted backtracking regex engine; input patterns follow
the promised valid syntax.
"""


class Solution:
    """Approach: Rolling pattern-prefix DP
    Time: O((m+1)*(n+1))
    Space: O(n)
    """

    def isMatch(self, s: str, p: str) -> bool:
        previous = [False] * (len(p) + 1)
        previous[0] = True
        for end in range(2, len(p) + 1):
            if p[end - 1] == "*":
                previous[end] = previous[end - 2]
        for character in s:
            current = [False] * (len(p) + 1)
            for end, atom in enumerate(p, 1):
                if atom == "*":
                    repeated = p[end - 2]
                    matches = repeated == "." or repeated == character
                    current[end] = current[end - 2] or (previous[end] and matches)
                else:
                    current[end] = previous[end - 1] and (atom == "." or atom == character)
            previous = current
        return previous[-1]


class NFASolution:
    """Approach: Active pattern states with epsilon closure
    Time: O((m+1)*(n+1))
    Space: O(n)
    """

    def isMatch(self, s: str, p: str) -> bool:
        atoms = []
        for character in p:
            if character == "*":
                atoms[-1] = (atoms[-1][0], True)
            else:
                atoms.append((character, False))

        def closure(states):
            result = set(states)
            for index in range(len(atoms)):
                if index in result and atoms[index][1]:
                    result.add(index + 1)
            return result

        active = closure({0})
        for character in s:
            following = set()
            for index in active:
                if index < len(atoms):
                    atom, starred = atoms[index]
                    if atom == "." or atom == character:
                        following.add(index if starred else index + 1)
            active = closure(following)
        return len(atoms) in active
