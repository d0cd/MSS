from enum import Enum


class Message:
    def __init__(self):
        raise NotImplementedError("Message cannot be instantiated")


class ActionType(Enum):
    LOAD = 1
    INFER = 2
    UNLOAD = 3

    # Note that INPUT, EXEC, and OUTPUT actually constitute one action: INFER
    INPUT = 4
    EXEC = 5
    OUTPUT = 6


class Action(Message):
    workerId: int
    modelName: str
    reqId: int
    type: ActionType
    earliest: int
    latest: int
    received: int
    batchKey: str

    def __init__(self, _workerId: int, _modelName: str, _reqId: int, _type: ActionType, _earliest: int, _latest: int, _batchKey: str):
        self.workerId = _workerId
        self.modelName = _modelName
        self.reqId = _reqId
        self.type = _type
        self.earliest = _earliest
        self.latest = _latest
        self.received = -1
        self.batchKey = _batchKey


# TODO: Richer error codes?
class Code(Enum):
    Success = 1
    Error = 2
    CannotMeetSLO = 3


class Executor(Enum):
    Load = 1
    Infer = 2
    Unload = 3


class Result(Message):
    code: Code
    action: Action
    actionReceived: int
    resultSent: int
    message: str

    def __init__(self, _code: Code, _action: Action, _recv: int, _sent: int, _msg: str):
        self.code = _code
        self.action = _action
        self.actionReceived = _recv
        self.resultSent = _sent
        self.message = _msg


class InferenceRequest(Message):
    modelName: str
    batchSize: int
    sloFactor: int
    uniqueId: int
    arrived: int

    def __init__(self, _modelName: str, _batchSize: int, _sloFactor: int, _uniqueId: int):
        self.modelName = _modelName
        self.batchSize = _batchSize
        self.sloFactor = _sloFactor
        self.uniqueId = _uniqueId
        self.arrived = 0

    def set_arrival_time(self, time: int):
        self.arrived = time


class InferenceResponse(Message):
    modelName: str
    batchSize: int
    sloFactor: int
    uniqueId: int
    arrived: int
    code: Code
    completed: int

    def __init__(self, _modelName: str, _batchSize: int, _sloFactor: int, _uniqueId: int, _arrived: int, _code: Code, _completed: int):
        self.modelName = _modelName
        self.batchSize = _batchSize
        self.sloFactor = _sloFactor
        self.uniqueId = _uniqueId
        self.arrived = _arrived
        self.code = _code
        self.completed = _completed

