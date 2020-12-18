from .base_executor import Executor
from ..messages import Action, Result, Code, Message

from queue import PriorityQueue, Queue
from simulator.dag import Function
from simulator.resource import Resource
from typing import Tuple, Dict, List, Any


class UnloadExecutor(Executor):
    workerId: int
    resource: Resource
    models: Dict[str, Function]
    cache: Dict[str, int]

    def __init__(self, _workerId: int, _inbox_worker: "Queue[Message]", _outbox_worker: "Queue[Message]", _resource: Resource, _models: Dict[str, Function], _cache: Dict[str, int]):
        super().__init__(f"Worker:{_workerId}:UnloadExecutor", _inbox_worker, _outbox_worker)
        self.workerId = _workerId
        self.resource = _resource
        self.models = _models
        self.cache = Dict[str, int]

    # Unload executor is always free to do work if there is any avaliable
    def is_free(self) -> bool:
        return True

    # Process UNLOAD actions and send back responses
    def exec(self):
        responses = []
        if self.requestQueue.empty(): return
        (earliest, action) = self.requestQueue.get()
        recv = action.received
        while self.clock >= earliest:
            # We can always unload a model (almost instantly because PCIe is fast)
            if action.modelName not in self.models:
                responses.append(
                    Result(Code.Error, action, recv, self.clock,
                           f"Model: {action.modelName} is not recognized by {self.name}.")
                )
            else:
                model = self.models[action.modelName]
                if self.resource.is_allocated(model, tag=None):
                    self.resource.remove_function(model, tag=None, curr_time=self.clock)
                    assert action.modelName in self.cache, "Model should be cached because its on this resource"
                    self.cache.pop(action.modelName)
                    responses.append(
                        Result(Code.Success, action, recv, self.clock,
                               f"Model: {action.modelName} was UNLOADED by {self.name} at time {self.clock}")
                    )
                else:
                    responses.append(
                        Result(Code.Error, action, recv, self.clock,
                               f"Model: {action.modelName} was not found on resource by {self.name} at time {self.clock}")
                    )
        self.requestQueue.put((earliest, action))
        self.outbox_worker_buf = responses

