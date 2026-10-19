"""## Task

Encode a binary tree as a string and reconstruct the same shape and values
from that string. The encoding format is your choice, but must round-trip.

## Hints

1. Values alone do not distinguish different tree shapes.
2. Include explicit missing-child markers in a deterministic traversal order.

## Approach

### Breadth-first null markers

Serialize breadth-first, writing each value or a # marker for None, separated
by commas. Deserialize by reading the root then two child tokens for each queued
real node. Use a fresh queue and nodes for every operation.

### Preorder null markers

Serialize iterative preorder with explicit null markers. Deserialize with a stack of pending
child slots, pushing right before left. Each codec owns its format; round-trip strings through
the same codec rather than mixing traversal formats.

## Why it works

### Breadth-first null markers

Each real node contributes exactly two ordered child slots. Recording all slots,
including empty ones, makes parent-child placement unambiguous. Deserialization
fills those slots in the same order, reconstructing the original structure.

### Preorder null markers

Every preorder token fills exactly one pending slot. A real node introduces its ordered left and
right slots, while a null closes a slot. This grammar uniquely reconstructs the entire original
shape.

## Walkthrough

A root 2 with only right child -1 becomes "2,#,-1,#,#". Reading the first
two child slots leaves the left empty and creates right child -1. Its next two
slots are empty. An empty tree is "#".

## Cost and pitfalls

Default approach costs and behavior:

O(n) time and O(n) auxiliary and encoding space under bounded node values.
Serialization does not mutate its input; deserialization allocates a new tree.
Do not omit null markers without a defined alternative format. Iteration handles
deep chains. Only strings produced by this codec are its input contract.

Alternative tradeoff: O(n) time; O(n) space.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """Approach: Breadth-first null markers
    Time: O(n)
    Space: O(n)
    """

    def serialize(self, root: TreeNode | None) -> str:
        tokens = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                tokens.append("#")
                continue
            tokens.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))
        first = next(tokens)
        if first == "#":
            return None
        root = TreeNode(int(first))
        queue = deque([root])
        while queue:
            node = queue.popleft()
            left, right = next(tokens), next(tokens)
            if left != "#":
                node.left = TreeNode(int(left))
                queue.append(node.left)
            if right != "#":
                node.right = TreeNode(int(right))
                queue.append(node.right)
        return root


class PreorderCodec:
    """Approach: Preorder null markers
    Time: O(n)
    Space: O(n)
    """

    def serialize(self, root: TreeNode | None) -> str:
        tokens = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                tokens.append("#")
            else:
                tokens.append(str(node.val))
                stack.extend((node.right, node.left))
        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        dummy = TreeNode()
        slots = [(dummy, "left")]
        for token in data.split(","):
            parent, side = slots.pop()
            if token == "#":
                continue
            node = TreeNode(int(token))
            setattr(parent, side, node)
            slots.extend(((node, "right"), (node, "left")))
        return dummy.left
