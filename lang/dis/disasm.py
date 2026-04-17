from typing import TextIO

from lang.parser.constants import Constants
from lang.parser.datatype import DataType
from lang.parser.opcodetype import OpCodeType
from lang.dis.byte_dispenser import ByteDispenser

from exceptions import LanmoDisAsmError

OP_WITH_LOOKUP = {
    OpCodeType.PUSH
}
OP_WITH_VALUE = {
    OpCodeType.CALL,
    OpCodeType.JUMP,
    OpCodeType.JUMP_IF_FALSE,
    OpCodeType.BIN_OP
}

class Disasm:
    def __init__(self, program: bytes, fp: TextIO):
        self.bd = ByteDispenser(program)
        self.fp = fp
        self.symbol_table   = list()
        self.function_table = list()
        self.__disassemble()

    def render(self) -> str:
        self.fp.write(f"// LANMO v{Constants.MAJOR_VERSION}.{Constants.MINOR_VERSION}\n")
        for function in self.function_table:
            name       = function[0]
            op_codes   = function[1]
            self.fp.write(f"\n{name} {{\n")
            for op_code in op_codes:
                self.fp.write(f"\t{op_code}\n")
            self.fp.write(f"}}\n")

    def __disassemble(self) -> None:
        magic = self.bd.next_int(4)
        major_version = self.bd.next_int(2)
        minor_version = self.bd.next_int(2)
        if magic != Constants.MAGIC:
            raise LanmoDisAsmError("Wrong Magic")
        if major_version != Constants.MAJOR_VERSION or minor_version != Constants.MINOR_VERSION:
            raise LanmoDisAsmError(f"Version v{major_version}.{minor_version} is not supported")
        self.__read_symbols()
        self.__read_functions()

    def __read_symbols(self) -> None:
        symbols_count = self.bd.next_int(2)
        for _ in range(symbols_count):
            symbol_type = self.bd.next_int(1)
            if symbol_type == DataType.INTEGER.value:
                size = self.bd.next_int(4)
                self.symbol_table.append(self.bd.next_int(size))
            elif symbol_type == DataType.STRING.value:
                size = self.bd.next_int(4)
                final_string = stringify(self.bd.next_str(size))
                self.symbol_table.append(final_string)
            elif symbol_type == DataType.IDENTIFIER.value:
                size = self.bd.next_int(4)
                self.symbol_table.append(self.bd.next_str(size))
            elif symbol_type == DataType.FUNCTION.value:
                size = self.bd.next_int(4)
                self.symbol_table.append(self.bd.next_str(size))
            elif symbol_type == DataType.BOOLEAN.value:
                size = self.bd.next_int(1)
                self.symbol_table.append("TRUE" if self.bd.next_int(size) else "FALSE")
            else:
                assert False, f"Unhandled DataType: { str(symbol_type) }"

    def __read_functions(self) -> None:
        function_count = self.bd.next_int(2)
        for _ in range(function_count):
            name = self.symbol_table[self.bd.next_int(2)]
            print(f"[INFO] Disasmbling { name } function")
            _ = self.bd.next(4)     # will be used later
            _ = self.bd.next(2)     # will be used later
            raw_op_code = self.__read_op_codes()
            self.function_table.append((name, raw_op_code))

    def __read_op_codes(self) -> list[str]:
        content = list()
        op_code_count = self.bd.next_int(4)
        for _ in range(op_code_count):
            op_code = OpCodeType(self.bd.next_int(1))
            data    = self.bd.next_int(2)
            if op_code in OP_WITH_LOOKUP:
                lookup_data = self.symbol_table[data]
                content.append(f"{op_code.name} {lookup_data}")
            elif op_code in OP_WITH_VALUE:
                content.append(f"{op_code.name} {data}")
            else:
                content.append(f"{op_code.name}")
        return content
    
def stringify(content: str) -> str:
    return f'"{content}"'

