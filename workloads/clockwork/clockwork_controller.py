from .clockwork_models import model_zoo
from .clockwork_worker import ClockworkWorker
from .messages import InferenceRequest
from .performance_profile import PerformanceProfile

from typing import Dict, List
from queue import Queue


# NOTE:
#   - One assumption we make is that the Controller has a 'perfect' view of each worker's state.
#     This assumption corresponds to a Clockwork deployment with very good telemetry and logging.
#     This is implemented by having workers manage their own performance profiles, while only
#     allowing the Controller to read them. Note that the design of this code allows modifications to
#     this idea while also preserving the abstraction of a performance profile.


class ClockworkController:
    clock: int
    workers: Dict[int, ClockworkWorker]
    modelRequestQueues: Dict[str, Dict[int, Queue]]
    performanceProfiles: Dict[int, PerformanceProfile]

    def __init__(self, _workers: Dict[int, ClockworkWorker]):
        self.workers = _workers
        self.clock = 0
        self.modelRequestQueues = {}

        # Instantiate model request queues for each batch size
        for modelName in model_zoo.keys():
            self.modelRequestQueues[modelName] = {
                1: Queue(),
                2: Queue(),
                4: Queue(),
                8: Queue(),
                16: Queue()
            }

        # Instantiate worker performance profiles
        for id, worker in self.workers.items():
            profile = PerformanceProfile(
                        worker.cache,
                        worker.loadRequestQueue,
                        worker.inferRequestQueue,
                        worker.unloadRequestQueue
                      )
            self.performanceProfiles[id] = profile

    def step(self, requests: List[InferenceRequest]) -> List:
        self._add_requests_to_batch_queues(requests)
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
            batchQueues = self.modelRequestQueues[req.modelName]
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

