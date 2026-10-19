"""## Task

Count structurally distinct BSTs that contain each value 1 through n exactly once. Return the
count rather than constructing trees.

## Hints

1. For each root, multiply the number of possible left and right subtrees.
2. The resulting sequence is the Catalan sequence.

## Approach

### Catalan convolution DP

Set count[0]=1. For each size, sum count[left_size]*count[right_size] over all root positions.

### Multiplicative Catalan recurrence

Use C_0=1 and C_(i+1)=C_i*2*(2*i+1)//(i+2). Exact division yields the next Catalan value without
storing previous counts.

## Why it works

### Catalan convolution DP

A root partitions a BST into independent left and right subtrees. Different roots or subtree
pairs produce different trees, so multiplication within a split and addition across splits are
exact.

### Multiplicative Catalan recurrence

The recurrence follows from C_i=binomial(2*i,i)/(i+1). Successive formula ratios simplify to the
multiplier used in the loop, so induction yields the same count as the combinatorial recurrence.

## Walkthrough

For n=3, roots 1,2,3 contribute 2,1,2 possibilities, totaling 5.

## Cost and pitfalls

Catalan convolution DP: O(n^2) time; O(n) space.
Multiplicative Catalan recurrence: O(n) bounded-size arithmetic operations time; O(1)
bounded-size integers space.
Inputs are unchanged. An empty subtree contributes one arrangement, not zero. Costs exploit
n<=19 and bounded results; for unbounded n, Python integer multiplication and storage grow with
the number of bits.
"""


class Solution:
    """Approach: Catalan convolution DP
    Time: O(n^2)
    Space: O(n)
    """

    def numTrees(self, n: int) -> int:
        counts = [0] * (n + 1)
        counts[0] = 1
        for size in range(1, n + 1):
            counts[size] = sum(counts[left] * counts[size - 1 - left] for left in range(size))
        return counts[n]


class FormulaSolution:
    """Approach: Multiplicative Catalan recurrence
    Time: O(n) bounded-size arithmetic operations
    Space: O(1) bounded-size integers
    """

    def numTrees(self, n: int) -> int:
        count = 1
        for index in range(n):
            count = count * 2 * (2 * index + 1) // (index + 2)
        return count
