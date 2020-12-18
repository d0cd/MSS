from .messages import Action, ActionType, Result, Message
from .clockwork_models import model_zoo
from .executors import *

from copy import deepcopy
from queue import PriorityQueue, Queue
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
#   - If this code was turned into an actual implementation, there would be so many concurrency bugs. That's why we
#     like simulations :)

# TODO:
#   - Make executors explicitly manage resources. ATM the management logic is handled in the execute functions

class ClockworkWorker:
    workerId: int
    clock: int
    resource: Resource
    models: Dict[str, Function]
    cache: Dict[str, Function]

    # Messaging
    inbox_controller: "Queue[Message]"   # Incoming messages from the controller
    outbox_controller: "Queue[Message]"  # Outgoing messages to the controller
    outbox_controller_buf: List[Message]
    inbox_controller_buf: List[Message]

    inbox_load: "Queue[Message]"
    outbox_load: "Queue[Message]"
    inbox_load_buf: List
    outbox_load_buf: List

    inbox_infer: "Queue[Message]"
    outbox_infer: "Queue[Message]"
    inbox_infer_buf: List
    outbox_infer_buf: List

    inbox_unload: "Queue[Message]"
    outbox_unload: "Queue[Message]"
    inbox_unload_buf: List
    outbox_unload_buf: List

    # Each worker runs a dedicated executor for each action type
    # Each executor is pinned to a core so they can all run concurrently
    # The PQ elements are (earliest time Action can exec, Action, time received by worker)
    loadExecutor: LoadExecutor
    inferExecutor: InferExecutor
    unloadExecutor: UnloadExecutor

    def __init__(self, _workerId: int, _inbox_controller: "Queue[Message]", _outbox_controller: "Queue[Message]"):
        self.workerId = _workerId
        self.clock = 0
        self.cache = {}
        # Messaging
        self.inbox_controller = _inbox_controller
        self.outbox_controller = _outbox_controller
        self.inbox_controller_buf = []
        self.outbox_controller_buf = []

        self.inbox_load = Queue()
        self.outbox_load = Queue()
        self.inbox_load_buf, self.outbox_load_buf = [], []

        self.inbox_infer = Queue()
        self.outbox_infer = Queue()
        self.inbox_infer_buf, self.outbox_infer_buf = [], []

        self.inbox_unload = Queue()
        self.outbox_unload = Queue()
        self.inbox_unload_buf, self.outbox_unload_buf = [], []

        # Other
        self.resource = Resource('NVIDIA_TESLA_V100_GPU', ResourceType.GPU)
        self.models = deepcopy(model_zoo)
        self.loadExecutor = LoadExecutor(self.workerId, self.outbox_load, self.inbox_load, self.resource, self.models, self.cache)
        self.inferExecutor = InferExecutor(self.workerId, self.outbox_infer, self.inbox_infer, self.resource, self.models, self.cache)
        self.unloadExecutor = UnloadExecutor(self.workerId, self.outbox_unload, self.inbox_unload, self.resource, self.models, self.cache)

        # Reserve space for IOCache and WorkSpace
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB
        self.resource.reserve_space(512.0 / (32.0 * 1024))  # 512MB out of 32GB

    # Steps the worker at the atomicity of 1ms
    def step(self):
        self.loadExecutor.step()
        self.inferExecutor.step()
        self.unloadExecutor.step()
        self.clock += 1

    # Read input from queues
    def input(self):
        self.loadExecutor.input()
        self.inferExecutor.input()
        self.unloadExecutor.input()
        while not self.inbox_controller.empty():
            self.inbox_controller_buf.append(self.inbox_controller.get())
        while not self.inbox_load.empty():
            self.inbox_load_buf.append(self.inbox_load.get())
        while not self.inbox_infer.empty():
            self.inbox_infer_buf.append(self.inbox_infer.get())
        while not self.inbox_unload.empty():
            self.inbox_unload_buf.append(self.inbox_unload.get())

    def output(self):
        self.loadExecutor.output()
        self.inferExecutor.output()
        self.unloadExecutor.output()
        for msg in self.outbox_controller_buf:
            self.outbox_controller.put(msg)
        self.outbox_controller_buf.clear()
        for msg in self.outbox_load_buf:
            self.outbox_load.put(msg)
        self.outbox_load_buf.clear()
        for msg in self.outbox_infer_buf:
            self.outbox_infer.put(msg)
        self.outbox_infer_buf.clear()
        for msg in self.outbox_unload_buf:
            self.outbox_unload.put(msg)
        self.outbox_unload_buf.clear()

    def exec(self):
        self.loadExecutor.exec()
        self.inferExecutor.exec()
        self.unloadExecutor.exec()
        for action in self.inbox_controller_buf:
            self.add_action(action)
        self.inbox_controller_buf.clear()
        for msg in self.inbox_load_buf:
            self.outbox_controller_buf.append(msg)
        self.inbox_load_buf.clear()
        for msg in self.inbox_infer_buf:
            self.outbox_controller_buf.append(msg)
        self.inbox_infer_buf.clear()
        for msg in self.inbox_unload_buf:
            self.outbox_controller_buf.append(msg)
        self.inbox_unload_buf.clear()

    def add_action(self, action: Action):
        assert(action.id[1] in self.models, f"Model: {action.id[1]} does not exist on this worker")  # Referenced model must exist on this worker
        action.received = self.clock
        if action.type == ActionType.LOAD:
            self.outbox_load_buf.append(action)
        elif action.type == ActionType.INFER:
            self.outbox_infer_buf.append(action)
        elif action.type == ActionType.UNLOAD:
            self.outbox_unload_buf.append(action)
        else:
            raise AssertionError(f"Action type: {action.type} is not explicitly allowed.")

    def get_lru_model_name(self) -> str:
        return min(self.cache, key=self.usage.get)




