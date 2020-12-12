from collections import deque
from copy import deepcopy
from itertools import groupby
from typing import Deque, List, Tuple, Optional, Set, Any

from .dag import Dag


class EventQueue:
    """A sequence of events waiting to be processed."""
    _queue: Deque

    # TODO: This is definitely not efficient
    def __init__(self, dags: List[Tuple[Dag, List[Tuple[int, Any]]]]):
        """Initialize an event queue from a list of DAGs, invocation times/inputs"""
        self._queue = deque()

        # Add all dags to a big array
        # TODO: This appears to be a bottleneck
        print("Collecting all invocations...")
        all_invocations = []
        for (dag, invoc_input) in dags:
            for (t, input) in invoc_input:
                all_invocations.append((t, deepcopy(dag), input))

        # Sort, process, and add elements to queue
        print("Sorting invocations...")
        sorted_invocations = sorted(all_invocations, key=lambda t: t[0])
        last_time = 0  # 0ms
        print("Grouping invocations...")
        for time, group in groupby(sorted_invocations, lambda t: t[0]):
            events = set(map(lambda t: (t[1], t[2]), group))
            self._queue.append((events, time, time - last_time))

    def get_next_event(self) -> Optional[Tuple[Set, int, int]]:
        """
        Get next event in the sequence.
        Returns a set of DAGs for invocation, the absolute time, and time since last event.
        Note that time is always in milliseconds.
        """
        if self.has_more_events():
            return self._queue.popleft()
        else:
            return None

    def peek(self) -> Optional[Tuple[Set, int, int]]:
        if self.has_more_events():
            first = self._queue.popleft()
            self._queue.appendleft(first)
            return first
        else:
            return None

    def has_more_events(self) -> bool:
        """Check for any events left."""
        return len(self._queue) > 0
