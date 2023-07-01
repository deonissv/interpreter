from enum import Enum, auto

from interpreter.token import Token, TokenType


class RelationalOperator(Enum):
    LESS = (auto(),)
    GREATER = (auto(),)
    EQ = (auto(),)
    NOT_EQ = (auto(),)
    LESS_OR_EQ = (auto(),)
    GREATER_OR_EQ = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.LESS_OPERATOR:
                return RelationalOperator.LESS
            case TokenType.GREATER_OPERATOR:
                return RelationalOperator.GREATER
            case TokenType.EQ_OPERATOR:
                return RelationalOperator.EQ
            case TokenType.NOT_EQ_OPERATOR:
                return RelationalOperator.NOT_EQ
            case TokenType.LESS_OR_EQ_OPERATOR:
                return RelationalOperator.LESS_OR_EQ
            case TokenType.GREATER_OR_EQ_OPERATOR:
                return RelationalOperator.GREATER_OR_EQ


class AdditiveOperator(Enum):
    ADDITION = (auto(),)
    SUBTRACTION = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.ADDITION_OPERATOR:
                return AdditiveOperator.ADDITION
            case TokenType.SUBTRACTION_OPERATOR:
                return AdditiveOperator.SUBTRACTION


class MultiplicativeOperator(Enum):
    MULTIPLICATION = (auto(),)
    DIVISION = (auto(),)
    MODULO = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.MULTIPLICATION_OPERATOR:
                return MultiplicativeOperator.MULTIPLICATION
            case TokenType.DIVISION_OPERATOR:
                return MultiplicativeOperator.DIVISION
            case TokenType.MODULO_OPERATOR:
                return MultiplicativeOperator.MODULO


class UnaryOperator(Enum):
    NEGATION = (auto(),)
    MINUS = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.SUBTRACTION_OPERATOR:
                return UnaryOperator.MINUS
            case TokenType.NOT_OPERATOR:
                return UnaryOperator.NEGATION


class CaseOperator(Enum):
    IS_EVEN = (auto(),)
    IS_ODD = (auto(),)
    IS_QUARTERO = (auto(),)
    IS_QUARTERTW = (auto(),)
    IS_QUARTERTH = (auto(),)
    IS_QUARTERF = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.IS_EVEN_OPERATOR:
                return CaseOperator.IS_EVEN
            case TokenType.IS_ODD_OPERATOR:
                return CaseOperator.IS_ODD
            case TokenType.IS_QUARTERO_OPERATOR:
                return CaseOperator.IS_QUARTERO
            case TokenType.IS_QUARTERTW_OPERATOR:
                return CaseOperator.IS_QUARTERTW
            case TokenType.IS_QUARTERTH_OPERATOR:
                return CaseOperator.IS_QUARTERTH
            case TokenType.IS_QUARTERF_OPERATOR:
                return CaseOperator.IS_QUARTERF
