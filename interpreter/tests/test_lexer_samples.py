import io
from pathlib import Path
from typing import List

from interpreter.error_handler import ErrorHandler
from interpreter.lexer import Lexer
from interpreter.reader import Reader
from interpreter.token import TokenType, Token

sample_fn = [
    TokenType.FN,
    TokenType.IDENTIFIER,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.RIGHT_BRACKET,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.IF,
    TokenType.IDENTIFIER,
    TokenType.LESS_OPERATOR,
    TokenType.NUM,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.RETURN,
    TokenType.NULL_VAL,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.IF,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.EQ_OPERATOR,
    TokenType.NUM,
    TokenType.OR_OPERATOR,
    TokenType.IDENTIFIER,
    TokenType.EQ_OPERATOR,
    TokenType.NUM,
    TokenType.RIGHT_BRACKET,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.RETURN,
    TokenType.NUM,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.RETURN,
    TokenType.IDENTIFIER,
    TokenType.MULTIPLICATION_OPERATOR,
    TokenType.IDENTIFIER,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.SUBTRACTION_OPERATOR,
    TokenType.NUM,
    TokenType.RIGHT_BRACKET,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.EOF,
]

sample_match = [
    TokenType.LET,
    TokenType.IDENTIFIER,
    TokenType.ASSIGNMENT_OPERATOR,
    TokenType.NUM,
    TokenType.SEMICOLON,
    TokenType.MATCH,
    TokenType.IDENTIFIER,
    TokenType.COLON,
    TokenType.ONE_LINE_COMMENT,
    TokenType.CASE,
    TokenType.IS_EVEN_OPERATOR,
    TokenType.COLON,
    TokenType.LEFT_BRACKET,
    TokenType.RIGHT_BRACKET,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.ADDITION_OPERATOR,
    TokenType.STR,
    TokenType.RIGHT_BRACKET,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.MULTILINE_COMMENT,
    TokenType.CASE,
    TokenType.IS_ODD_OPERATOR,
    TokenType.COLON,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.RIGHT_BRACKET,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.ADDITION_OPERATOR,
    TokenType.STR,
    TokenType.RIGHT_BRACKET,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.DEFAULT,
    TokenType.COLON,
    TokenType.LEFT_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.RIGHT_BRACKET,
    TokenType.LEFT_CURLY_BRACKET,
    TokenType.IDENTIFIER,
    TokenType.LEFT_BRACKET,
    TokenType.STR,
    TokenType.RIGHT_BRACKET,
    TokenType.SEMICOLON,
    TokenType.RIGHT_CURLY_BRACKET,
    TokenType.EOF,
]


def read_sample() -> List[Token]:
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        t = lexer.next_token()
        tokens = [t]
        while tokens[-1].token_type != TokenType.EOF:
            tokens.append(lexer.next_token())
        return tokens


def test_sample_fn(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"fn factorial(n) { if n < 0 { return null; } if (n == 0 or n == 1) { return 1; } return n * factorial(n - 1); }"
        ),
    )
    tokens = read_sample()
    assert [t.token_type for t in tokens] == sample_fn


def test_sample_match_cr(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b'let x = 1; match x: // check if even \n case isEven: () { print(x + "is even"); } /* check if odd */ case isOdd: (x) { print(x + "is odd"); } default: (x) { print(\'wow\'); }'
        ),
    )
    tokens = read_sample()
    assert [t.token_type for t in tokens] == sample_match
