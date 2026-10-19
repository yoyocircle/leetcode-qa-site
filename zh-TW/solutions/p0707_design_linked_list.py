"""## Task

Implement indexed get, insertion at head/tail/index, and deletion by index for a mutable linked
list. Invalid get returns -1; invalid insertion or deletion leaves the list unchanged.

## Hints

1. Dummy boundaries remove special cases for empty and end operations.
2. A doubly linked representation can search from whichever end is nearer.

## Approach

### Doubly linked sentinels

Maintain head/tail sentinels and size. Locate indexed nodes from the closer boundary, then
splice or unlink with reciprocal pointer updates.

### Dummy-headed singly linked list

Keep one dummy head and size. Walk to the indexed predecessor before insertions and deletions;
get walks directly to its target.

## Why it works

### Doubly linked sentinels

The sentinel chain contains exactly size live nodes in list order. Searching counts the
requested number of links; local splice/unlink changes exactly that indexed position while
preserving all others.

### Dummy-headed singly linked list

The predecessor is the unique incoming link for the target position. Replacing that link
implements insertion or deletion without needing backward pointers.

## Walkthrough

Add head 2, add tail 5, insert 3 at index 1: the list is [2,3,5]. Delete index 1 and get(1)
returns 5.

## Cost and pitfalls

Doubly linked sentinels: O(1) end insertion; O(min(i,n-i)+1) indexed operations time; O(n)
space.
Dummy-headed singly linked list: O(n) indexed/tail operations; O(1) head insertion time; O(n)
space.
Objects own all nodes. Index equal to size is valid insertion but invalid get/deletion.
Nonpositive insertion indices act as head insertion. Return no replacement nodes to callers;
index bounds use the current size.
"""


class ListEntry:
    def __init__(self, value=0):
        self.value = value
        self.previous = self.next = None


class MyLinkedList:
    """Approach: Doubly linked sentinels
    Time: O(1) end insertion; O(min(i,n-i)+1) indexed operations
    Space: O(n)
    """

    def __init__(self):
        self.head, self.tail = ListEntry(), ListEntry()
        self.head.next = self.tail
        self.tail.previous = self.head
        self.size = 0

    def _node(self, index):
        if index < self.size // 2:
            node = self.head.next
            for _ in range(index):
                node = node.next
        else:
            node = self.tail.previous
            for _ in range(self.size - index - 1):
                node = node.previous
        return node

    def get(self, index: int) -> int:
        return self._node(index).value if 0 <= index < self.size else -1

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        index = max(index, 0)
        if index > self.size:
            return
        after = self.tail if index == self.size else self._node(index)
        before = after.previous
        node = ListEntry(val)
        node.previous, node.next = before, after
        before.next = after.previous = node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.size:
            return
        node = self._node(index)
        node.previous.next = node.next
        node.next.previous = node.previous
        self.size -= 1


class SinglyLinkedList:
    """Approach: Dummy-headed singly linked list
    Time: O(n) indexed/tail operations; O(1) head insertion
    Space: O(n)
    """

    def __init__(self):
        self.head = ListEntry()
        self.size = 0

    def get(self, index: int) -> int:
        if not 0 <= index < self.size:
            return -1
        node = self.head.next
        for _ in range(index):
            node = node.next
        return node.value

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        index = max(index, 0)
        if index > self.size:
            return
        before = self.head
        for _ in range(index):
            before = before.next
        node = ListEntry(val)
        node.next = before.next
        before.next = node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.size:
            return
        before = self.head
        for _ in range(index):
            before = before.next
        before.next = before.next.next
        self.size -= 1
