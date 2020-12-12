import pandas as pd
import numpy as np

from ..clockwork_models import model_zoo

from copy import deepcopy
from azuretools.utils import read_function_invocations
from simulator.event_queue import EventQueue
from simulator.dag import Dag


# Describe benchmarks by defining a python function that outputs an EventQueus
def clockwork_sim_bench_1(path_to_invocations) -> EventQueue:
    invocations:  pd.DataFrame = read_function_invocations(path_to_invocations, start=1, end=1440)
    invocations['Total'] = invocations[list(invocations)[4:]].sum(axis=1)
    sorted_invocations = invocations.sort_values(by=['Total'], ascending=False)
    selected_invocs = sorted_invocations[200:264]

    # Assign each row of invocations to each function in the model zoo
    dags = []
    model_names = list(sorted(model_zoo.keys()))
    for (name, invocs) in zip(model_names, selected_invocs.itertuples()):
        # Slice out an 8hr section of the trace
        eight_hr_invocs = invocs[5:485]
        event_queue_invocs = []
        for (i, invs) in enumerate(eight_hr_invocs):
            # Uniformly distribute invocations across 1 min interval
            interval_invoc_times = np.linspace(0, 60000, num=int(invs), endpoint=False, dtype=int)
            for time in interval_invoc_times:
                event_queue_invocs.append(
                    (i * 60000 + time, {'latency_slo': 100}))  # Expect 100ms SLO for all func invocs
        model_dag = Dag(f"{name}_dag", [deepcopy(model_zoo[name])])
        dags.append((model_dag, event_queue_invocs))
    return EventQueue(dags)


