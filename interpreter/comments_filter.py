from typing import Optional

from interpreter.lexer import ILexer
from interpreter.token import Token, TokenType


class CommentsFilter(ILexer):
    def __init__(self, lexer: ILexer):
        self._lexer = lexer

    def next_token(self) -> Optional[Token]:
        token = self._lexer.next_token()
        while token.token_type in [
            TokenType.MULTILINE_COMMENT,
            TokenType.ONE_LINE_COMMENT,
        ]:
            token = self._lexer.next_token()
        return token
