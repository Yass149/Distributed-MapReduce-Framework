"""
jobs/avg_duration.py
Compute average flight duration per route.

Map:     record → ((FromAirport, ToAirport), duration)
Combine: accumulate (partial_sum, count) per route to avoid passing raw values
Reduce:  combine (sum, count) pairs → final average
"""

from collections import defaultdict


def map_fn(chunk):
    pairs = []
    for r in chunk:
        try:
            pairs.append(((r["FromAirport"].strip(), r["ToAirport"].strip()),
                          float(r["TotalFlightTime"].strip())))
        except ValueError:
            pass  # skip malformed duration values
    return pairs


def combiner_fn(pairs):
    """Emit (partial_sum, count) so the reducer can compute an exact mean."""
    local = defaultdict(lambda: [0.0, 0])
    for route, dur in pairs:
        local[route][0] += dur
        local[route][1] += 1
    return [(route, tuple(v)) for route, v in local.items()]


def reduce_fn(key, values):
    total = sum(v[0] for v in values)
    count = sum(v[1] for v in values)
    return round(total / count, 2) if count else 0.0


def top_durations(output, n=10):
    return sorted(output.items(), key=lambda kv: -kv[1])[:n]