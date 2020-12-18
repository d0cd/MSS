from .clockwork_models import model_zoo
from .clockwork_worker import ClockworkWorker
from .messages import InferenceRequest, InferenceResponse, Message, Action, Result, Code
from .performance_profile import PerformanceProfile
from .schedulers.base_scheduler import Scheduler, SchedulerType
from .schedulers.simple_scheduler import SimpleScheduler

from typing import Dict, List, Union, Optional
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
    scheduler: Scheduler

    # Messaging
    inbox_clockwork: "Queue[Message]"   # Incoming messages from Clockwork
    outbox_clockwork: "Queue[Message]"  # Outgoing messages to Clockwork
    inbox_workers: Dict[int, "Queue[Message]"]
    outbox_workers: Dict[int, "Queue[Message]"]

    inbox_clockwork_buf: List[Message]
    outbox_clockwork_buf: List[Message]
    inbox_workers_buf: Dict[int, List[Message]]
    outbox_workers_buf: Dict[int, List[Message]]

    def __init__(self, _inbox_clockwork: "Queue[Message]", _outbox_clockwork: "Queue[Message]", num_workers: int, _schedulerType: SchedulerType):
        self.workers = {}
        self.inbox_workers, self.inbox_workers_buf = {}, {}
        self.outbox_workers, self.outbox_workers_buf = {}, {}
        for i in range(num_workers):
            # Instantiate workers and messaging
            inbox_worker_i = Queue()
            outbox_worker_i = Queue()
            self.workers[i] = ClockworkWorker(i, outbox_worker_i, inbox_worker_i)
            self.inbox_workers[i] = inbox_worker_i
            self.inbox_workers_buf[i] = []
            self.outbox_workers[i] = outbox_worker_i
            self.outbox_workers_buf[i] = []
        self.inbox_clockwork = _inbox_clockwork
        self.outbox_clockwork = _outbox_clockwork
        self.inbox_clockwork_buf = []
        self.outbox_clockwork_buf = []
        self.clock = 0

        # TODO: Initialize schedulers here
        if _schedulerType == SchedulerType.SIMPLE:
            self.scheduler = SimpleScheduler()




        self.performanceProfiles = {}
        self.globalRequestQueue = PriorityQueue()

        # Instantiate worker performance profiles
        for id, worker in self.workers.items():
            profile = PerformanceProfile(
                worker.cache,
                worker.loadExecutor.requestQueue,
                worker.inferExecutor.requestQueue,
                worker.unloadExecutor.requestQueue
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

    def step(self):
        for worker in self.workers.values():
            worker.step()
        self.clock += 1
        return []

    def input(self):
        for worker in self.workers.values():
            worker.input()
        while not self.inbox_clockwork.empty():
            self.inbox_clockwork_buf.append(self.inbox_clockwork.get())
        for worker_id, inbox in self.inbox_workers.items():
            while not inbox.empty():
                self.inbox_workers_buf[worker_id].append(inbox.get())

    def exec(self):
        def dispatch_order(order: Optional[Union[InferenceResponse, Action]]):
            if isinstance(order, Action):
                self.outbox_workers_buf[order.workerId].append(order)
            elif isinstance(order, InferenceResponse):
                self.outbox_clockwork_buf.append(order)
            else:
                assert order is None
                # Skip

        for worker in self.workers.values():
            worker.exec()
        for msg in self.inbox_clockwork_buf:
            assert isinstance(msg, InferenceRequest)
            order = self.scheduler.on_request(msg)
            dispatch_order(order)
        self.inbox_clockwork_buf.clear()

        for worker_id, buf in self.inbox_workers_buf.items():
            for msg in buf:
                assert isinstance(msg, Result)
                order = self.scheduler.on_request(msg)
                dispatch_order(order)
            buf.clear()

        for order in self.scheduler.step():
            dispatch_order(order)

    def output(self):
        for worker in self.workers.values():
            worker.output()
        for msg in self.outbox_clockwork_buf:
            self.outbox_clockwork.put(msg)
        self.outbox_clockwork_buf.clear()
        for worker_id, outbox_buf in self.outbox_workers_buf.items():
            for msg in outbox_buf:
                self.outbox_workers[worker_id].put(msg)
            outbox_buf.clear()

    def on_request(self):
        pass

    def on_result(self):
        pass

    # This function may be inefficient
    def has_outstanding_requests(self) -> bool:
        return self.scheduler.has_outstanding_requests()

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

