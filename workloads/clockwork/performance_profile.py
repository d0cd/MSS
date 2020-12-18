from typing import Dict, Tuple, List
from queue import PriorityQueue

# Performance Profile for each worker
# Note:
#   - We leave out ActionProfiles since we assume that our the runtime specification of our models are accurate


class PerformanceProfile:
    # Cache: model name, last inference request
    cache: Dict[str, int]

    pendingLoadActions: PriorityQueue
    pendingInferActions: PriorityQueue
    pendingUnloadActions: PriorityQueue

    def __init__(
            self,
            _cache: Dict[str, int],
            _pendingLoadActions: PriorityQueue,
            _pendingInferActions: PriorityQueue,
            _pendingUnloadActions: PriorityQueue):
        self.cache = _cache
        self.pendingLoadActions = _pendingLoadActions
        self.pendingInferActions = _pendingInferActions
        self.pendingUnloadActions = _pendingUnloadActions
