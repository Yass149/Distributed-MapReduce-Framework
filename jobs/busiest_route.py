"""
jobs/busiest_route.py
Find the busiest routes (FromAirport → ToAirport) by number of flights.

Map:     record → ((FromAirport, ToAirport), 1)
Combine: sum counts locally per route per chunk
Reduce:  sum partial counts → total flights per route
"""

from collections import defaultdict

def map_fn(chunk):
    return [((r["FromAirport"].strip(), r["ToAirport"].strip()), 1) for r in chunk]


def combiner_fn(pairs):
    counts = defaultdict(int)
    for route, n in pairs:
        counts[route] += n
    return list(counts.items())

def reduce_fn(key, values):
    return sum(values)

def top_routes(output, n=10):
    return sorted(output.items(), key=lambda kv: -kv[1])[:n]