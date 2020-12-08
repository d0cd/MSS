from typing import Dict, Tuple

from .dag import Dag
from .event_queue import EventQueue
from .resource import ResourcePool

# TODO: Need to adjust this interface after writing a couple of examples
class System:
    """Abstract system implementation. Subclass and customize behavior based on what you'd like."""
    events: EventQueue
    pools: Dict[str, ResourcePool]
    outstanding_requests: Dict[str, Tuple[bool, Dag]]  # The boolean flag indicates whether or not the next function can be scheduled
    time: int

    def __init__(self, _events: EventQueue, _pools: Dict[str, ResourcePool], *args, **kwargs):
        self.events = _events
        self.pools = _pools
        self.outstanding_requests = {}
        self.time = 0

    def schedule(self, curr_time, events, *args, **kwargs):
        raise NotImplementedError("Create a subclass and implement your secheduler in this function.")

    def run(self, *args, **kwargs) -> int:
        while self.events.has_more_events():
            (invocations, absolute_time, elapsed_time) = self.events.get_next_event()
            for _ in range(0, max(0, elapsed_time)):
                self.schedule(self.time, set(), *args, **kwargs)
                self.time += 1
            assert self.time == absolute_time, "The time should have been accurately stepped to current time"
            self.schedule(self.time, invocations, *args, **kwargs)
        while len(self.outstanding_requests) > 0:
            self.time += 1
            self.schedule(self.time, set(), *args, **kwargs)

        return self.time
