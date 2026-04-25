from lang.lexer.tokenizer import tokenize
from lang.parser.compiler import Compiler
from exceptions import LanmoSyntaxError

class Assembler:
    def __init__(self, program, path):
        self.program = program
        self.path = path

    def assemble(self) -> None:
        tokens = tokenize(self.program)
        byte_code_file = f"{self.path[:-5]}.lmc"
        with open(byte_code_file, 'wb') as byte_code_file:
            try:
                compiler = Compiler(tokens)
                byte_code_file.write(compiler.compile())
            except LanmoSyntaxError as e:
                print(f"In file: {self.path}")
                if e.token is not None:
                    print(self.get_error_token_format(e))
                print(f"SyntaxError: {e}")

    def get_error_token_format(self, e: LanmoSyntaxError) -> str:
        line = e.token.get_line() - 1
        raw = e.token.get_raw()
        program_lines = self.program.splitlines()
        raw_line = program_lines[line]
        size = len(e.token.get_raw())
        previous_line = "" if line <= 0 else program_lines[line - 1]
        prefix = f"  > {line + 1}: "
        previous_line = f"    {line}: " + previous_line if len(previous_line) != 0 else ""
        return f"{previous_line}\n{prefix}{raw_line}\n{' ' * (len(prefix) + raw_line.find(raw))}{'^' * size}"
