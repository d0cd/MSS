from .base_executor import Executor
from ..messages import Action, Result, Code, Message

from queue import PriorityQueue, Queue
from simulator.dag import Function
from simulator.resource import Resource
from typing import Tuple, Dict, List


class LoadExecutor(Executor):
    workerId: int
    resource: Resource
    models: Dict[str, Function]
    actionRecieved: int  # When was the current action received
    cache: Dict[str, int]

    def __init__(self, _workerId: int, _inbox_worker: "Queue[Message]", _outbox_worker: "Queue[Message]", _resource: Resource, _models: Dict[str, Function], _cache: Dict[str, int]):
        super().__init__(f"Worker:{_workerId}:LoadExecutor", _inbox_worker, _outbox_worker)
        self.workerId = _workerId
        self.resource = _resource
        self.models = _models
        self.actionRecieved = -1
        self.cache = _cache

    # Process UNLOAD actions and send back responses
    def exec(self):
        responses = []
        if self.requestQueue.empty(): return
        (earliest, action) = self.requestQueue.get()
        recv = action.received
        while self.clock >= earliest:
            if action.modelName not in self.models:
                responses.append(Result(Code.Error, action, recv, self.clock,
                                        f"Model: {action.modelName} is not recognized by {self.name}.")
                                 )
            if self.clock <= action.latest:
                if self.is_free():
                    model = self.models[action.modelName]
                    if self.resource.is_allocated(model, tag=None):
                        responses.append(
                            Result(Code.Error, action, recv, self.clock,
                                   f"Model: {action.modelName} was already LOADED at time {self.clock}")
                        )
                    else:
                        if self.resource.can_add_function(model, tag=None):
                            self.resource.add_function(model, tag=None, curr_time=self.clock)
                            self.currentAction = action
                            self.actionRecieved = recv
                            self.timeLeft = model.resources[self.resource.name]['pre']
                            self.cache[action.modelName] = -1
                            break
                        else:
                            responses.append(
                                Result(Code.Error, action, recv, self.clock,
                                       f"Not enough space to LOAD model: {action.modelName} by {self.name} at time {self.clock}")
                            )
                else:
                    break
            else:
                responses.append(
                    Result(Code.Error, action, recv, self.clock,
                           f"LOAD for {action.modelName} could not be serviced by {self.name} in time.")
                )
        self.requestQueue.put((earliest, action))

        # Now actually step the worker
        if self.timeLeft:
            self.timeLeft -= 1

        # Executor is finished with task
        if not self.timeLeft:
            responses.append(
                Result(Code.Success, self.currentAction, self.actionRecieved, self.clock,
                       f"Model: {self.currentAction.modelName} was LOADED by {self.name} at time {self.clock}")
            )
            self.currentAction = None
        self.outbox_worker_buf = responses

