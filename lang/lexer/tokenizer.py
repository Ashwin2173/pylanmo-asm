import re

from lang.lexer.word import Word
from lang.lexer.tokentype import TokenType
from lang.lexer.grammar import TOKEN_GRAMMER

def tokenize(program) -> list[Word]:
    line = 1
    tokens: list[Word] = list()
    compiled_grammar = re.compile(TOKEN_GRAMMER, re.VERBOSE)
    for item in compiled_grammar.finditer(program):
        token_type = TokenType[item.lastgroup]
        if token_type == TokenType.NEWLINE:
            line += 1
        elif token_type == TokenType.COMMENT:
            continue
        else:
            raw = item.group()
            token_span = (item.start(), item.end())
            tokens.append(Word(raw, token_type, line, token_span))
            
    tokens.append(Word('EOF', TokenType.K_EOF, line, ()))
    return tokens
