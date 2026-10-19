"""## Task

Return every sentence formed by splitting s into dictionary words, allowing reuse and
inserting single spaces.

## Hints

1. A feasible word-ending edge can be separated from sentence reconstruction.
2. Suffix sentence lists can also be memoized when the string is short.

## Approach

### Feasible word-boundary DAG and iterative paths

Build only dictionary-word edges whose suffix can finish. Enumerate complete paths over
those boundaries with an explicit stack, then join each word sequence.

### Memoized suffix sentences

Cache every complete sentence of each reached suffix. Prefix it with each matching first
dictionary word, using an empty-string suffix as the completed base case.

## Why it works

### Feasible word-boundary DAG and iterative paths

Every sentence corresponds uniquely to a boundary path. Backward feasibility removes only
dead suffixes, so reconstruction visits all and only complete dictionary segmentations.

### Memoized suffix sentences

The first word uniquely partitions all possible sentences. Each suffix answer is combined
with every valid first-word choice, and caching reuses the same suffix completions without
removing distinct prefixes.

## Walkthrough

For "catsanddog" and ["cat","cats","and","sand","dog"], return "cats and dog" and "cat sand
dog".

## Cost and pitfalls

Feasible word-boundary DAG and iterative paths: O(W+n^3+P*n^2) expected time; O(W+n^2+P*n^2)
space.
Memoized suffix sentences: O(W+n^3+P*n^2) expected time; O(W+n+P*n^2) space.

W is total dictionary characters, n string length, and P final sentence count. Both preserve
inputs. The bounds include Python slice/hash costs and repeated partial-path or
suffix-string copying; exponential output cannot be avoided. Memo depth is at most n<=20.
Output order is unspecified.
"""


class Solution:
    """Approach: Feasible word-boundary DAG and iterative paths
    Time: O(W+n^3+P*n^2) expected
    Space: O(W+n^2+P*n^2)
    """

    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        words = set(wordDict)
        lengths = sorted({len(word) for word in words})
        successors = [[] for _ in range(len(s) + 1)]
        feasible = [False] * (len(s) + 1)
        feasible[-1] = True
        for start in range(len(s) - 1, -1, -1):
            for length in lengths:
                end = start + length
                if end > len(s):
                    break
                if feasible[end] and s[start:end] in words:
                    feasible[start] = True
                    successors[start].append(end)
        result = []
        stack = [(0, [])] if feasible[0] else []
        while stack:
            start, path = stack.pop()
            if start == len(s):
                result.append(" ".join(path))
            else:
                stack.extend((end, path + [s[start:end]]) for end in successors[start])
        return result


class MemoSolution:
    """Approach: Memoized suffix sentences
    Time: O(W+n^3+P*n^2) expected
    Space: O(W+n+P*n^2)
    """

    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        from functools import cache

        words = set(wordDict)

        @cache
        def sentences(start):
            if start == len(s):
                return ("",)
            result = []
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                if word in words:
                    for tail in sentences(end):
                        result.append(word + (" " + tail if tail else ""))
            return tuple(result)

        return list(sentences(0))
