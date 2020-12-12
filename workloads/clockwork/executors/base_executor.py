from ..messages import Action

from queue import PriorityQueue
from simulator.resource import Resource
from typing import Tuple, Optional


class Executor:
    name: str
    requestQueue: PriorityQueue
    resource: Resource
    timeLeft: int
    currentAction: Optional[Action]

    def __init__(self, _name: str, _requestQueue: PriorityQueue):
        self.name = _name
        self.requestQueue = _requestQueue
        self.clock = 0
        self.timeLeft = 0
        self.currentAction = None

    def is_free(self) -> bool:
        assert not (self.timeLeft ^ self.currentAction), "Mismatch in time left and current action"
        return self.timeLeft == 0

    def step(self):
        raise NotImplementedError("Base executor cannot be stepped.")
