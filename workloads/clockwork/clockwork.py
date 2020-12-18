from .clockwork_controller import ClockworkController
from .messages import InferenceRequest, InferenceResponse, Message, Code
from .schedulers.base_scheduler import SchedulerType

from simulator.event_queue import EventQueue
from simulator.system import System

from datetime import datetime
from typing import Dict, List
from queue import Queue

# TODO: Message queue abstraction needs to be refined. Presently the message queues are input to step
# TODO: Sanity check on clocks
# TODO: Logging and telemetry


class Clockwork(System):
    controller: ClockworkController

    # Messaging
    inbox_controller: "Queue[Message]"   # Incoming messages from the controller
    outbox_controller: "Queue[Message]"  # Outgoing messages to the controller
    outbox_controller_buf: List[Message]

    # Logging state
    numReqIssued: int
    numRespRecv: int
    numSLOSat: int
    numSLONotSat: int
    numErrors: int

    # Temp
    minute: int

    def __init__(self, _events: EventQueue, num_workers: int, scheduler_type: SchedulerType):
        super().__init__(_events)
        # Instantiate messaging
        self.inbox_controller = Queue()
        self.outbox_controller = Queue()
        self.outbox_controller_buf = []

        # Instantiate controller
        self.controller = ClockworkController(self.outbox_controller, self.inbox_controller, num_workers, scheduler_type)
        self.minute = -1

        # Logging state
        self.numReqIssued = 0
        self.numRespRecv = 0
        self.numSLOSat = 0
        self.numSLONotSat = 0
        self.numErrors = 0

    def step(self):
        if self.clock % 60000 == 0:
            print(f"Minute: {self.clock // 60000 }")
        self.controller.step()
        print(f"Clock: {self.clock}")
        self.clock += 1

    # This stage gets messages back from the controllers, so do logging here
    def input(self):
        self.controller.input()
        resps = []
        while not self.inbox_controller.empty():
            resps.append(self.inbox_controller.get())
        self.log_responses(resps)

    def exec(self):
        self.controller.exec()
        (_, absolute_time, _) = self.events.peek()
        # If the event has arrived, then handle it
        assert self.clock <= absolute_time, "Clock should never go ahead of the event queue"
        if self.clock == absolute_time:
            (requests, _, _) = self.events.get_next_event()
            for (_, req) in requests:
                assert isinstance(req, InferenceRequest)
                self.outbox_controller_buf.append(req)
        self.numReqIssued += len(self.outbox_controller_buf)

    def output(self):
        self.controller.output()
        for msg in self.outbox_controller_buf:
            self.outbox_controller.put(msg)
        self.outbox_controller_buf.clear()

    def run(self):
        start_time = datetime.now()
        print("Running Clockwork...")
        while self.events.has_more_events() or self.controller.has_outstanding_requests():
            self.input()
            self.exec()
            self.output()
            self.step()
            if self.clock == 10000: break
        end_time = datetime.now()
        simulation_time = self.clock / 1000
        real_time = (end_time - start_time).total_seconds()

        print(f"Execution finished at time: {self.clock}ms")
        print(f"Simulated {simulation_time} seconds in {real_time}. Simulation Factor: {simulation_time / real_time}")
        print(f"Requests Issued: {self.numReqIssued}")
        print(f"Responses Received: {self.numRespRecv}")
        print(f"Number of SLOs satisfied: {self.numSLOSat}")
        print(f"Number of SLOs violated: {self.numSLONotSat}")

    def schedule(self, curr_time, events, *args, **kwargs):
        raise NotImplementedError("Schedule abstraction looks different for Clockwork")

    def log_responses(self, responses: List[InferenceResponse]):
        self.numRespRecv += len(responses)
        for resp in responses:
            if resp.code == Code.Success:
                self.numSLOSat += 1
            elif resp.code == Code.Error:
                self.numErrors += 1
            else:
                self.numSLONotSat += 1
