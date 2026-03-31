TOKEN_GRAMMER = r"""
(?P<COMMENT>//[^\n]*)                                     # single-line comment
| (?P<K_PUSH>PUSH)                                        # push keyword
| (?P<K_POP>POP)                                          # pop keyword
| (?P<K_BIN_OP>BIN_OP)                                    # binary operation keyword
| (?P<K_PEEK>PEEK)                                        # peek keyword
| (?P<K_CALL>CALL)                                        # call keyword
| (?P<K_HALT>HALT)                                        # halt keyword
| (?P<K_EOF>EOF)                                          # eof keyword
| (?P<K_RET>RET)                                          # return keyword
| (?P<OPEN_BRACE>\{)                                      # open brace operator
| (?P<CLOSE_BRACE>\})                                     # close brace operator
| (?P<IDENTIFIER>[A-Za-z_]\w*)                            # identifiers and keywords
| (?P<FLOAT>\d+\.\d+)                                     # float numbers
| (?P<INTEGER>\d+)                                        # integer numbers
| (?P<STRING>"(?:\\.|[^"\\])*")                           # double-quoted strings with escape support
| (?P<NEWLINE>\n)                                         # new line
"""