from .messages import Action, ActionType, Result
from .clockwork_models import model_zoo
from .executors import *

from copy import deepcopy
from queue import PriorityQueue
from simulator.dag import Function
from simulator.resource import Resource, ResourceType
from typing import List, Tuple, Any, Dict


# Notes:
#   - We do not model INPUT and OUTPUT since they are orders of magnitude faster than EXEC and LOAD (10s of microseconds).
#     Instead they are all lumped into the INFER executor
#   - Another assumption we make is that network transfer of input and output is negligible since they are on the order of kBs
#     and Clockwork has access to 10GB/s Ethernet. This assumption is fine since we are not measuring real time performance
#     rather we are evaluating scheduling algorithms for the executing resources which dominates most of the runtime.
#   - For simplicity, each Worker is given one GPU

# TODO:
#   - Make executors explicitly manage resources. ATM the management logic is handled in the execute functions

class ClockworkWorker:
    workerId: int
    clock: int
    resource: Resource
    models: Dict[str, Function]

    # Each worker runs a dedicated executor for each action type
    # Each executor is pinned to a core so they can all run concurrently
    # The PQ elements are (earliest time Action can exec, Action, time received by worker)
    loadRequestQueue: PriorityQueue
    inferRequestQueue: PriorityQueue
    unloadRequestQueue: PriorityQueue

    loadExecutor: LoadExecutor
    inferExecutor: InferExecutor
    unloadExecutor: UnloadExecutor

    def __init__(self, _workerId: int):
        self.workerId = _workerId
        self.clock = 0
        self.resource = Resource('NVIDIA_TESLA_V100_GPU', ResourceType.GPU)
        self.models = deepcopy(model_zoo)
        self.loadRequestQueue = PriorityQueue()
        self.inferRequestQueue = PriorityQueue()
        self.unloadRequestQueue = PriorityQueue()
        self.loadExecutor = LoadExecutor(self.workerId, self.loadRequestQueue, self.resource, self.models)
        self.inferExecutor = InferExecutor(self.workerId, self.inferRequestQueue, self.resource, self.models)
        self.unloadExecutor = UnloadExecutor(self.workerId, self.unloadRequestQueue, self.resource, self.models)

        # Reserve space for IOCache and WorkSpace
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB

    # Steps the worker at the atomicity of 1ms
    def step(self, inputs: List[Action]) -> List[Result]:
        for action in inputs:
            self.add_action(action)
        loadResp = self.loadExecutor.step()
        inferResp = self.inferExecutor.step()
        unloadResp = self.unloadExecutor.step()
        self.clock += 1
        return loadResp + inferResp + unloadResp

    def add_action(self, action: Action):
        assert(action.id[1] in self.models, f"Model: {action.id[1]} does not exist on this worker")  # Referenced model must exist on this worker
        if action.type == ActionType.LOAD:
            self.loadRequestQueue.put((action.earliest, action, self.clock))
        elif action.type == ActionType.INFER:
            self.inferRequestQueue.put((action.earliest, action, self.clock))
        elif action.type == ActionType.UNLOAD:
            self.unloadRequestQueue.put((action.earliest, action, self.clock))
        else:
            raise AssertionError(f"Action type: {action.type} is not explicitly allowed.")

    def get_usage_stats(self):
        return self.inferExecutor.get_usage_stats()

    def get_lru_model_name(self):
        return self.inferExecutor.get_lru_model_name()



