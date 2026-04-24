from enum import Enum, auto

class OpCodeType(Enum):
    PUSH          = auto()
    POP           = auto()
    BIN_OP        = auto()
    WRITE         = auto()
    CALL          = auto()
    HALT          = auto()
    RETURN        = auto()
    JUMP          = auto()
    JUMP_IF_FALSE = auto()
    DUP           = auto()
    STORE         = auto()
    LOAD          = auto()