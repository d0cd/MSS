from typing import Dict, Tuple

from .dag import Dag
from .event_queue import EventQueue
from .resource import ResourcePool

# TODO: Need to adjust this interface after writing a couple of examples
class System:
    """Abstract system implementation. Subclass and customize behavior based on what you'd like."""
    events: EventQueue
    outstanding_requests: Dict[str, Tuple[bool, Dag]]  # The boolean flag indicates whether or not the next function can be scheduled
    clock: int

    def __init__(self, _events: EventQueue, *args, **kwargs):
        self.events = _events
        self.outstanding_requests = {}
        self.clock = 0

    def schedule(self, curr_time, events, *args, **kwargs):
        raise NotImplementedError("Create a subclass and implement your secheduler in this function.")

    def run(self, *args, **kwargs) -> int:
        print("Running system...")
        while self.events.has_more_events():
            (invocations, absolute_time, _) = self.events.get_next_event()
            assert self.clock <= absolute_time
            while self.clock < absolute_time:
                self.schedule(self.clock, set(), *args, **kwargs)
                self.clock += 1
            assert self.clock == absolute_time, "The time should have been accurately stepped to current time"
            self.schedule(self.clock, invocations, *args, **kwargs)
        while len(self.outstanding_requests) > 0:
            self.clock += 1
            self.schedule(self.clock, set(), *args, **kwargs)

        return self.clock
