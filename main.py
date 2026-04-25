import sys

from lang.parser.constants import Constants
from lang.asm.assembler import Assembler
from lang.dis.disasm import Disasm

program_args = set()

def read_program_file(args: list[str]) -> tuple[str, str]:
    ret_value = None, None
    for arg in args:
        if arg.endswith(".lasm"):
            if ret_value[0] is not None:
                print("[Error] Passed multiple files")
                exit(1)
            ret_value = open(arg, 'r').read(), arg
        elif arg.endswith(".lmc"):
            if ret_value[0] is not None:
                print("[Error] Passed multiple files")
                exit(1)
            ret_value = open(arg, 'rb').read(), arg
        elif arg.startswith("--"):
            program_args.add(arg)
    return ret_value

def main(args: list[str]) -> None:
    program, path = read_program_file(args)
    if "--version" in program_args:
        version = f"{Constants.MAJOR_VERSION}.{Constants.MINOR_VERSION}"
        print(f"LANMO v{version}; Written in python")
        sys.exit(0)
    elif program is None or "--help" in program_args:
        print("USAGE:")
        print("    lasm [OPTIONS] [PROGRAM_PATH]")
        print("PROGRAM_PATH:   <lasm_file>.lasm")
        print("OPTIONS:")
        print("    --dis       Disasmble bytecode to program")
        print("    --help      Prints this usage")
        print("    --version   prints the version")
        sys.exit(0)
    elif "--dis" in program_args:
        if not path.endswith("lmc"):
            print("[ERROR] Required .lmc file for disasmbling")
            sys.exit(1)
        with open(f"{path[:-4]}.dis.lasm", 'w') as new_file_path:
            disasmbler = Disasm(program, new_file_path)
            disasmbler.render()
        sys.exit(0)
    else:
        if not path.endswith("lasm"):
            print("[ERROR] Required .lasm file for compiling")
            exit(1)
        asmbler = Assembler(program, path)
        asmbler.assemble()
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)