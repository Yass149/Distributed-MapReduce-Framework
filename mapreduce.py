"""
mapreduce.py
Implements the MapReduce pipeline: Split → Map → Combine → Shuffle/Sort → Reduce
Uses Python threads so map tasks run in parallel across chunks.
"""

import csv
import threading
from collections import defaultdict


# Data loading

COLUMNS = ["PassengerId", "FlightID", "FromAirport",
           "ToAirport", "DepartureTime", "TotalFlightTime"]

def load_csv(path):
    """Load the headerless CSV and return a list of row dicts."""
    records = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if len(row) == len(COLUMNS):
                records.append(dict(zip(COLUMNS, row)))
    print(f"Loaded {len(records)} records from '{path}'")
    return records


# Split 

def split(data, chunk_size):
    """Divide data into equal-sized chunks for parallel processing."""
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


# Shuffle and Sort

def shuffle_and_sort(all_pairs):
    """Group all (key, value) pairs by key and sort keys ascending."""
    grouped = defaultdict(list)
    for key, value in all_pairs:
        grouped[key].append(value)
    return dict(sorted(grouped.items()))


# main MapReduce class

class MapReduce:
    """
    Generic MapReduce emulator with parallel map phase with anoptional combiner.

    Parameters
    ----------
    num_workers : max concurrent mapper threads
    chunk_size  : records per chunk
    """

    def __init__(self, num_workers=4, chunk_size=50):
        self.num_workers = num_workers
        self.chunk_size  = chunk_size

    def run(self, data, map_fn, reduce_fn, combiner_fn=None, job_name="Job"):
        print(f"\n--- {job_name} ---")

        # 1. Split
        chunks = split(data, self.chunk_size)
        print(f"Split: {len(data)} records → {len(chunks)} chunks")

        # 2. Map (parallel) + optional Combine
        results = [None] * len(chunks)
        semaphore = threading.Semaphore(self.num_workers)
        lock = threading.Lock()

        def worker(i, chunk):
            with semaphore:
                pairs = map_fn(chunk)
                if combiner_fn:
                    pairs = combiner_fn(pairs)  # Combine within the chunk
                with lock:
                    results[i] = pairs

        threads = [threading.Thread(target=worker, args=(i, c))
                   for i, c in enumerate(chunks)]
        for t in threads: t.start()
        for t in threads: t.join()

        all_pairs = [p for chunk_pairs in results for p in chunk_pairs]
        print(f"Map+Combine: {len(all_pairs)} intermediate pairs")

        # 3. Shuffle / Sort
        grouped = shuffle_and_sort(all_pairs)
        print(f"Shuffle/Sort: {len(grouped)} distinct keys")

        # 4. Reduce
        output = {key: reduce_fn(key, values) for key, values in grouped.items()}
        print(f"Reduce: {len(output)} output records")

        return output