"""## Task

Each input entry gives a directory followed by file-name/content pairs.
Return groups of full file paths whose contents are identical. Exclude groups
of size one; the order of groups and of paths within a group is unrestricted.

## Hints

1. The full content is the equivalence key; file names alone are insufficient.
2. Equal keys can be collected in a dictionary or made adjacent by sorting.

## Approach

### Content dictionary

Parse every record into (content, full path), then append the path to a list
under its content key. Return only lists containing at least two paths.
Python dictionaries resolve hash collisions using equality, so this does not
mistake a hash collision for equal file content.

### Sort and group records

Materialize parsed records and sort by their full content strings. Consecutive
equal keys form one group. Keep that group's paths only if it has duplicates.
This uses ordering rather than a hash table as the grouping mechanism.

## Why it works

Every parsed file is inserted exactly once. Dictionary equality puts a file
in exactly its content-equivalence class. Sorting makes each such class
contiguous because equal content keys compare equally. Filtering singleton
classes removes precisely the files without duplicates.

## Walkthrough

For "r a(x) b(y)" and "s c(x)", content x maps to r/a and s/c, while y maps
only to r/b. Return [["r/a", "s/c"]]. Equal names in different directories
would still be different paths, and different names can have equal content.

## Cost and pitfalls

Let L count parsed content and full-path characters, f be the file count, and
C the longest content. Dictionary grouping takes expected O(L) time and O(L)
space, including returned paths. Sorting takes O(L+f*C*log f) worst-case time
for lexicographic comparisons and O(L+f) space. These bounds account for
string hashing/comparison rather than treating arbitrarily long strings as
constant-size keys. Parsing follows the stated no-space record grammar.
Inputs are unchanged. This task compares the provided content, not files on disk.
"""

from collections import defaultdict
from itertools import groupby


def _files(paths):
    for entry in paths:
        directory, *records = entry.split()
        for record in records:
            name, _, content = record.partition("(")
            yield content[:-1], directory + "/" + name


class Solution:
    """Approach: Content dictionary
    Time: O(L) expected, including string hashing
    Space: O(L), including returned paths
    """

    def findDuplicate(self, paths: list[str]) -> list[list[str]]:
        groups = defaultdict(list)
        for content, path in _files(paths):
            groups[content].append(path)
        return [group for group in groups.values() if len(group) > 1]


class SortedRecordsSolution:
    """Approach: Sort and group records
    Time: O(L+f*C*log f), with f files and longest content C
    Space: O(L+f), including returned paths
    """

    def findDuplicate(self, paths: list[str]) -> list[list[str]]:
        records = sorted(_files(paths), key=lambda record: record[0])
        answer = []
        for _, group in groupby(records, key=lambda record: record[0]):
            paths_in_group = [path for _, path in group]
            if len(paths_in_group) > 1:
                answer.append(paths_in_group)
        return answer
