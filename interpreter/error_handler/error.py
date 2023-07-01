from enum import Enum, auto

from dataclasses import dataclass

from interpreter.position import Position


class ErrorType(Enum):
    UNEXPECTED_END_OF_TEXT = (auto(),)
    NUM_OVERFLOW_ERROR = (auto(),)
    LEADING_ZERO = (auto(),)
    VARIABLE_NAME_EXPECTED = (auto(),)
    ASSIGNMENT_OPERATOR_EXPECTED = (auto(),)
    SEMICOLON_EXPECTED = (auto(),)
    EXPRESSION_EXPECTED = (auto(),)
    CODE_BLOCK_EXPECTED = (auto(),)
    COLON_EXPECTED = (auto(),)
    IDENTIFIER_EXPECTED = (auto(),)
    LEFT_BRACKET_EXPECTED = (auto(),)
    RIGHT_BRACKET_EXPECTED = (auto(),)
    RIGHT_CURLY_BRACKET_EXPECTED = (auto(),)
    DEFAULT_STATEMENT_EXPECTED = (auto(),)
    NO_EFFECT = (auto(),)
    OPERATION_BAD_TYPES = (auto(),)
    ZERO_DIVISION = (auto(),)
    NOT_DEFINED = (auto(),)
    NOT_CALLABLE = (auto(),)
    MISSING_PARAMETER = (auto(),)
    UNEXPECTED_ARGUMENT = (auto(),)
    ASSIGN_MUT = (auto(),)
    UNEXPECTED_TYPE = (auto(),)
    ALREADY_DEFINED = (auto(),)


@dataclass
class Error:
    type: ErrorType
    msg: str
    position: Position


@dataclass
class CriticalError(Exception):
    position: Position
    msg: str


class OperationBadTypes(CriticalError):
    ...


class ZeroDivision(CriticalError):
    ...


class NotDefined(CriticalError):
    ...


class NotCallable(CriticalError):
    ...


class MissingParameter(CriticalError):
    ...


class UnexpectedArgument(CriticalError):
    ...


class AssignMut(CriticalError):
    ...


class UnexpectedType(CriticalError):
    ...


class AlreadyDefined(CriticalError):
    ...


class RecusionDepth(CriticalError):
    ...
