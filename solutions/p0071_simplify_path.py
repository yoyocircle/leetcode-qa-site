"""
## Task

Canonicalize an absolute Unix path: collapse repeated separators, ignore dot components, and
make double dots move up without passing root.

## Hints

1. A stack records the retained directory components.
2. Only exact components dot and double dot are special.

## Approach

### Split components and reduce

Split on slashes and reduce components into a directory stack, then join them under root.

### Streaming character parser

Scan characters and flush each component at a slash, avoiding a separate array of all split
components.

## Why it works

### Split components and reduce

After every component the stack is the canonical path to that point. Ordinary names descend, dot
stays, and double dot removes the latest descent if present.

### Streaming character parser

The parser emits exactly the same component sequence as separator splitting. Reducing each
emitted component keeps the stack equal to the canonical prefix path.

## Walkthrough

"/a//b/../c/./" becomes "/a/c". A component "..." is an ordinary directory name.

## Cost and pitfalls

Split components and reduce: O(n) time; O(n) space.

Streaming character parser: O(n) time; O(n) space.

Input is unchanged. This is lexical path normalization, with no filesystem or symbolic-link
lookup. Both methods retain the root slash.
"""


class Solution:
    """Approach: Split components and reduce
    Time: O(n)
    Space: O(n)
    """

    def simplifyPath(self, path: str) -> str:
        directories = []
        for part in path.split("/"):
            if part == "..":
                if directories:
                    directories.pop()
            elif part and part != ".":
                directories.append(part)
        return "/" + "/".join(directories)


class StreamingSolution:
    """Approach: Streaming character parser
    Time: O(n)
    Space: O(n)
    """

    def simplifyPath(self, path: str) -> str:
        directories, component = [], []
        for char in path + "/":
            if char != "/":
                component.append(char)
                continue
            name = "".join(component)
            component.clear()
            if name == "..":
                if directories:
                    directories.pop()
            elif name and name != ".":
                directories.append(name)
        return "/" + "/".join(directories)
