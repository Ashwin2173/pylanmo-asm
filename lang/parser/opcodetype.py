from enum import Enum, auto

class OpCodeType(Enum):
    PUSH          = auto()
    POP           = auto()
    BIN_OP        = auto()
    WRITE         = auto()
    CALL          = auto()
    HALT          = auto()
    RET           = auto()
    JUMP          = auto()
    JUMP_IF_FALSE = auto()