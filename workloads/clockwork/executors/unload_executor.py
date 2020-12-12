from .base_executor import Executor
from ..messages import Action, Result, Code

from queue import PriorityQueue
from simulator.dag import Function
from simulator.resource import Resource
from typing import Tuple, Dict, List, Any


class UnloadExecutor(Executor):
    workerId: int
    resource: Resource
    models: Dict[str, Function]

    def __init__(self, _workerId: int, _requestQueue: PriorityQueue[Tuple[int, Action, int]], _resource: Resource, _models: Dict[str, Function]):
        super().__init__(f"Worker:{_workerId}:UnloadExecutor", _requestQueue)
        self.workerId = _workerId
        self.resource = _resource
        self.models = _models

    # Unload executor is always free to do work if there is any avaliable
    def is_free(self) -> bool:
        return True

    # Process UNLOAD actions and send back responses
    def step(self) -> List[Result]:
        responses = []
        (earliest, action, recv) = self.requestQueue.get()
        while self.clock >= earliest:
            # We can always unload a model (almost instantly because PCIe is fast)
            if action.modelName not in self.models:
                responses.append(
                    Result(
                        Code.Error,
                        action,
                        recv,
                        self.clock,
                        f"Model: {action.modelName} is not recognized by {self.name}."
                    )
                )
            else:
                model = self.models[action.modelName]
                if self.resource.is_allocated(model, tag=None):
                    self.resource.remove_function(model, tag=None, curr_time=self.clock)
                    responses.append(
                        Result(
                            Code.Success,
                            action,
                            recv,
                            self.clock,
                            f"Model: {action.modelName} was UNLOADED by {self.name} at time {self.clock}"
                        )
                    )
                else:
                    responses.append(
                        Result(
                            Code.Error,
                            action,
                            recv,
                            self.clock,
                            f"Model: {action.modelName} was not found on resource by {self.name} at time {self.clock}"
                        )
                    )
        self.requestQueue.put((earliest, action, recv))
        self.clock += 1
        return responses

