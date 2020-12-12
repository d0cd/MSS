from .actions import Action, ActionType
from .clockwork_models import model_zoo

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

class Executor:
    name: str
    response: str
    timeLeft: int
    currentAction: Action

    def __init__(self, _name: str, _response: str):
        self.name = _name
        self.response = _response

    def isFree(self) -> bool:
        return self.timeLeft == 0

    def add_job(self, action: Action, duration: int):
        assert(self.isFree())
        self.currentAction = action
        self.timeLeft = duration

    def step(self):
        if self.timeLeft > 0:
            self.timeLeft -= 1
        if self.timeLeft == 0:
            response = self.currentAction.id + (self.response)
            self.currentAction = None
            return [response]
        else:
            return []


class ClockworkWorker:
    resource: Resource
    models: Dict[str, Function]

    # Each worker runs a dedicated executor for each action type
    # Each executor is pinned to a core so they can all run concurrently
    loadRequestQueue: PriorityQueue
    inferRequestQueue: PriorityQueue
    unloadRequestQueue: PriorityQueue

    loadExecutor: Executor
    inferRequestExecutor: Executor
    unloadExecutor: Executor

    def __init__(self):
        self.resource = Resource('NVIDIA_TESLA_V100_GPU', ResourceType.GPU)
        self.models = deepcopy(model_zoo)
        self.loadRequestQueue = PriorityQueue()
        self.inferRequestQueue = PriorityQueue()
        self.unloadRequestQueue = PriorityQueue()
        self.loadExecutor = Executor("LoadExecutor", "Finished load.")
        self.inferExecutor = Executor("InferExecutor", "Finished inference.")
        self.unloadExecutor = Executor("UnloadExecutor", "Finished unload")

        # Reserve space for IOCache and WorkSpace
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB

    # Steps the worker at the atomicity of 1ms
    def step(self, time: int, inputs: List[Action]) -> List[Tuple[int, str, Any]]:
        for action in inputs:
            self.add_action(action)
        loadResp = self.execute_load(time)
        inferResp = self.execute_infer(time)
        unloadResp = self.execute_unload(time)
        return loadResp + inferResp + unloadResp

    def add_action(self, action: Action):
        assert(action.id[1] in self.models, f"Model: {action.id[1]} does not exist on this worker")  # Referenced model must exist on this worker
        if action.type == ActionType.LOAD:
            self.loadRequestQueue.put((action.earliest, action))
        elif action.type == ActionType.INFER:
            self.inferRequestQueue.put((action.earliest, action))
        elif action.type == ActionType.UNLOAD:
            self.unloadRequestQueue.put((action.earliest, action))
        else:
            raise AssertionError(f"Action type: {action.type} is not explicitly allowed.")

    ###############################################################################################################
    ### Executors
    ###############################################################################################################

    # Acquires pages from PageCache and copies weights to those pages
    def execute_load(self, time: int):
        # Clear actionable requests
        item = self.loadRequestQueue.get()
        (earliest, action) = item
        errorResps = []
        while time >= earliest:
            # Can handle this request
            if time <= action.latest:
                # Add to executor if executor is free
                if self.loadExecutor.isFree():
                    fun = self.models[action.id[1]]
                    assert not self.resource.is_allocated(fun, tag=None), "Model is already allocated on this GPU"
                    self.resource.add_function(fun, tag=None, curr_time=time)
                    self.loadExecutor.add_job(action, fun.resources['NVIDIA_TESLA_V100_GPU']['pre'])
                break
            # Cannot meet this request
            else:
                assert(time > action.latest)
                errorResps.append(action.id + ("Error: Could not meet request."))

            item = self.loadRequestQueue.get()
            (earliest, action) = item
        self.loadRequestQueue.put(item)
        executorResp = self.loadExecutor.step()
        return errorResps + executorResp

    # Execute inference. At most one at any given time.
    def execute_infer(self, time: int):
        # Clear actionable requests
        item = self.inferRequestQueue.get()
        (earliest, action) = item
        errorResps = []
        while time >= earliest:
            # Can handle this request
            if time <= action.latest:
                # Add to executor if executor is free
                if self.inferExecutor.isFree():
                    fun = self.models[action.id[1]]
                    assert self.resource.is_allocated(fun, tag=None), "Model must exist on GPU"
                    self.inferExecutor.add_job(action, fun.resources['NVIDIA_TESLA_V100_GPU'][action.batchKey])
                break
            # Cannot meet this request
            else:
                assert (time > action.latest)
                errorResps.append(action.id + ("Error: Could not meet request."))

            item = self.inferRequestQueue.get()
            (earliest, action) = item
        self.inferRequestQueue.put(item)
        executorResp = self.inferExecutor.step()
        return errorResps + executorResp

    # Update in-memory metadata. Always succeeds
    def execute_unload(self, time: int):
        # Clear actionable requests
        item = self.unloadRequestQueue.get()
        (earliest, action) = item
        resps = []
        while time >= earliest:
            # Actually unload the function
            fun = self.models[action.id[1]]
            if self.resource.is_allocated(fun, tag=None):
                self.resource.remove_function(self, fun, tag=None, curr_time=time)

            # We should always be able to handle UNLOAD requests (almost instantly)
            self.unloadExecutor.add_job(action, 0)
            resps += self.unloadExecutor.step()

            item = self.unloadRequestQueue.get()
            (earliest, action) = item
        self.unloadRequestQueue.put(item)
        return resps

