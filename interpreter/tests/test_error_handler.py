import io
from pathlib import Path

from interpreter.reader.reader import Reader
from interpreter.position import Position
from interpreter.error_handler.error_handler import ErrorHandler
from interpreter.error_handler.error import ErrorType


def test_leading_zero(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 001;"))

    with Reader("path") as reader:
        list(reader)
        error_handler = ErrorHandler()
        pos = Position(10, 1, 11)
        error_handler.leading_zero(pos)

        assert isinstance(error_handler.errors, list)
        assert error_handler[0].type == ErrorType.LEADING_ZERO
        assert error_handler[0].position == Position(10, 1, 11)
