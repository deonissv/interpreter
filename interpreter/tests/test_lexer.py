import io

from interpreter.lexer.lexer import Lexer
from interpreter.position import Position
from interpreter.reader.reader import Reader
from interpreter.error_handler.error_handler import ErrorHandler
from interpreter.error_handler.error import ErrorType
from interpreter.token import TokenType


def test__build_base(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"123"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer._char == "1"
        i = lexer._build_base()
        assert i == 123


def test__build_base_leading_zero(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"0123"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer._build_base() is None


def test__build_base_overflow(mocker):
    mocker.patch(
        "builtins.open", return_value=io.BytesIO(f'{"9" * 99}a'.encode("utf-8"))
    )
    with Reader("path") as reader:
        error_handler = ErrorHandler()
        lexer = Lexer(reader, error_handler)
        assert lexer._build_base() is None
        assert reader.position == Position(100, 1, 101)
        assert error_handler[0].type == ErrorType.NUM_OVERFLOW_ERROR


def test__build_fraction(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"0123"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer._build_fraction() == 0.0123


def test__build_num_no_fraction(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"123asd"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        num = lexer._build_num()
        assert num.token_type == TokenType.NUM
        assert num.value == 123.0


def test__build_num_no_fraction_dot(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"123.asd"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        num = lexer._build_num()
        assert num.token_type == TokenType.NUM
        assert num.value == 123.0


def test__build_num_fraction(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"123.0123a"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        num = lexer._build_num()
        assert num.token_type == TokenType.NUM
        assert num.value == 123.0123


def test__build_num_leading_zero(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"0123.0123"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer._build_num() is None


def test__build_num_leading_non_digit(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"a0123"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer._build_num() is None


def test__build_div_operator_or_comment_div(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"/2"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert (
            lexer._build_div_operator_or_comment().token_type
            == TokenType.DIVISION_OPERATOR
        )


def test__build_div_operator_or_comment_one_line_comment(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"//asd\nzxc"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_div_operator_or_comment()
        assert token.token_type == TokenType.ONE_LINE_COMMENT
        assert token.value == "asd"
        assert lexer.next_token().token_type == TokenType.IDENTIFIER


def test__build_div_operator_or_comment_multiline_comment(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"/*asd*/"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_div_operator_or_comment()
        assert token.token_type == TokenType.MULTILINE_COMMENT
        assert token.value == "asd"


def test__build_div_operator_or_comment_multiline_comment_asterisk(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"/***99**asd***/zxc"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_div_operator_or_comment()
        assert token.token_type == TokenType.MULTILINE_COMMENT
        assert token.value == "**99**asd**"
        assert lexer.next_token().token_type == TokenType.IDENTIFIER


def test__build_div_operator_or_comment_unexpected_eof(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"/*asd"))
    with Reader("path") as reader:
        error_handler = ErrorHandler()
        lexer = Lexer(reader, error_handler)
        token = lexer._build_div_operator_or_comment()
        assert token is None
        assert error_handler[0].type == ErrorType.UNEXPECTED_END_OF_TEXT


def test__build_div_operator_or_comment_no_token(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"asd"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_div_operator_or_comment()
        assert token is None


def test__build_str_quote_single_quote(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"'as\"d'"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote("'")
        assert token.token_type == TokenType.STR
        assert token.value == 'as"d'


def test__build_str_quote_single_quote_escape_quote(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"'as\\'d'"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote("'")
        assert token.token_type == TokenType.STR
        assert token.value == "as'd"


def test__build_str_quote_double_quote(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b'"as\'d"'))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote('"')
        assert token.token_type == TokenType.STR
        assert token.value == "as'd"


def test__build_str_quote_double_quote_escape_quote(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b'"as\\"d"'))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote('"')
        assert token.token_type == TokenType.STR
        assert token.value == 'as"d'


def test__build_str_quote_escape_characters(mocker):
    mocker.patch(
        "builtins.open", return_value=io.BytesIO(b'"a\\\\a\na\ra\ta\ba\f\\q\\w"')
    )
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote('"')
        assert token.token_type == TokenType.STR
        assert token.value == "a\\a\na\ra\ta\ba\f\\q\\w"


def test__build_str_quote_unexpected_eof(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"'asd"))
    with Reader("path") as reader:
        error_handler = ErrorHandler()
        lexer = Lexer(reader, error_handler)
        token = lexer._build_str_quote("'")
        assert token is None
        assert error_handler[0].type == ErrorType.UNEXPECTED_END_OF_TEXT


def test__build_str_quote_unexpected_eof_escape_char(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"'asd\\"))
    with Reader("path") as reader:
        error_handler = ErrorHandler()
        lexer = Lexer(reader, error_handler)
        token = lexer._build_str_quote("'")
        assert token is None
        assert error_handler[0].type == ErrorType.UNEXPECTED_END_OF_TEXT


def test__build_str_quote_no_str(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"asd"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote("'")
        assert token is None


def test_build_str_single_quote(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"'a\\\\a\\\"a\\'a\na\ra\ta\ba\f\\q\\w'd"),
    )
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str()
        assert token.token_type == TokenType.STR
        assert token.value == "a\\a\"a'a\na\ra\ta\ba\f\\q\\w"
        assert lexer.next_token().token_type == TokenType.IDENTIFIER


def test_build_str_double_quote(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b'"a\\\\a\\"a\\\'a\na\ra\ta\ba\f\\q\\w"d'),
    )
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str()
        assert token.token_type == TokenType.STR
        assert token.value == "a\\a\"a'a\na\ra\ta\ba\f\\q\\w"
        assert lexer.next_token().token_type == TokenType.IDENTIFIER


def test__build_str_no_str(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"asd"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_str_quote("'")
        assert token is None


def test__build_str_unexpected_eof(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"'asd"))
    with Reader("path") as reader:
        error_handler = ErrorHandler()
        lexer = Lexer(reader, error_handler)
        token = lexer._build_str()
        assert token is None
        assert error_handler[0].type == ErrorType.UNEXPECTED_END_OF_TEXT


def test__build_operator_assignment(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"="))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.ASSIGNMENT_OPERATOR


def test__build_operator_not(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"!"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.NOT_OPERATOR


def test__build_operator_less(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"<"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.LESS_OPERATOR


def test__build_operator_greater(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b">"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.GREATER_OPERATOR


def test__build_operator_addition(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"+"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.ADDITION_OPERATOR


def test__build_operator_eq(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"=="))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_operator()
        assert token.token_type == TokenType.EQ_OPERATOR


def test__build_keyword_or_identifier_keyword(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"if"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_keyword_or_identifier()
        assert token.token_type == TokenType.IF


def test__build_keyword_or_identifier_identifier(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"ifi;"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_keyword_or_identifier()
        assert token.token_type == TokenType.IDENTIFIER


def test__build_eof_common(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b""))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_eof()
        assert token.token_type == TokenType.EOF


def test__build_eof_none(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"if"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        token = lexer._build_eof()
        assert token is None


def test_next_token(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let mut x = 1;"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer.next_token().token_type == TokenType.LET
        assert lexer.next_token().token_type == TokenType.MUT
        assert lexer.next_token().token_type == TokenType.IDENTIFIER
        assert lexer.next_token().token_type == TokenType.ASSIGNMENT_OPERATOR
        token = lexer.next_token()
        assert token.token_type == TokenType.NUM
        assert token.value == 1
        assert lexer.next_token().token_type == TokenType.SEMICOLON
        assert lexer.next_token().token_type == TokenType.EOF


def test_next_token_condition(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"if n < 0 { return null; }"))
    with Reader("path") as reader:
        lexer = Lexer(reader, ErrorHandler())
        assert lexer.next_token().token_type == TokenType.IF
        assert lexer.next_token().token_type == TokenType.IDENTIFIER
        assert lexer.next_token().token_type == TokenType.LESS_OPERATOR
        assert lexer.next_token().token_type == TokenType.NUM
        assert lexer.next_token().token_type == TokenType.LEFT_CURLY_BRACKET
        assert lexer.next_token().token_type == TokenType.RETURN
        assert lexer.next_token().token_type == TokenType.NULL_VAL
        assert lexer.next_token().token_type == TokenType.SEMICOLON
        assert lexer.next_token().token_type == TokenType.RIGHT_CURLY_BRACKET
        assert lexer.next_token().token_type == TokenType.EOF
