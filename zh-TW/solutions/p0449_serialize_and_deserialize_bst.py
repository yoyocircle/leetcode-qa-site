"""## Task

Serialize and deserialize a BST into a compact string. Its strict ordering lets the encoding
omit explicit missing-child markers.

## Hints

1. Preorder plus BST ordering uniquely determines the missing boundaries.
2. An ancestor stack locates where a new right subtree begins.

## Approach

### Preorder values and ancestor stack

Serialize iterative root-left-right values. Decode in that order: smaller values attach left,
while larger values pop completed ancestors before attaching right.

### Postorder values and reversed stack

Serialize iterative left-right-root values. Decode backward, swapping the preorder roles of left
and right. Formats are private to each codec.

## Why it works

### Preorder values and ancestor stack

The first value fixes the root; strict BST intervals determine where each later value belongs.
Popping smaller ancestors finds exactly the closest ancestor whose right subtree contains the
new value.

### Postorder values and reversed stack

Reversed postorder visits root-right-left. Greater values descend right; a smaller value closes
completed right ancestors and starts the appropriate left subtree, the symmetric BST
construction.

## Walkthrough

A BST with root 5 and children 2 and 9 can encode as preorder "5,2,9" or postorder "2,9,5". Each
matching decoder restores that shape.

## Cost and pitfalls

Preorder values and ancestor stack: O(n) time; O(n) space.
Postorder values and reversed stack: O(n) time; O(n) space.
Serialization leaves the input unchanged; deserialization creates fresh nodes. Round-trip with
the same variant. Splitting the string and storing values costs linear space. Iteration supports
deep BSTs.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """Approach: Preorder values and ancestor stack
    Time: O(n)
    Space: O(n)
    """

    def serialize(self, root: TreeNode | None) -> str:
        result = []
        stack = [root] if root else []
        while stack:
            node = stack.pop()
            result.append(str(node.val))
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode | None:
        if not data:
            return None
        values = list(map(int, data.split(",")))
        root = TreeNode(values[0])
        stack = [root]
        for value in values[1:]:
            node = TreeNode(value)
            if value < stack[-1].val:
                stack[-1].left = node
            else:
                parent = stack[-1]
                while stack and value > stack[-1].val:
                    parent = stack.pop()
                parent.right = node
            stack.append(node)
        return root


class PostorderCodec:
    """Approach: Postorder values and reversed stack
    Time: O(n)
    Space: O(n)
    """

    def serialize(self, root: TreeNode | None) -> str:
        result = []
        stack = [(root, False)] if root else []
        while stack:
            node, expanded = stack.pop()
            if expanded:
                result.append(str(node.val))
            else:
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))
        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode | None:
        if not data:
            return None
        values = list(map(int, data.split(",")))
        root = TreeNode(values[-1])
        stack = [root]
        for value in reversed(values[:-1]):
            node = TreeNode(value)
            if value > stack[-1].val:
                stack[-1].right = node
            else:
                parent = stack[-1]
                while stack and value < stack[-1].val:
                    parent = stack.pop()
                parent.left = node
            stack.append(node)
        return root
