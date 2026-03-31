from enum import Enum

class TokenType(Enum):
    COMMENT = "COMMENT"
    IDENTIFIER = "IDENTIFIER"
    FUNCTION = "FUNCTION"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    NEWLINE = "NEWLINE"

    OPEN_BRACE = "OPEN_BRACE"
    CLOSE_BRACE = "CLOSE_BRACE"

    K_PUSH = "PUSH"
    K_POP = "POP"
    K_BIN_OP = "BIN_OP"
    K_PEEK = "PEEK"
    K_CALL = "CALL"
    K_HALT = "HALT"
    K_EOF = "EOF"
    K_RET = "RET"