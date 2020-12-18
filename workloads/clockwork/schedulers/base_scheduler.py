from ..messages import InferenceResponse, InferenceRequest, Result, Action

from enum import Enum
from typing import Union


class SchedulerType(Enum):
    SIMPLE = 1


class Scheduler:
    def __init__(self):
        raise NotImplementedError("Cannot initialize base scheduler.")

    def on_request(self, req: InferenceRequest) -> Union[InferenceResponse, Action]:
        raise NotImplementedError("Base scheduler cannot handle requests.")

    def on_result(self, result: Result) -> Union[InferenceResponse, Action]:
        raise NotImplementedError("Base scheduler cannot handle results.")