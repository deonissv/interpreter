import io
from collections.abc import Iterable

from interpreter.program.statement import *
from interpreter.reader.reader import Reader


def test__is_new_line_lf_no_symbol(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\n"))
    with Reader("path") as reader:
        reader._find_new_line_symbol(b"\n")
        assert reader.newline_symbol == b"\n"


def test__is_new_line_lf(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\n"))
    with Reader("path") as reader:
        reader._newline_symbol = b"\n"
        assert reader.get_char() == "\n"


def test__is_new_line_cr_no_symbol(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\r"))
    with Reader("path") as reader:
        reader._find_new_line_symbol(b"\r")
        assert reader.newline_symbol == b"\r"


def test__is_new_line_cr(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\r"))
    with Reader("path") as reader:
        reader._newline_symbol = b"\r"
        assert reader.get_char() == "\n"


def test__is_new_line_crlf_no_symbol(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\r\n"))
    with Reader("path") as reader:
        reader._file_handler.read(1)
        reader._find_new_line_symbol(b"\r")
        assert reader.newline_symbol == b"\r\n"


def test__is_new_line_crlf(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\r\n"))
    with Reader("path") as reader:
        assert reader.get_char() == "\n"


def test__is_new_line_graph_char(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"cd"))
    with Reader("path") as reader:
        assert reader.get_char() == "c"
        assert reader.get_char() == "d"


def test_get_char_lf(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"x\nlet"))
    with Reader("path") as reader:
        assert reader.get_char() == "x"
        assert reader.position == Position(1, 1, 2)

        assert reader.get_char() == "\n"
        assert reader.position == Position(2, 2, 1)

        assert reader.get_char() == "l"
        assert reader.get_char() == "e"
        assert reader.position == Position(4, 2, 3)


def test_get_char_cr(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"x\rlet"))
    with Reader("path") as reader:
        assert reader.get_char() == "x"
        assert reader.position == Position(1, 1, 2)

        assert reader.get_char() == "\n"
        assert reader.position == Position(2, 2, 1)

        assert reader.get_char() == "l"
        assert reader.get_char() == "e"
        assert reader.position == Position(4, 2, 3)


def test_get_char_crlf(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"x\r\nlet"))
    with Reader("path") as reader:
        assert reader.get_char() == "x"
        assert reader.position == Position(1, 1, 2)

        assert reader.get_char() == "\n"
        assert reader.position == Position(3, 2, 1)

        assert reader.get_char() == "l"
        assert reader.get_char() == "e"
        assert reader.position == Position(5, 2, 3)


def test_iterable(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"asd"))
    with Reader("path") as reader:
        assert isinstance(iter(reader), Iterable)


def test_iterator(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"asd"))
    with Reader("path") as reader:
        assert list(reader) == ["a", "s", "d"]


def test_read_char(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let"))
    with Reader("path") as reader:
        assert reader.get_char() == "l"
        assert reader.position == Position(1, 1, 2)

        assert reader.read_char() == "e"
        assert reader.position == Position(1, 1, 2)
        reader.read_char()
        assert reader.read_char() is None


def test_get_line(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\na\nb\n"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(2, 2, 1))[0] == "a"


def test_get_line_first_line(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a\nb\n"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(1, 1, 1))[0] == "a"


def test_get_line_first_line_blank_line(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"\na\nb\n"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(1, 1, 1))[0] == ""


def test_get_line_last_line(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a\nb\n"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(3, 2, 1))[0] == "b"


def test_get_line_last_line_blank_line(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a\nb\n"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(4, 3, 1))[0] == ""


def test_get_line_last_line_no_trailing_newline(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a\nb"))
    with Reader("path") as reader:
        list(reader)
        assert reader.get_line_n_offset(Position(3, 2, 1))[0] == "b"
