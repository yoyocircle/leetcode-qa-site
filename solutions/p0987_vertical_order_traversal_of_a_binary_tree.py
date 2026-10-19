"""## Task

Group a binary tree into vertical columns. Within each column, order nodes by row, breaking
equal-row ties by node value. Columns run left to right.

## Hints

1. Record each node's row and column coordinates.
2. A BFS already supplies row order, leaving only same-row column ties to sort.

## Approach

### Sort coordinate triples

Iteratively gather (column,row,value) triples, globally sort them, then group consecutive equal
columns.

### BFS row buckets by column

At each BFS level collect values into column buckets, sort values within each bucket, and append
them to accumulated columns. Return columns in sorted order.

## Why it works

### Sort coordinate triples

Lexicographic triple order is exactly the specified column, row, and value priority. Grouping by
the first coordinate therefore produces the requested traversal.

### BFS row buckets by column

BFS fixes row order before appending. Sorting a level's column bucket resolves exactly its
equal-row ties; later levels append after all shallower rows.

## Walkthrough

Root 5 has children 2 and 8; 2.right=7 and 8.left=3. Column zero is [5,3,7], since the two
grandchildren share row and column and sort by value.

## Cost and pitfalls

Sort coordinate triples: O(n log(n+1)) time; O(n) space.
BFS row buckets by column: O(n log(n+1)) worst time; O(n) space.
The tree is unchanged. Ordinary left-to-right BFS alone does not satisfy equal-position value
ties. Duplicate values are separate nodes and must remain in the output. Both traversals avoid
recursion.
"""

from collections import defaultdict, deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Sort coordinate triples
    Time: O(n log(n+1))
    Space: O(n)
    """

    def verticalTraversal(self, root: TreeNode) -> list[list[int]]:
        coordinates = []
        stack = [(root, 0, 0)]
        while stack:
            node, row, col = stack.pop()
            coordinates.append((col, row, node.val))
            if node.left:
                stack.append((node.left, row + 1, col - 1))
            if node.right:
                stack.append((node.right, row + 1, col + 1))
        coordinates.sort()
        result = []
        previous = None
        for col, _, value in coordinates:
            if col != previous:
                result.append([])
                previous = col
            result[-1].append(value)
        return result


class LevelBucketSolution:
    """Approach: BFS row buckets by column
    Time: O(n log(n+1)) worst
    Space: O(n)
    """

    def verticalTraversal(self, root: TreeNode) -> list[list[int]]:
        columns = defaultdict(list)
        queue = deque([(root, 0)])
        while queue:
            level = defaultdict(list)
            for _ in range(len(queue)):
                node, col = queue.popleft()
                level[col].append(node.val)
                if node.left:
                    queue.append((node.left, col - 1))
                if node.right:
                    queue.append((node.right, col + 1))
            for col, values in level.items():
                columns[col].extend(sorted(values))
        return [columns[col] for col in sorted(columns)]
