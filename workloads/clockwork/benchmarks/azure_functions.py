import pandas as pd
import numpy as np

from ..clockwork_models import model_zoo
from ..messages import InferenceRequest

from copy import deepcopy
from azuretools.utils import read_function_invocations
from simulator.event_queue import EventQueue
from simulator.dag import Dag


class UniqueIdGenerator:
    _id: int

    def __init__(self):
        self._id = -1

    def get_uid(self) -> id:
        self._id += 1
        return self._id


# Describe benchmarks by defining a python function that outputs an EventQueus
def azure_bench_1(path_to_invocations) -> EventQueue:
    print("Processing Azure Function traces...")
    invocations:  pd.DataFrame = read_function_invocations(path_to_invocations, start=1, end=1440)
    invocations['Total'] = invocations[list(invocations)[4:]].sum(axis=1)
    sorted_invocations = invocations.sort_values(by=['Total'], ascending=False)
    selected_invocs = sorted_invocations[200:264]

    # Assign each row of invocations to each function in the model zoo
    print("Assembling dag...")
    dags = []
    uid_gen = UniqueIdGenerator()
    model_names = list(sorted(model_zoo.keys()))
    for (name, invocs) in zip(model_names, selected_invocs.itertuples()):
        # Slice out an 8hr section of the trace
        eight_hr_invocs = invocs[5:10]  # Temporarily set lower
        event_queue_invocs = []
        for (i, invs) in enumerate(eight_hr_invocs):
            # Uniformly distribute invocations across 1 min interval
            interval_invoc_times = np.linspace(0, 60000, num=int(invs), endpoint=False, dtype=int)
            for time in interval_invoc_times:
                req = InferenceRequest(name, 1, 100, uid_gen.get_uid())
                event_queue_invocs.append(
                    (i * 60000 + time, req))  # Expect 100ms SLO for all func invocs
        model_dag = Dag(f"{name}_dag", [deepcopy(model_zoo[name])])
        dags.append((model_dag, event_queue_invocs))
    print(f"Generating event queue...")
    return EventQueue(dags)


