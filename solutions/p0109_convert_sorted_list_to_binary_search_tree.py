"""## Task

Convert an ascending singly linked list to a height-balanced BST containing the same values. The
input list must remain available unchanged.

## Hints

1. Balanced subtree sizes can be chosen before consuming their values.
2. An inorder construction can advance one shared list cursor exactly once per output node.

## Approach

### Inorder simulation by subtree size

Count list nodes. Build a balanced left subtree of size n//2, consume the current list value for
the root, and build the remaining right subtree.

### Array snapshot and middle splits

Copy list values to an array. Build subtrees using middle indices and interval bounds, without
recursively slicing arrays.

## Why it works

### Inorder simulation by subtree size

The left construction consumes exactly the smaller prefix, so the next value is the correct
root. Balanced size splitting bounds height, and inorder consumption preserves sorted BST order.

### Array snapshot and middle splits

Each midpoint separates smaller and larger values, making a BST. Splitting each interval near
its midpoint keeps child heights within one, yielding a balanced tree.

## Walkthrough

For list [-3,0,4,9], one result has root 4, left subtree rooted at 0 with left child -3, and
right leaf 9.

## Cost and pitfalls

Inorder simulation by subtree size: O(n) time; O(log n) auxiliary; O(n) output space.
Array snapshot and middle splits: O(n) time; O(n) auxiliary and output space.
Both allocate new tree nodes and leave every list value and next pointer unchanged. Recursion
depth is logarithmic despite potentially long input lists. Repeatedly searching list midpoints
would add an unnecessary logarithmic time factor.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Approach: Inorder simulation by subtree size
    Time: O(n)
    Space: O(log n) auxiliary; O(n) output
    """

    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        current, count = head, 0
        while current:
            count += 1
            current = current.next
        current = head

        def build(size):
            nonlocal current
            if size == 0:
                return None
            left = build(size // 2)
            root = TreeNode(current.val)
            current = current.next
            root.left = left
            root.right = build(size - size // 2 - 1)
            return root

        return build(count)


class ArraySolution:
    """Approach: Array snapshot and middle splits
    Time: O(n)
    Space: O(n) auxiliary and output
    """

    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        values = []
        while head:
            values.append(head.val)
            head = head.next

        def build(low, high):
            if low == high:
                return None
            middle = (low + high) // 2
            return TreeNode(values[middle], build(low, middle), build(middle + 1, high))

        return build(0, len(values))
