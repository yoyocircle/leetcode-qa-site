"""## Task

Return one original root for every subtree shape and value pattern that occurs at least twice in
a binary tree.

## Hints

1. Equal subtrees have equal root values and equal left/right subtree descriptions.
2. Intern descriptions as small IDs instead of repeatedly copying long strings.

## Approach

### Interned structural IDs

Process iterative postorder. Assign a unique integer ID to each (value,left-ID,right-ID) tuple.
Count IDs and return a root exactly when its count reaches two.

### Full subtree signatures

Build a fully delimited string signature for each subtree in postorder and count those strings.
This educational baseline copies growing descendant encodings.

## Why it works

### Interned structural IDs

Induction makes IDs equal exactly for structurally identical valued subtrees. Counting a
repeated ID detects duplicates; emitting only at count two produces one representative per
duplicate class.

### Full subtree signatures

Explicit null markers and ordered child delimiters make the string encoding unambiguous. Equal
signatures therefore identify exactly equal subtrees, though large repeated copies are
unnecessary.

## Walkthrough

If two different parents each have a value-7 leaf, the value-7 leaf signature occurs twice, so
return one of those original leaves.

## Cost and pitfalls

Interned structural IDs: O(n) expected time; O(n) space.
Full subtree signatures: O(n^2) worst due to copied signatures time; O(n^2) worst space.
The tree is unchanged and returned nodes are original identities. The string baseline may time
out or use excessive memory on long trees; IDs preserve linear storage. Equal root values alone
do not establish duplicate subtrees.
"""

from collections import Counter


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Interned structural IDs
    Time: O(n) expected
    Space: O(n)
    """

    def findDuplicateSubtrees(self, root: TreeNode | None) -> list[TreeNode]:
        identifiers = {None: 0}
        interned, counts, result = {}, Counter(), []
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if expanded:
                key = (node.val, identifiers[node.left], identifiers[node.right])
                if key not in interned:
                    interned[key] = len(interned) + 1
                identifier = identifiers[node] = interned[key]
                counts[identifier] += 1
                if counts[identifier] == 2:
                    result.append(node)
            else:
                stack.append((node, True))
                for child in (node.left, node.right):
                    if child:
                        stack.append((child, False))
        return result


class StringSignatureSolution:
    """Approach: Full subtree signatures
    Time: O(n^2) worst due to copied signatures
    Space: O(n^2) worst
    """

    def findDuplicateSubtrees(self, root: TreeNode | None) -> list[TreeNode]:
        signatures = {None: "#"}
        counts, result = Counter(), []
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if expanded:
                signature = f"{node.val}({signatures[node.left]})({signatures[node.right]})"
                signatures[node] = signature
                counts[signature] += 1
                if counts[signature] == 2:
                    result.append(node)
            else:
                stack.append((node, True))
                for child in (node.left, node.right):
                    if child:
                        stack.append((child, False))
        return result
