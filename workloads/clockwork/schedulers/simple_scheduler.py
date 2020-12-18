from .base_scheduler import Scheduler
from ..messages import InferenceRequest, InferenceResponse, Code, Action, Result, ActionType
from ..clockwork_models import model_zoo
from ..clockwork_worker import ClockworkWorker

from typing import Dict, Union, List, Optional, Tuple
from queue import PriorityQueue

import random

# The SimpleScheduler does the following:
    # (1) If a model exists on multiple workers GPUs, assigns requests to workers round-robin
    # (2) If a model isn't on any worker GPUs, selects a worker, round-robin, to load the GPU
    # (3) Workers execute requests FIFO
    # (4) Controller does not batch requests to the same model
    # (5) Controller only forwards 3 requests at a time to a worker

class SimpleScheduler(Scheduler):
    models = model_zoo
    batch_sizes = [1, 2, 4, 8, 16]

    clock: int
    executingRequests: Dict[int, InferenceRequest]  # All currently executing inference requests
    globalRequestQueue: PriorityQueue
    workers: Dict[int, ClockworkWorker]


    def __init__(self, _workers: Dict[int, ClockworkWorker]):
        super().__init__()
        self.executingRequests = {}
        self.globalRequestQueue = PriorityQueue()
        self.workers = _workers

    def on_request(self, req: InferenceRequest) -> Optional[Union[InferenceResponse, Action]]:
        req.arrived = self.clock
        # Prune requests that we immediately know that we cannot meet
        return self.admit_request(req)

    def on_result(self, result: Result) -> Optional[Union[InferenceResponse, Action]]:
        # If any action corresponding to an active request error, then immediately send an error
        if result.code == Code.Error and result.action.reqId in self.executingRequests:
            assert result.action.type != ActionType.UNLOAD, "UNLOADs must always succeed"
            self.remove_request(result.action.reqId)
            return InferenceResponse(result.action.modelName, -1, -1, result.action.reqId, -1, Code.Error, self.clock)

        if result.action.type == ActionType.LOAD and result.action.reqId in self.executingRequests:
            req = self.executingRequests[result.action.reqId]
            if self.estimate_execution_time(req) + self.clock > req.arrived + req.sloFactor:
                self.remove_request(result.action.reqId)
                return InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived,
                                         Code.CannotMeetSLO, self.clock)
            else:
                # Schedule this action immediately
                return self.schedule_infer(result.action.workerId, req)
        elif result.action.type == ActionType.INFER:
            assert result.action.reqId in self.executingRequests, "INFER must be part of executing requests."
            req = self.executingRequests[result.action.reqId]
            self.remove_request(result.action.reqId)
            if result.resultSent > req.arrived + req.sloFactor:
                return InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived,
                                         Code.CannotMeetSLO, self.clock)
            else:
                return InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived,
                                         Code.Success, self.clock)
        else:
            # Do nothing since UNLOADS should always work and cache state exists for each worker
            pass

    def step(self) -> List[Union[InferenceResponse, Action]]:
        orders = []
        if self.globalRequestQueue.empty(): return orders
        while not self.globalRequestQueue.empty() and len(orders) < 10:
            (latest, req) = self.globalRequestQueue.get()
            if latest < self.clock + self.estimate_execution_time(req):
                orders.append(InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived, Code.CannotMeetSLO, self.clock))

            loaded_workers, free_workers, full_workers = self.check_availability(req.modelName)
            if len(loaded_workers) > 0:
                self.schedule_infer(random.choice(loaded_workers), req)
            elif len(free_workers) > 0:
                self.schedule_load(random.choice(free_workers))
            else:
                # If system if fully loaded up just drop requests
                orders.append(InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived,
                                               Code.CannotMeetSLO, self.clock))
        self.clock += 1
        return orders


    def schedule_infer(self, workerId: int, req: InferenceRequest) -> Action:
        pass

    def schedule_load(self, workerId: int, req: InferenceResponse) -> Action:
        pass

    # TODO: Not used at the moment
    def schedule_unload(self, workerId: int, req: InferenceRequest) -> Action:
        pass

    def admit_request(self, req: InferenceRequest) -> Optional[InferenceResponse]:
        if req.modelName not in self.models or req.batchSize not in self.batch_sizes:
            return InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived, Code.Error, self.clock)
        if self.estimate_execution_time(req, self.) > req.sloFactor:
            return InferenceResponse(req.modelName, req.batchSize, req.sloFactor, req.uniqueId, req.arrived, Code.CannotMeetSLO, self.clock)
        self.globalRequestQueue.put((self.clock + req.sloFactor), req)

    # TODO: Find models
    def check_availability(self, modelName: str) -> Tuple[List[int], List[int], List[int]]:
        return False

    def is_loaded(self, modelName: str) -> bool:
        return False

    # TODO: Purge reqId from all scheduler state
    def remove_request(self, reqId: int):
        pass

    # TODO: Estimate should be made based on worker state
    def estimate_execution_time(self, req: InferenceRequest, isLoaded: bool) -> int:
        resource = self.models[req.modelName].resources['NVIDIA_TESLA_V100_GPU']
        assert f"exec_b{req.batchSize}" in resource, "Batch execution times should be in model specification"
        estimate = resource[f"exec_b{req.bar}"]
        if not isLoaded:
            estimate += resource['pre']
        return estimate

    def has_outstanding_requests(self) -> bool:
        return len(self.executingRequests) > 0 or not self.globalRequestQueue.empty()


