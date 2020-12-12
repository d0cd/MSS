from enum import Enum
from typing import Tuple

class ActionType(Enum):
    LOAD = 1
    INFER = 2
    UNLOAD = 3

    # Note that INPUT, EXEC, and OUTPUT actually constitute one action: INFER
    INPUT = 4
    EXEC = 5
    OUTPUT = 6

class Action:
    id: Tuple[int, str]  # request ID, model name
    type: ActionType
    earliest: int
    latest: int
    batchKey: str

    def __init__(self, _id: Tuple[int, str], _type: ActionType, _earliest: int, _latest: int, _batchKey: str):
        self.id = _id
        self.type = _type
        self.earliest = _earliest
        self.latest = _latest
        self.batchKey = _batchKey

