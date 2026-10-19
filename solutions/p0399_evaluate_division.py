"""## Task

Evaluate division queries from positive, consistent ratio equations; return -1 for unknown
or disconnected variables.

## Hints

1. A path product gives the ratio between its endpoints.
2. Weighted union-find can store each variable ratio to its component root.

## Approach

### Ratio-product graph search

Add each equation as a ratio edge and its reciprocal. For each query, search while
multiplying edge factors from the source.

### Weighted union-find ratios

Store variable/parent ratios and size-weighted component trees. Compress paths iteratively
while multiplying ratios, and choose the root-link ratio required by each new equation.

## Why it works

### Ratio-product graph search

Products telescope along a path to the endpoint ratio. Consistent equations ensure any
discovered path gives the same result; absence of a path means the ratio is undetermined.

### Weighted union-find ratios

The invariant weight[x]=x/parent[x] telescopes to x/root after compression. Linking roots
with the derived ratio preserves each equation; connected query ratios divide their two
root-relative weights.

## Walkthrough

If a/b=2 and b/c=3, then a/c=6 and c/a=1/6; an unknown x/x is -1.

## Cost and pitfalls

Ratio-product graph search: O(E+Q*(V+E)) time; O(V+E) space.
Weighted union-find ratios: O((E+Q)*alpha(V)) expected time; O(V) space.

Q is query count. Inputs stay unchanged. Unknown self-queries differ from known
self-queries. Floating-point products use the problem tolerance; reciprocal edges require
positive nonzero equation values.
"""


class Solution:
    """Approach: Ratio-product graph search
    Time: O(E+Q*(V+E))
    Space: O(V+E)
    """

    def calcEquation(self, equations, values, queries):
        graph = {}
        for (a, b), value in zip(equations, values, strict=True):
            graph.setdefault(a, []).append((b, value))
            graph.setdefault(b, []).append((a, 1 / value))
        answers = []
        for start, end in queries:
            if start not in graph or end not in graph:
                answers.append(-1.0)
                continue
            stack, seen = [(start, 1.0)], {start}
            answer = -1.0
            while stack:
                node, ratio = stack.pop()
                if node == end:
                    answer = ratio
                    break
                for other, factor in graph[node]:
                    if other not in seen:
                        seen.add(other)
                        stack.append((other, ratio * factor))
            answers.append(answer)
        return answers


class WeightedUnionFindSolution:
    """Approach: Weighted union-find ratios
    Time: O((E+Q)*alpha(V)) expected
    Space: O(V)
    """

    def calcEquation(self, equations, values, queries):
        parent, weight, size = {}, {}, {}

        def find(node):
            trail = []
            root = node
            while parent[root] != root:
                trail.append(root)
                root = parent[root]
            ratio = 1.0
            for item in reversed(trail):
                ratio *= weight[item]
                parent[item], weight[item] = root, ratio
            return root, weight[node]

        for (a, b), value in zip(equations, values, strict=True):
            for node in (a, b):
                if node not in parent:
                    parent[node], weight[node], size[node] = node, 1.0, 1
            ra, wa = find(a)
            rb, wb = find(b)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                parent[ra], weight[ra] = rb, value * wb / wa
                size[rb] += size[ra]
            else:
                parent[rb], weight[rb] = ra, wa / (value * wb)
                size[ra] += size[rb]
        answers = []
        for a, b in queries:
            if a not in parent or b not in parent:
                answers.append(-1.0)
                continue
            ra, wa = find(a)
            rb, wb = find(b)
            answers.append(wa / wb if ra == rb else -1.0)
        return answers
