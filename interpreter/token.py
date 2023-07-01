from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from interpreter.position import Position


class TokenType(Enum):
    BOOL_TYPE = (auto(),)
    NUM_TYPE = (auto(),)
    STR_TYPE = (auto(),)
    DEFAULT = (auto(),)
    NUM = (auto(),)
    STR = (auto(),)
    BOOL = (auto(),)
    NULL_VAL = (auto(),)
    TRUE_VAL = (auto(),)
    FALSE_VAL = (auto(),)

    BREAK = (auto(),)
    CASE = (auto(),)
    CONTINUE = (auto(),)
    ELSE = (auto(),)
    FN = (auto(),)
    IF = (auto(),)
    LET = (auto(),)
    MATCH = (auto(),)
    MUT = (auto(),)
    WHILE = (auto(),)
    RETURN = (auto(),)
    IDENTIFIER = (auto(),)

    AND_OPERATOR = (auto(),)
    OR_OPERATOR = (auto(),)
    NOT_OPERATOR = (auto(),)
    LESS_OPERATOR = (auto(),)
    GREATER_OPERATOR = (auto(),)
    ASSIGNMENT_OPERATOR = (auto(),)
    EQ_OPERATOR = (auto(),)
    NOT_EQ_OPERATOR = (auto(),)
    LESS_OR_EQ_OPERATOR = (auto(),)
    GREATER_OR_EQ_OPERATOR = (auto(),)

    ADDITION_OPERATOR = (auto(),)
    SUBTRACTION_OPERATOR = (auto(),)
    MULTIPLICATION_OPERATOR = (auto(),)
    DIVISION_OPERATOR = (auto(),)
    MODULO_OPERATOR = (auto(),)
    LEFT_BRACKET = (auto(),)
    RIGHT_BRACKET = (auto(),)
    LEFT_CURLY_BRACKET = (auto(),)
    RIGHT_CURLY_BRACKET = (auto(),)
    COLON = (auto(),)
    SEMICOLON = (auto(),)
    COMMA = (auto(),)

    IS_EVEN_OPERATOR = (auto(),)
    IS_ODD_OPERATOR = (auto(),)
    IS_QUARTERO_OPERATOR = (auto(),)
    IS_QUARTERTW_OPERATOR = (auto(),)
    IS_QUARTERTH_OPERATOR = (auto(),)
    IS_QUARTERF_OPERATOR = (auto(),)

    ONE_LINE_COMMENT = (auto(),)
    MULTILINE_COMMENT = (auto(),)

    EOF = (auto(),)


@dataclass
class Token:
    token_type: TokenType
    position: Position
    value: Any = None

    ASSIGN_OPERATORS = [
        TokenType.ASSIGNMENT_OPERATOR,
    ]

    RELATIONAL_OPERATORS = [
        TokenType.LESS_OPERATOR,
        TokenType.LESS_OR_EQ_OPERATOR,
        TokenType.GREATER_OPERATOR,
        TokenType.GREATER_OR_EQ_OPERATOR,
        TokenType.EQ_OPERATOR,
        TokenType.NOT_EQ_OPERATOR,
    ]

    ADDITIVE_OPERATORS = [
        TokenType.ADDITION_OPERATOR,
        TokenType.SUBTRACTION_OPERATOR,
    ]

    MULTIPLICATIVE_OPERATORS = [
        TokenType.MULTIPLICATION_OPERATOR,
        TokenType.DIVISION_OPERATOR,
        TokenType.MODULO_OPERATOR,
    ]

    CASE_OPERATORS = [
        TokenType.IS_EVEN_OPERATOR,
        TokenType.IS_ODD_OPERATOR,
        TokenType.IS_QUARTERO_OPERATOR,
        TokenType.IS_QUARTERTW_OPERATOR,
        TokenType.IS_QUARTERTH_OPERATOR,
        TokenType.IS_QUARTERF_OPERATOR,
    ]

    UNARY_OPERATORS = [
        TokenType.NOT_OPERATOR,
        TokenType.SUBTRACTION_OPERATOR,
    ]

    DATA_TYPES = [
        TokenType.NUM_TYPE,
        TokenType.STR_TYPE,
        TokenType.BOOL_TYPE,
    ]
