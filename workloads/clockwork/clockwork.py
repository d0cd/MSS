from .clockwork_controller import ClockworkController
from .clockwork_worker import ClockworkWorker
from .messages import InferenceRequest, InferenceResponse

from simulator.event_queue import EventQueue
from simulator.system import System

from typing import Dict, List

# TODO: Message queue abstraction needs to be refined. Presently the message queues are input to step
# TODO: Sanity check on clocks
# TODO: Logging and telemetry


class Clockwork(System):
    workers: Dict[int, ClockworkWorker]
    controller: ClockworkController

    # Logging state
    numReqIssued: int
    numRespRecv: int
    numSLOSat: int
    numSLONotSat: int

    # Temp
    minute: int

    def __init__(self, _events: EventQueue, num_workers):
        super().__init__(_events)
        # Instantiate workers
        self.workers = {}
        for i in range(num_workers):
            self.workers[i] = ClockworkWorker(i)
        # Instantiate controller
        self.controller = ClockworkController(self.workers)
        self.minute = -1

        # Logging state
        self.numReqIssued = 0
        self.numRespRecv = 0
        self.numSLOSat = 0
        self.numSLONotSat = 0

    def step(self, reqs: List[InferenceRequest]):
        resps = self.controller.step(reqs)
        self.clock += 1
        return resps

    def run(self):
        print("Running Clockwork...")
        while self.events.has_more_events():
            controller_requests = []
            (_, absolute_time, _) = self.events.peek()
            # If the event has arrived, then handle it
            assert self.clock <= absolute_time, "Clock should never go ahead of the event queue"
            if self.clock == absolute_time:
                (requests, _, _) = self.events.get_next_event()
                for (_, req) in requests:
                    assert isinstance(req, InferenceRequest)
                    controller_requests.append(req)
            self.numReqIssued += len(controller_requests)
            controller_responses = self.step(controller_requests)
            self.log_responses(controller_responses)

            # Temp logging
            # TODO: Remove
            if self.clock % 60000 == 0:
                self.minute += 1
                print(f"Minute: {self.minute}")

        while self.controller.has_outstanding_requests():
            controller_responses = self.step([])
            self.log_responses(controller_responses)

            # Temp logging
            # TODO: Remove
            if self.clock % 60000 == 0:
                self.minute += 1
                print(f"Minute: {self.minute}")

        print(f"Execution finished at time: {self.clock}ms")
        print(f"Requests Issued: {self.numReqIssued}")
        print(f"Responses Received: {self.numRespRecv}")
        print(f"Number of SLOs satisfied: {self.numSLOSat}")
        print(f"Number of SLOs violated: {self.numSLONotSat}")

    def schedule(self, curr_time, events, *args, **kwargs):
        raise NotImplementedError("Schedule abstraction looks different for Clockwork")

    def log_responses(self, responses: List[InferenceResponse]):
        self.numRespRecv += len(responses)
        for resp in responses:
            if resp.satisfied_slo():
                self.numSLOSat += 1
            else:
                self.numSLONotSat += 1
