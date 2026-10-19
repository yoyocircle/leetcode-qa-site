"""## Task

Maintain browser history from an initial homepage. Visit discards forward history; back and
forward move at most the available number of steps and return the current URL.

## Hints

1. History has one current position between a past and future.
2. A new visit must discard every entry after that position.

## Approach

### History array and cursor

Store chronological URLs and a cursor. Visit deletes the forward suffix before appending;
navigation clamps the cursor to array bounds.

### Past and future stacks

Keep a current URL, past stack, and future stack. Navigation transfers one current URL per step
between stacks; visit clears the future and pushes the old current into past.

## Why it works

### History array and cursor

The array prefix through the cursor is exactly reachable past/current history, and its suffix is
reachable future. Truncation and cursor changes preserve those meanings.

### Past and future stacks

The nearest past and future entries are their stack tops. Each transfer performs one valid
history step, while clearing future exactly implements a new navigation branch.

## Walkthrough

Start at a, visit b then c, go back to b, and visit d. Forward now stays at d because c was
discarded.

## Cost and pitfalls

History array and cursor: O(f) visit when discarding f entries; O(1) back/forward time; O(n)
space.
Past and future stacks: O(f) visit; O(min(steps,n)) navigation time; O(n) space.
Objects own their history. Python deletion and clear release f references, so a branching visit
is not worst-case constant time. Returning a URL string does not expose mutable history storage.
"""


class BrowserHistory:
    """Approach: History array and cursor
    Time: O(f) visit when discarding f entries; O(1) back/forward
    Space: O(n)
    """

    def __init__(self, homepage: str):
        self.history = [homepage]
        self.index = 0

    def visit(self, url: str) -> None:
        del self.history[self.index + 1 :]
        self.history.append(url)
        self.index += 1

    def back(self, steps: int) -> str:
        self.index = max(0, self.index - steps)
        return self.history[self.index]

    def forward(self, steps: int) -> str:
        self.index = min(len(self.history) - 1, self.index + steps)
        return self.history[self.index]


class TwoStackBrowserHistory:
    """Approach: Past and future stacks
    Time: O(f) visit; O(min(steps,n)) navigation
    Space: O(n)
    """

    def __init__(self, homepage: str):
        self.current = homepage
        self.past = []
        self.future = []

    def visit(self, url: str) -> None:
        self.past.append(self.current)
        self.current = url
        self.future.clear()

    def back(self, steps: int) -> str:
        for _ in range(min(steps, len(self.past))):
            self.future.append(self.current)
            self.current = self.past.pop()
        return self.current

    def forward(self, steps: int) -> str:
        for _ in range(min(steps, len(self.future))):
            self.past.append(self.current)
            self.current = self.future.pop()
        return self.current
