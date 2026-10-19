"""## Task

Two nonempty linked lists store decimal digits least-significant first. Return
a new linked list representing their sum in the same order.

## Hints

1. Add matching digits with a carry, as in column arithmetic.
2. The two lists may have different lengths, and a final carry may need a node.

## Approach

### Column addition

Walk both lists while either has digits or a carry remains. Add available digits
to the carry, use divmod(total,10) for the next carry and output digit, and append
a new node through a dummy head.

### Whole-number arithmetic

Convert each reversed list to an arbitrary-precision integer using increasing decimal place
values. Add the numbers and extract output digits with divmod. This is concise but performs
arithmetic on growing integers.

## Why it works

### Column addition

After each iteration, the emitted suffix of low-order digits equals the same
digits of the true sum, and carry is exactly what must enter the next column.
Processing all columns and the final carry completes the number.

### Whole-number arithmetic

Each conversion accumulates digit times its positional power of ten, so the integer equals the
represented number. Repeated division by ten emits its sum in the required
least-significant-first order.

## Walkthrough

Lists [8,9] and [5] represent 98 and 5. The first sum is 13: write 3,
carry 1. The second is 10: write 0, carry 1. Append 1, giving [3,0,1].

## Cost and pitfalls

Default approach costs and behavior:

O(max(m,n)) time and O(1) auxiliary state, plus O(max(m,n)) new output nodes.
Both inputs are unchanged. Digits are reversed, so do not reverse the lists.
Continue for a remaining carry even after both input pointers are exhausted.

Alternative tradeoff: O(d^2) bit-operation upper bound time; O(d) space.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Approach: Column addition
    Time: O(d)
    Space: O(1) auxiliary; O(d) output
    """

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = tail = ListNode()
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next


class IntegerArithmeticSolution:
    """Approach: Whole-number arithmetic
    Time: O(d^2) bit-operation upper bound
    Space: O(d)
    """

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def number(head):
            total, place = 0, 1
            while head:
                total += head.val * place
                place *= 10
                head = head.next
            return total

        total = number(l1) + number(l2)
        dummy = tail = ListNode()
        while total:
            total, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next if dummy.next else ListNode(0)
