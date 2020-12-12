from .clockwork_models import model_zoo
from .clockwork_worker import ClockworkWorker
from .messages import InferenceRequest

from typing import Dict, List
from queue import Queue


class ClockworkController:
    clock: int
    workers: Dict[int, ClockworkWorker]
    modelRequestQueues: Dict[str, Queue]

    def __init__(self, _workers: Dict[int, ClockworkWorker]):
        self.workers = _workers
        self.clock = 0
        self.modelRequestQueues = {name:Queue() for name in model_zoo.keys()}

    def step(self, requests: List[InferenceRequest]) -> List:
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

