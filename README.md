# CSMBD Task A: Distributed MapReduce Framework

**Author:** Yassine Malal

**Module:** CSMBD (Big Data and Cloud Computing)

**Institution:** University of Reading

## Overview
This repository contains a custom, fully generic MapReduce emulator written in Python. It is designed to process and analyze flight and passenger datasets by simulating the core distributed data processing phases of Apache Hadoop (Split, Map, Combine, Shuffle/Sort, Reduce). 

The framework leverages a bounded thread pool for concurrent map execution and implements local pre-aggregation (a Combiner) to significantly reduce shuffle data volume.

## Project Structure
The architecture decouples the generic MapReduce engine from the specific business logic (jobs).

```text
csmbd-task-a/
│
├── jobs/                       # Business logic for specific MapReduce tasks
│   ├── __init__.py
│   ├── avg_duration.py         # Job 3: Calculates average duration per route
│   ├── busiest_route.py       # Job 2: Identifies routes with the most flights
│   └── passenger_count.py      # Job 1: Counts total flights per passenger
│
├── main.py                     # Entry point and command-line execution
├── mapreduce.py                # Core generic engine (Split, Map, Shuffle, Reduce)
├── Task_A_passenger_flight_data.csv # Raw dataset
└── README.md
```
## How to Run
This framework requires no external distributed dependencies (like Hadoop) as it relies on Python's native threading pool.

1. Ensure you have Python 3.x installed.
2. Clone the repository and navigate to the root directory.
3. Execute the main MapReduce engine against the raw dataset:
`python main.py --job avg_duration --input Task_A_passenger_flight_data.csv`
