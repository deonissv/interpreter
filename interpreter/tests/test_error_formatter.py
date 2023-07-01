import io

from interpreter.error_formatter import ErrorFormatter
from interpreter.error_handler import ErrorType, Error
from interpreter.program.statement import *
from interpreter.reader.reader import Reader


def test__get_error_msg(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a\nb\nc\nd\n"))
    with Reader("path") as reader:
        list(reader)
        error_handler = ErrorFormatter(reader)
        error_msg = "msg\n"
        error_msg += "   |\n"
        error_msg += " 3 | c\n"
        error_msg += "   |^^^\n"
        assert (
            error_handler.get_error_msg(
                Error(ErrorType.NUM_OVERFLOW_ERROR, "msg", Position(4, 3, 1))
            )
            == error_msg
        )
