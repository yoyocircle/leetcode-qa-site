"""## Task

Return the maximum width of any tree level, counting missing positions between its first and
last existing nodes as if the tree were complete.

## Hints

1. Give children of position i positions 2*i and 2*i+1.
2. Subtract each level's first index before computing children to bound integer growth.

## Approach

### Normalized breadth-first positions

Queue nodes with complete-tree positions. At each layer, subtract its first position and compute
width from the first and last occupied positions.

### Leftmost index per depth

Use left-first DFS, recording the first index at each depth. Normalize every visited index by
that depth's first, update the width, and derive child indices from the normalized offset.

## Why it works

### Normalized breadth-first positions

Affine translation preserves position differences, hence widths. The binary child-index formula
preserves every internal gap, including positions occupied by missing nodes.

### Leftmost index per depth

Left-first DFS encounters the leftmost occupied position first at every depth. All indices at a
depth share the same translation, so each normalized offset measures distance from that left
edge.

## Walkthrough

For root 1 with children 2 and 3, where 2 has only a left child and 3 only a right child, the
last level occupies positions 0 and 3: width 4.

## Cost and pitfalls

Normalized breadth-first positions: O(n) time; O(w) space.
Leftmost index per depth: O(n) time; O(h) space.
The tree is unchanged. Queue length is not width when gaps exist. Normalization avoids integers
growing with depth on narrow chains; the official maximum answer fits a 32-bit signed integer.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Normalized breadth-first positions
    Time: O(n)
    Space: O(w)
    """

    def widthOfBinaryTree(self, root: TreeNode) -> int:
        queue = deque([(root, 0)])
        best = 0
        while queue:
            first = queue[0][1]
            width = queue[-1][1] - first + 1
            best = max(best, width)
            for _ in range(len(queue)):
                node, index = queue.popleft()
                index -= first
                if node.left:
                    queue.append((node.left, 2 * index))
                if node.right:
                    queue.append((node.right, 2 * index + 1))
        return best


class DepthFirstSolution:
    """Approach: Leftmost index per depth
    Time: O(n)
    Space: O(h)
    """

    def widthOfBinaryTree(self, root: TreeNode) -> int:
        first = {}
        stack = [(root, 0, 0)]
        best = 0
        while stack:
            node, depth, index = stack.pop()
            first.setdefault(depth, index)
            offset = index - first[depth]
            best = max(best, offset + 1)
            if node.right:
                stack.append((node.right, depth + 1, 2 * offset + 1))
            if node.left:
                stack.append((node.left, depth + 1, 2 * offset))
        return best
