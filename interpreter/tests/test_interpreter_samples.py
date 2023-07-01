import io
from pathlib import Path

import pytest

from interpreter.comments_filter import CommentsFilter
from interpreter.error_formatter import ErrorFormatter
from interpreter.error_handler import ErrorHandler
from interpreter.error_handler.error import *
from interpreter.interpreter.interpreter import Interpreter
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.reader import Reader
from interpreter.tests.test_interpreter import Mock


def test_not_callable(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 0; a();"))
    error_handler = ErrorHandler()
    with pytest.raises(NotCallable):
        Mock(error_handler)


def test_not_defined(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a = 0;"))
    error_handler = ErrorHandler()
    with pytest.raises(NotDefined):
        Mock(error_handler)


def test_zero_division(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1 / 0;"))
    error_handler = ErrorHandler()
    with pytest.raises(ZeroDivision):
        Mock(error_handler)


def test_assign_mut(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1; a = 2;"))
    error_handler = ErrorHandler()
    with pytest.raises(AssignMut):
        Mock(error_handler)


def test_already_defined(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1; let mut a = 2;"))
    error_handler = ErrorHandler()
    with pytest.raises(AlreadyDefined):
        Mock(error_handler)


def test_missing_parameter(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"fn a(b,c,d){}  a(1);"))
    error_handler = ErrorHandler()
    with pytest.raises(MissingParameter):
        Mock(error_handler)


def test_unexpected_argument(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"fn a(b){} a(1,1,1);"))
    error_handler = ErrorHandler()
    with pytest.raises(UnexpectedArgument):
        Mock(error_handler)


def test_unexpected_type(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1 or 2;"))
    error_handler = ErrorHandler()
    with pytest.raises(UnexpectedType):
        Mock(error_handler)
