# Benchmarks are simply event queues.
# This file will contain a function for each type of workload, you can tweak the slo params and input dags as you see fit
# To generate your own distributions, you just need to provide the request times and the helper function will do the rest
# To print a graph of the benchmark request times use numpy histogram

import numpy as np

from simulator import EventQueue, Dag
from typing import List, Tuple
from workloads.toy.linear_dag import linear_dag


# Helper function
def assign_request_times_to_dags(dags: List[Dag], all_req_times: List[int], latency_slo, cost_slo) -> List[Tuple[Dag, List[Tuple[int, Tuple[int, int]]]]]:
    event_queue_input = []
    for i, dag in enumerate(dags):
        req_times = all_req_times[i::len(dags)]
        requests = [(time, (latency_slo, cost_slo)) for time in req_times]
        event_queue_input.append((dag, requests))
    return event_queue_input


def gen_uniform_bench(latency_slo, cost_slo, dags=[linear_dag], time_in_ms=600000, number_of_requests=60000) -> Tuple:
    all_req_times = np.linspace(0, time_in_ms, num=number_of_requests, endpoint=False, dtype=int)
    hist = np.histogram(all_req_times, bins=100, range=(0.0, float(time_in_ms)))
    return EventQueue(assign_request_times_to_dags(dags, all_req_times, latency_slo, cost_slo)), hist


# In first 1/10 of the interval, generate 1/2 requests, then evenly space out the rest
def gen_single_burst_bench(latency_slo, cost_slo, dags=[linear_dag], time_in_ms=600000, number_of_requests=60000) -> Tuple:
    burst = np.linspace(0, time_in_ms/10, num=int(number_of_requests/2), endpoint=False, dtype=int)
    coast = np.linspace(time_in_ms/10, time_in_ms, num=int(number_of_requests/2), endpoint=False, dtype=int)
    all_req_times = burst + coast
    hist = np.histogram(all_req_times, bins=100, range=(0.0, float(time_in_ms)))
    return EventQueue(assign_request_times_to_dags(dags, all_req_times, latency_slo, cost_slo)), hist


# Generate 10 pillars of high traffic
def gen_pillar_bench(latency_slo, cost_slo, dags=[linear_dag], time_in_ms=600000, number_of_requests=600000) -> Tuple:
    all_pillars = []
    mult_factor = time_in_ms / 10
    start_add_factor = 9/20 * mult_factor
    stop_add_factor = 11/20 * mult_factor
    for i in range(10):
        pillar = np.linspace(i * mult_factor + start_add_factor, i * mult_factor + stop_add_factor, num=int(number_of_requests/10), endpoint=False, dtype=int)
        all_pillars.append(pillar)
    all_req_times = np.concatenate(all_pillars)
    hist = np.histogram(all_req_times, bins=100, range=(0.0, float(time_in_ms)))
    return EventQueue(assign_request_times_to_dags(dags, all_req_times, latency_slo, cost_slo)), hist





