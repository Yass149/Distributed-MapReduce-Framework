"""
jobs/passenger_count.py
Core requirement: find the passengers with the highest number of flights.

Map:     record → (PassengerId, 1)
Combine: sum counts locally per chunk to reduce shuffle volume
Reduce:  sum partial counts → total flights per passenger
"""

from collections import defaultdict


def map_fn(chunk):
    """Emit (PassengerId, 1) for every flight record in the chunk."""
    return [(r["PassengerId"].strip(), 1) for r in chunk]


def combiner_fn(pairs):
    """Pre-aggregate counts locally before the shuffle phase."""
    counts = defaultdict(int)
    for pid, n in pairs:
        counts[pid] += n
    return list(counts.items())


def reduce_fn(key, values):
    """Sum all partial counts to get total flights for this passenger."""
    return sum(values)


def top_passengers(output, n=10):
    return sorted(output.items(), key=lambda kv: (-kv[1], kv[0]))[:n]