import struct

from lang.lexer.word import Word
from lang.lexer.tokentype import TokenType
from lang.parser.opcodetype import OpCodeType
from lang.parser.datatype import DataType
from lang.parser.constants import Constants
from exceptions import LanmoSyntaxError

SINGLE_OPCODES = {
    TokenType.K_ADD,
    TokenType.K_PEEK,
    TokenType.K_POP,
    TokenType.K_HALT,
    TokenType.K_RET
}

class Compiler:
    def __init__(self, tokens: list[Word]):
        self.tokens = tokens_iter(tokens)
        self.constant_table = bytearray()
        self.function_table = bytearray()
        self.constant_lookup = dict()
        self.function_lookup = set()
        self.function_count = 0

    def compile(self) -> bytearray:
        try:
            for token in self.tokens:
                if token.get_type() == TokenType.K_EOF:
                    break
                elif token.get_type() == TokenType.IDENTIFIER:
                    self.__parse_function(token)
                else:
                    raise LanmoSyntaxError(token, "Unknown token out of function")
        except StopIteration:
            raise LanmoSyntaxError(None, "Missing <EOF>")
        return self.__pack_byte_code()

    def __parse_function(self, token: Word) -> None:
        if token.get_raw() in self.function_lookup:
            raise LanmoSyntaxError(token, "function re-defined")
        self.function_count += 1
        self.function_lookup.add(token.get_raw())
        name_index = self.__add_constant(token)
        function_code = bytearray()
        op_code_count = 0
        max_stack_size = 255
        args_count = next(self.tokens)
        expect_token(args_count, TokenType.INTEGER)
        expect_token(next(self.tokens), TokenType.OPEN_BRACE)
        for token in self.tokens:
            token_type = token.get_type()
            if token_type == TokenType.CLOSE_BRACE: 
                break
            elif token_type == TokenType.K_PUSH:
                self.__parse_push(token, function_code)
            elif token_type == TokenType.K_CALL:
                self.__parse_call(token, function_code)
            elif token_type in SINGLE_OPCODES:
                function_code += struct.pack("<BH", get_opcode(token), 0)
            else:
                raise LanmoSyntaxError(token, "Unknown token or Unhandled opCode")
            op_code_count += 1
        function = bytearray()
        function += struct.pack("<H", name_index)
        function += struct.pack("<B", int(args_count.get_raw()))
        function += struct.pack("<I", 0)     # local count 
        function += struct.pack("<H", max_stack_size)
        function += struct.pack("<I", op_code_count)
        function += function_code
        self.function_table += function
    
    def __parse_call(self, token: Word, excution_code: bytearray) -> None:
        value: Word = next(self.tokens)
        expect_token(value, TokenType.INTEGER)
        count = int(value.get_raw())
        if count >= 256:
            raise LanmoSyntaxError("call size should be <= 255")
        excution_code += struct.pack("<BH", get_opcode(token), count)
    
    def __parse_push(self, token: Word, execution_code: bytearray) -> None:
        value: Word = next(self.tokens)
        index = self.__add_constant(value)
        execution_code += struct.pack("<BH", get_opcode(token), index)

    def __add_constant(self, token: Word) -> int:
        raw_value = token.get_raw()
        if raw_value not in self.constant_lookup:
            self.constant_lookup[raw_value] = len(self.constant_lookup)
            if token.get_type() == TokenType.INTEGER:
                self.constant_table += struct.pack("<BIi", DataType.INTEGER.value, 4, int(raw_value))
            elif token.get_type() == TokenType.IDENTIFIER:
                word = token.get_raw()
                self.constant_table += struct.pack("<B", DataType.IDENTIFIER.value)
                self.constant_table += struct.pack(Constants.STRING_LEN_FORMAT(word), len(word), word.encode('utf-8'))
            elif token.get_type() == TokenType.STRING:
                string_value = token.get_raw()[1:-1]
                self.constant_table += struct.pack("<B", DataType.STRING.value)
                self.constant_table += struct.pack(Constants.STRING_LEN_FORMAT(string_value), len(string_value), string_value.encode('utf-8'))
            else:
                raise LanmoSyntaxError(token, f"Expected CONSTANT; got {token.get_type().value}")
        return self.constant_lookup.get(raw_value)

    def __pack_byte_code(self) -> bytearray:
        if (len(self.constant_lookup) >= 65534):
            raise LanmoSyntaxError(None, "the file contains too many symbols")
        final_byte_code = bytearray()
        final_byte_code += get_header()
        final_byte_code += struct.pack("<H", len(self.constant_lookup))
        final_byte_code += self.constant_table
        final_byte_code += struct.pack("<H", self.function_count)
        final_byte_code += self.function_table
        return final_byte_code

def get_opcode(token: Word) -> int:
    return OpCodeType[token.get_raw()].value

def expect_token(token: Word, token_type: TokenType) -> None:
    if token.get_type() != token_type:
        raise LanmoSyntaxError(token, f"Expected {token_type.name}, but got {token.get_type().value}")

def tokens_iter(tokens: list[Word]):
    for token in tokens:
        yield token

def get_header() -> bytearray:
    return struct.pack("<IHH", Constants.MAGIC, Constants.MAJOR_VERSION, Constants.MINOR_VERSION)
