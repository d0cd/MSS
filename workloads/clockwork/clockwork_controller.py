from .clockwork_models import model_zoo
from .clockwork_worker import ClockworkWorker
from .messages import InferenceRequest, InferenceResponse
from .performance_profile import PerformanceProfile

from simulator import Resource

from typing import Dict, List
from queue import Queue, PriorityQueue


# NOTE:
#   - One assumption we make is that the Controller has a 'perfect' view of each worker's state.
#     This assumption corresponds to a Clockwork deployment with very good telemetry and logging.
#     This is implemented by having workers manage their own performance profiles, while only
#     allowing the Controller to read them. Note that the design of this code allows modifications to
#     this idea while also preserving the abstraction of a performance profile.
#   - Limitation: This Controller implements SimpleScheduler from the Clockwork source code
#   - Batch


class ClockworkController:
    clock: int
    workers: Dict[int, ClockworkWorker]
    globalRequestQueue: PriorityQueue
    modelRequestQueues: Dict[str, Queue]
    batchRequestQueues: Dict[str, Dict[int, Queue]]
    performanceProfiles: Dict[int, PerformanceProfile]

    def __init__(self, _workers: Dict[int, ClockworkWorker]):
        self.workers = _workers
        self.clock = 0
        self.performanceProfiles = {}
        self.globalRequestQueue = PriorityQueue()

        # Instantiate worker performance profiles
        for id, worker in self.workers.items():
            profile = PerformanceProfile(
                worker.cache,
                worker.loadRequestQueue,
                worker.inferRequestQueue,
                worker.unloadRequestQueue
            )
            self.performanceProfiles[id] = profile

        # Note: The below structures are not used in scheduling logic
        # Instantiate model request queues for each batch size
        self.modelRequestQueues = {name:Queue() for name in model_zoo.keys()}
        self.batchRequestQueues = {}
        for modelName in model_zoo.keys():
            self.batchRequestQueues[modelName] = {
                1: Queue(),
                2: Queue(),
                4: Queue(),
                8: Queue(),
                16: Queue()
            }

    # The SimpleScheduler does the following:
    # (1) If a model exists on multiple workers GPUs, assigns requests to workers round-robin
    # (2) If a model isn't on any worker GPUs, selects a worker, round-robin, to load the GPU
    # (3) Workers execute requests FIFO
    # (4) Controller does not batch requests to the same model
    # (5) Controller only forwards 3 requests at a time to a worker

    def step(self, requests: List[InferenceRequest]) -> List[InferenceResponse]:
        #self._add_requests_to_batch_queues(requests)
        self.clock += 1
        return []

    def on_request(self):
        pass

    def on_result(self):
        pass

    # This function may be inefficient
    def has_outstanding_requests(self) -> bool:
        for (_, queue) in self.modelRequestQueues.items():
            if not queue.empty():
                return True
        return False

    def _add_requests_to_batch_queues(self, requests: List[InferenceRequest]):
        for req in requests:
            assert req.batchSize > 0, f"Invalid batch size"
            batchQueues = self.batchRequestQueues[req.modelName]
            if req.batchSize <= 16:
                batchQueues[16].put(req)
            if req.batchSize <= 8:
                batchQueues[8].put(req)
            if req.batchSize <= 4:
                batchQueues[4].put(req)
            if req.batchSize <= 2:
                batchQueues[2].put(req)
            if req.batchSize <= 1:
                batchQueues[1].put(req)
            self.modelRequestQueues[req.modelName].put(req)
            self.globalRequestQueue.put((self.clock + req.sloFactor), req)

