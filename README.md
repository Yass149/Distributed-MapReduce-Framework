# Distributed MapReduce framework

[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
![Concurrency](https://img.shields.io/badge/execution-thread%20pool-6A1B9A)
![MapReduce](https://img.shields.io/badge/pattern-MapReduce-455A64)

A small, generic Python MapReduce engine that emulates the core batch-processing stages of Hadoop locally: split, map, combine, shuffle/sort and reduce.

> **Project status:** local distributed-systems demonstration. It uses a bounded thread pool on one machine; it is not a Hadoop cluster or production distributed service.

## Architecture

```text
input records
     │
     ▼
partitioned map tasks ──► local combiner
     │                         │
     └──────────────┬──────────┘
                    ▼
             shuffle / sort
                    │
                    ▼
                 reducers
                    │
                    ▼
              job output
```

The engine is decoupled from business logic. Jobs provide mapper/reducer behaviour; `mapreduce.py` owns execution and data movement.

## Included jobs

- `jobs/passenger_count.py` — aggregate passenger counts.
- `jobs/busiest_route.py` — identify high-volume routes.
- `jobs/avg_duration.py` — calculate average duration by route.

## Repository layout

```text
mapreduce.py                 generic execution engine
main.py                      command-line entry point
jobs/                        pluggable job definitions
Task_A_passenger_flight_data.csv  example input
```

## Run locally

```bash
git clone https://github.com/Yass149/Distributed-MapReduce-Framework.git
cd Distributed-MapReduce-Framework
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if present in your checkout
python main.py --help
python main.py --job avg_duration --input Task_A_passenger_flight_data.csv
```

## Design decisions

The combiner reduces intermediate shuffle volume before the reduce phase. A bounded thread pool demonstrates concurrent map execution without requiring Hadoop, Spark or external infrastructure. The tradeoff is important: local threads do not provide worker isolation, fault tolerance, distributed storage, network partition handling or horizontal scaling.

## Production path

For a production deployment, keep the job interface but replace the local executor with a distributed runtime, add durable input/output storage, retries, idempotent writes, schema validation, metrics and integration tests against representative data.

## Context

Built for the University of Reading CSMBD coursework. The README describes the implementation as it exists today and avoids implying cluster deployment.
