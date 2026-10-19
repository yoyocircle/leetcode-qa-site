"""
## Task

Hire exactly k workers. Each worker needs at least wage[i], and all chosen workers must receive
the same pay per unit of quality. Return the minimum total pay.

## Hints

1. A group pays at its largest minimum wage-to-quality ratio.
2. For a fixed maximum ratio, choose the k smallest eligible qualities.

## Approach

### Ratio sweep with a largest-quality heap

Sort workers by required ratio. Maintain the k smallest qualities seen using a max-heap, and
evaluate their total quality times the current ratio.

### Enumerate exact rate thresholds

Use each worker ratio as a candidate rate. Determine eligibility by exact cross multiplication,
sort eligible qualities, and sum the smallest k. This educational baseline may time out at full
constraints.

## Why it works

### Ratio sweep with a largest-quality heap

Every optimal group has a highest-ratio member. At that sweep point all its workers are
eligible, and choosing the k smallest qualities minimizes cost for that rate. Evaluating every
rate therefore includes a group no worse than the optimum.

### Enumerate exact rate thresholds

An optimal rate must equal some worker minimum ratio. For each such rate, exact eligibility
includes precisely workers whose requirements are met, and the smallest k quality values
minimize the shared-rate total.

## Walkthrough

quality=[10,20,5], wage=[70,50,30], k=2 can choose qualities 10 and 5 at rate 7, paying 105
total.

## Cost and pitfalls

Ratio sweep with a largest-quality heap: O(n log n+n log k) time; O(n+k) space.

Enumerate exact rate thresholds: O(n squared log n) time; O(n) space.

Inputs are unchanged. The heap stores negative qualities to evict the largest. Python float
division is used only for rates and final costs; answers are judged with tolerance. Exact cross
multiplication avoids eligibility rounding in the baseline.
"""

from heapq import heappop, heappush


class Solution:
    """Approach: Ratio sweep with a largest-quality heap
    Time: O(n log n+n log k)
    Space: O(n+k)
    """

    def mincostToHireWorkers(self, quality: list[int], wage: list[int], k: int) -> float:
        workers = sorted(
            (required / amount, amount) for amount, required in zip(quality, wage, strict=True)
        )
        heap = []
        total = 0
        answer = float("inf")
        for ratio, amount in workers:
            heappush(heap, -amount)
            total += amount
            if len(heap) > k:
                total += heappop(heap)
            if len(heap) == k:
                answer = min(answer, ratio * total)
        return answer


class RateEnumerationSolution:
    """Approach: Enumerate exact rate thresholds
    Time: O(n squared log n)
    Space: O(n)
    """

    def mincostToHireWorkers(self, quality: list[int], wage: list[int], k: int) -> float:
        answer = float("inf")
        for denominator, numerator in zip(quality, wage, strict=True):
            eligible = sorted(
                amount
                for amount, required in zip(quality, wage, strict=True)
                if required * denominator <= numerator * amount
            )
            if len(eligible) >= k:
                cost = sum(eligible[:k]) * numerator / denominator
                answer = min(answer, cost)
        return answer
