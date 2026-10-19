"""## Task

Convert an integer from 1 through 3999 into its standard Roman numeral, using
the subtractive forms IV, IX, XL, XC, CD, and CM.

## Hints

1. Include subtractive pairs as tokens alongside individual symbols.
2. Alternatively, each decimal place has only ten possible encodings.

## Approach

### Descending token subtraction

Process token values from 1000 down to 1, including subtractive tokens in
their numeric positions. Divide the remaining number by each token value;
append that many copies and keep the remainder.

### Decimal place tables

Split the integer into thousands, hundreds, tens, and units. Use four fixed
lookup tables and concatenate their entries. Each table encodes the permitted
repetitions and the fourth/ninth subtractive cases directly.

## Why it works

For each decimal place, standard Roman notation fixes its canonical encoding.
Descending tokens emit exactly those encodings: the fourth and ninth cases
are consumed by the subtractive token before individual symbols can repeat.
Place tables store the same complete cases explicitly. Higher decimal places
always precede lower places, so concatenation preserves canonical order.

## Walkthrough

For 2449, thousands contribute MM, hundreds CD, tens XL, and units IX.
The result is MMCDXLIX. Descending tokens consume 2000, 400, 40, then 9.

## Cost and pitfalls

Both versions take O(1) time and O(1) space under the fixed 1..3999 domain.
The tables and number of tokens are fixed, and even the output length is
bounded. For a generalized unbounded numeral system these bounds would need
reconsideration. The integer input is immutable. Do not use arbitrary
subtraction pairs such as IL for 49; its canonical form is XLIX.
"""


class Solution:
    """Approach: Descending token subtraction
    Time: O(1) for the stated bounded integer domain
    Space: O(1) for the stated bounded integer domain
    """

    def intToRoman(self, num: int) -> str:
        tokens = (
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        )
        pieces = []
        for value, symbol in tokens:
            count, num = divmod(num, value)
            pieces.append(symbol * count)
        return "".join(pieces)


class PlaceTableSolution:
    """Approach: Decimal place tables
    Time: O(1) for the stated bounded integer domain
    Space: O(1) for the stated bounded integer domain
    """

    def intToRoman(self, num: int) -> str:
        thousands = ("", "M", "MM", "MMM")
        hundreds = ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM")
        tens = ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC")
        ones = ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")
        return (
            thousands[num // 1000]
            + hundreds[num // 100 % 10]
            + tens[num // 10 % 10]
            + ones[num % 10]
        )
