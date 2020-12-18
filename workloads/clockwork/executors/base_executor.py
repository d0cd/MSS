from ..messages import Action, Message

from queue import PriorityQueue, Queue
from simulator.resource import Resource
from typing import Tuple, Optional, List


class Executor:
    name: str
    requestQueue: PriorityQueue
    resource: Resource
    timeLeft: int
    currentAction: Optional[Action]

    # Messaging
    inbox_worker: "Queue[Message]"  # Incoming messages from Worker
    outbox_worker: "Queue[Message]" # Outgoing messages to Worker
    inbox_worker_buf: List[Message]
    outbox_worker_buf: List[Message]

    def __init__(self, _name: str, _inbox_worker: "Queue[Message]", _outbox_worker: "Queue[Message]"):
        self.name = _name
        self.inbox_worker = _inbox_worker
        self.outbox_worker = _outbox_worker
        self.outbox_worker_buf = []
        self.requestQueue = PriorityQueue()
        self.clock = 0
        self.timeLeft = 0
        self.currentAction = None

    def is_free(self) -> bool:
        assert not (self.timeLeft ^ self.currentAction), "Mismatch in time left and current action"
        return self.timeLeft == 0

    def step(self):
        self.clock += 1

    def input(self):
        while not self.inbox_worker.empty():
            msg = self.inbox_worker.get()
            assert isinstance(msg, Action)
            self.requestQueue.put((msg.earliest, msg))

    def exec(self):
        raise NotImplementedError("Base executor cannot execute")

    def output(self):
        for msg in self.outbox_worker_buf:
            self.outbox_worker.put(msg)
        self.outbox_worker_buf.clear()
