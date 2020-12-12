from enum import Enum


class ActionType(Enum):
    LOAD = 1
    INFER = 2
    UNLOAD = 3

    # Note that INPUT, EXEC, and OUTPUT actually constitute one action: INFER
    INPUT = 4
    EXEC = 5
    OUTPUT = 6


class Action:
    modelName: str
    reqId: int
    type: ActionType
    earliest: int
    latest: int
    batchKey: str

    def __init__(self, _modelName: str, _reqId: int, _type: ActionType, _earliest: int, _latest: int, _batchKey: str):
        self.modelName = _modelName
        self.reqId = _reqId
        self.type = _type
        self.earliest = _earliest
        self.latest = _latest
        self.batchKey = _batchKey


# TODO: Richer error codes?
class Code(Enum):
    Success = 1
    Error = 2


class Result:
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


class InferenceRequest:
    modelName: str
    batchSize: int
    sloFactor: int

    def __init__(self, _modelName: str, _batchSize: int, _sloFactor: int):
        self.modelName = _modelName
        self.batchSize = _batchSize
        self.sloFactor = _sloFactor



