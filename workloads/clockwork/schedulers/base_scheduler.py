from ..messages import InferenceResponse, InferenceRequest, Result, Action

from enum import Enum
from typing import Union, Optional


class SchedulerType(Enum):
    SIMPLE = 1


class Scheduler:
    clock: int

    def __init__(self):
        self.clock = 0

    def step(self):
        self.clock += 1

    def on_request(self, req: InferenceRequest) -> Optional[Union[InferenceResponse, Action]]:
        raise NotImplementedError("Base scheduler cannot handle requests.")

    def on_result(self, result: Result) -> Optional[Union[InferenceResponse, Action]]:
        raise NotImplementedError("Base scheduler cannot handle results.")

    def has_outstanding_requests(self) -> bool:
        raise NotImplementedError("Base scheduler cannot have outstanding requests.")