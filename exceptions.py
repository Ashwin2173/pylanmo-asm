from lang.lexer.word import Word

class LanmoError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class LanmoSyntaxError(Exception):
    def __init__(self, token: Word | None, message: str):
        super().__init__(message)
        self.token = token

class LanmoDisAsmError(Exception):
    def __init__(self, *args):
        super().__init__(*args)