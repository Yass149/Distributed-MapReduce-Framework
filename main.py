"""
main.py
Run all three MapReduce jobs against the flight dataset.

Usage:
    python main.py
    python main.py --data path/to/data.csv --workers 8 --chunk 50
"""

import argparse
from mapreduce import MapReduce, load_csv
import jobs.passenger_count as job1
import jobs.busiest_route   as job2
import jobs.avg_duration    as job3


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data",    default="Task_A_passenger_flight_data.csv")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--chunk",   type=int, default=50)
    p.add_argument("--top",     type=int, default=10)
    return p.parse_args()


def print_table(title, rows, col1, col2):
    print(f"\n  {title}")
    print(f"  {'Rank':<6} {col1:<22} {col2:>10}")
    print(f"  {'-'*6} {'-'*22} {'-'*10}")
    for rank, (k, v) in enumerate(rows, 1):
        label = str(k) if not isinstance(k, tuple) else f"{k[0]} → {k[1]}"
        marker = " ◄ HIGHEST" if rank == 1 else ""
        print(f"  {rank:<6} {label:<22} {str(v):>10}{marker}")


def main():
    args = parse_args()
    data = load_csv(args.data)
    mr   = MapReduce(num_workers=args.workers, chunk_size=args.chunk)

    # Job 1 core requirement
    out1 = mr.run(data, job1.map_fn, job1.reduce_fn, job1.combiner_fn, "Passenger Flight Count")
    print_table("Top passengers by flight count", job1.top_passengers(out1, args.top),
                "Passenger ID", "Flights")

    # Job 2 for busiest routes
    out2 = mr.run(data, job2.map_fn, job2.reduce_fn, job2.combiner_fn, "Busiest Route")
    print_table("Busiest routes by flight count", job2.top_routes(out2, args.top),
                "Route", "Flights")

    # Job 3 average duration
    out3 = mr.run(data, job3.map_fn, job3.reduce_fn, job3.combiner_fn, "Avg Flight Duration")
    print_table("Longest routes by avg duration", job3.top_durations(out3, args.top),
                "Route", "Avg Duration")


if __name__ == "__main__":
    main()