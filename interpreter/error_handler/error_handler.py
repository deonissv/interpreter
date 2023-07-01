from typing import List

from interpreter.error_handler.error import (
    Error,
    ErrorType,
    OperationBadTypes,
    ZeroDivision,
    NotDefined,
    AssignMut,
    UnexpectedType,
    AlreadyDefined,
    NotCallable,
    MissingParameter,
    UnexpectedArgument,
)
from interpreter.interpreter.value import DataType
from interpreter.position import Position


class ErrorHandler:
    def __init__(self):
        self._errors: List[Error] = []

    @property
    def errors(self) -> List[Error]:
        return self._errors

    def __getitem__(self, item) -> Error:
        return self.errors[item]

    def unexpected_end_of_text(self, position: Position):
        msg = "SyntaxError: unexpected EOF while parsing"
        self._errors.append(Error(ErrorType.UNEXPECTED_END_OF_TEXT, msg, position))

    def num_overflow_error(self, position: Position):
        msg = "NumberOverFlowError: provided value cannot be handled"
        self._errors.append(Error(ErrorType.NUM_OVERFLOW_ERROR, msg, position))

    def leading_zero(self, position: Position):
        msg = "SyntaxError: leading zeros in decimal integer literals are not permitted"
        self._errors.append(Error(ErrorType.LEADING_ZERO, msg, position))

    def variable_name_expected(self, position: Position) -> None:
        msg = "Error: Variable name expected"
        self._errors.append(Error(ErrorType.VARIABLE_NAME_EXPECTED, msg, position))

    def assignment_operator_expected(self, position: Position) -> None:
        msg = "Error: Assignment operator expected"
        self._errors.append(
            Error(ErrorType.ASSIGNMENT_OPERATOR_EXPECTED, msg, position)
        )

    def semicolon_expected(self, position: Position):
        msg = 'Error: ";" expected'
        self._errors.append(Error(ErrorType.SEMICOLON_EXPECTED, msg, position))

    def expression_expected(self, position: Position):
        msg = "Error: Expression expected"
        self._errors.append(Error(ErrorType.EXPRESSION_EXPECTED, msg, position))

    def code_block_expected(self, position: Position):
        msg = "Error: Code block expected"
        self._errors.append(Error(ErrorType.CODE_BLOCK_EXPECTED, msg, position))

    def colon_expected(self, position: Position):
        msg = 'Error: ":" expected'
        self._errors.append(Error(ErrorType.COLON_EXPECTED, msg, position))

    def identifier_expected(self, position: Position):
        msg = "Error: Identifier expected"
        self._errors.append(Error(ErrorType.IDENTIFIER_EXPECTED, msg, position))

    def left_bracket_expected(self, position: Position):
        msg = 'Error: "(" expected'
        self._errors.append(Error(ErrorType.LEFT_BRACKET_EXPECTED, msg, position))

    def right_bracket_expected(self, position: Position):
        msg = 'Error: ")" expected'
        self._errors.append(Error(ErrorType.RIGHT_BRACKET_EXPECTED, msg, position))

    def right_curly_bracket_expected(self, position: Position):
        msg = 'Error: "{" expected'
        self._errors.append(
            Error(ErrorType.RIGHT_CURLY_BRACKET_EXPECTED, msg, position)
        )

    def default_statement_expected(self, position: Position):
        msg = "default statement expected"
        self._errors.append(Error(ErrorType.DEFAULT_STATEMENT_EXPECTED, msg, position))

    def no_effect(self, position: Position):
        msg = "statement seems to have no effect"
        self._errors.append(Error(ErrorType.NO_EFFECT, msg, position))

    @staticmethod
    def operation_bad_types(position: Position):
        msg = "not supported between types"
        raise OperationBadTypes(position, msg)

    @staticmethod
    def zero_division(position: Position):
        msg = f"attempt to divide by zero"
        raise ZeroDivision(position, msg)

    @staticmethod
    def not_defined(position: Position, name: str):
        msg = f"{name} is not defined"
        raise NotDefined(position, msg)

    @staticmethod
    def not_callable(position: Position, name: str):
        msg = f"{name} is not callable"
        raise NotCallable(position, msg)

    @staticmethod
    def missing_parameter(position: Position, name: str):
        msg = f"missing parameter {name}"
        raise MissingParameter(position, msg)

    @staticmethod
    def unexpected_argument(position: Position):
        msg = f"unexpected argument"
        raise UnexpectedArgument(position, msg)

    @staticmethod
    def assign_mut(position: Position, name: str):
        msg = f"attempt to assign to immutable variable {name}"
        raise AssignMut(position, msg)

    @staticmethod
    def unexpected_type(position: Position, expected: DataType, found: DataType):
        msg = f"unexpected type: expected {expected} but found {found}"
        raise UnexpectedType(position, msg)

    @staticmethod
    def already_defined(position: Position, name: str):
        msg = f"attempt to redefine variable {name}"
        raise AlreadyDefined(position, msg)

    @staticmethod
    def max_recursion_depth(position: Position):
        msg = f"reached maximum recursion depth"
        raise AlreadyDefined(position, msg)
