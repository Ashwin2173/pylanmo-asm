from enum import Enum, auto

class OpCodeType(Enum):
    PUSH = auto()
    POP = auto()
    BIN_OP = auto()
    PEEK = auto()
    CALL = auto()
    HALT = auto()
    RET = auto()