from lang.lexer.tokentype import TokenType

class Constants:
    MAGIC = 2273
    MAJOR_VERSION = 1
    MINOR_VERSION = 0

    STRING_LEN_FORMAT = lambda word:f"<I{len(word)}s"

    SINGLE_OPCODES = {
        TokenType.K_WRITE,
        TokenType.K_POP,
        TokenType.K_HALT,
        TokenType.K_RET
    }

    OP_CODE_KEYWORDS = {
        TokenType.K_PUSH,
        TokenType.K_POP,
        TokenType.K_BIN_OP,
        TokenType.K_WRITE,
        TokenType.K_CALL,
        TokenType.K_HALT,
        TokenType.K_RET,
        TokenType.K_JUMP,
        TokenType.K_JUMP_IF_FALSE
    }