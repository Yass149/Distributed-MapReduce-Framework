# CSMBD Task A — MapReduce Emulator

## How to run
python main.py
python main.py --data Task_A_passenger_flight_data.csv --workers 4 --chunk 50 --top 10

## Requirements
Python 3.8+ — no external libraries needed (stdlib only: csv, threading, collections)

## Project structure
mapreduce.py          — full framework (load, split, map, shuffle, reduce)
main.py               — entry point
jobs/passenger_count.py  — core requirement
jobs/busiest_route.py    — extended analysis
jobs/avg_duration.py     — extended analysis