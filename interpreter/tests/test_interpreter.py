import io
from typing import Optional
from unittest.mock import patch

import pytest

from interpreter.comments_filter import CommentsFilter
from interpreter.error_handler.error_handler import ErrorHandler
from interpreter.interpreter import Var, DataType, Value, Function
from interpreter.interpreter.interpreter import Interpreter
from interpreter.lexer.ilexer import ILexer
from interpreter.lexer.lexer import Lexer
from interpreter.parser.parser import Parser
from interpreter.program import CaseIdentifier, LiteralType, Literal
from interpreter.program.operator import CaseOperator
from interpreter.program.statement import *
from interpreter.reader.reader import Reader
from interpreter.token import Token, TokenType
from interpreter.error_handler.error import *


class LexerMock(ILexer):
    def __init__(self, tokens):
        self.token = None
        self.tokens = tokens
        self.idx = 0

    def next_token(self) -> Optional[Token]:
        if not self.idx < len(self.tokens):
            return None
        t = self.tokens[self.idx]
        self.token = t
        self.idx += 1
        return t


class Mock:
    def __init__(self, error_handler: ErrorHandler):
        with Reader("path") as reader:
            lexer = Lexer(reader, error_handler)
            parser = Parser(CommentsFilter(lexer), error_handler)
            self.program = parser.parse()
            self.interpreter = Interpreter(error_handler)
            self.program.accept(self.interpreter)


@patch("builtins.open")
def test_visit_num_literal(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NUM, position, 1),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        interpreter = Interpreter(error_handler)

        stmt = parser._parse_literal()
        stmt.accept(interpreter)
        assert interpreter._last_value.type == DataType.NUM


@patch("builtins.open")
def test_visit_str_literal(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.STR, position, "asd"),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        interpreter = Interpreter(error_handler)

        stmt = parser._parse_literal()
        stmt.accept(interpreter)
        assert interpreter._last_value.value == "asd"


@patch("builtins.open")
def test_visit_bool_literal(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.TRUE_VAL, position, True),
                Token(TokenType.FALSE_VAL, position, True),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        interpreter = Interpreter(error_handler)

        stmt = parser._parse_literal()
        stmt.accept(interpreter)
        assert interpreter._last_value.value == True
        stmt = parser._parse_literal()
        stmt.accept(interpreter)
        assert interpreter._last_value.value == False


@patch("builtins.open")
def test_visit_null_literal(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NULL_VAL, position, "asd"),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        interpreter = Interpreter(error_handler)

        stmt = parser._parse_literal()
        stmt.accept(interpreter)
        assert interpreter._last_value.value == None


def test_var_definition(mocker):
    mocker.patch(
        "builtins.open", return_value=io.BytesIO(b"let a = 1; let mut b = null;")
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var(
        "b", Value(DataType.NULL, None), True
    )


def test_var_assignment(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let mut a = 1; a = 0;"))
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 0), True)


def test_var_assignment_type_change(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let mut a = 1; a = '0';"))
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.STR, "0"), True)


def test_var_assignment_immutable(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1; a = '0';"))
    error_handler = ErrorHandler()
    with pytest.raises(AssignMut):
        m = Mock(error_handler)


def test_identifier_expression(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"let a = 1; let mut b = a;"))
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 1), True)


def test_eq_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let a = 1; let mut b = 2; let c = a == b;"),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var(
        "c", Value(DataType.BOOL, False), False
    )


def test_not_eq_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let a = 1; let mut b = 2; let c = a != b;"),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var(
        "c", Value(DataType.BOOL, True), False
    )


def test_less_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let a = 1; let mut b = 2; let c = a < b;"),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var(
        "c", Value(DataType.BOOL, True), False
    )


def test_less_eq_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let a = 1; let mut b = 2; let mut d = b; let c = a < b; let c1 = b <= b; let c2 = 4 <= b;"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var(
        "c", Value(DataType.BOOL, True), False
    )
    assert m.interpreter._scope.look_up("c1") == Var(
        "c1", Value(DataType.BOOL, True), False
    )
    assert m.interpreter._scope.look_up("c2") == Var(
        "c2", Value(DataType.BOOL, False), False
    )


def test_additive_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let a = 1; let mut b = 2; let c = b - a; let d = a - b;"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var("c", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("d") == Var("d", Value(DataType.NUM, -1), False)


def test_multiplicative_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let a = 1; let mut b = 2; let c = b * a; let d = a / b;  let e = a % b;"
        ),
    )

    error_handler = ErrorHandler()

    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, 2), True)
    assert m.interpreter._scope.look_up("c") == Var("c", Value(DataType.NUM, 2), False)
    assert m.interpreter._scope.look_up("d") == Var(
        "d", Value(DataType.NUM, 0.5), False
    )
    assert m.interpreter._scope.look_up("e") == Var("e", Value(DataType.NUM, 1), False)


def test_negated_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let a = 1; let b = -a; let c = not (a > 1)"),
    )

    error_handler = ErrorHandler()

    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a") == Var("a", Value(DataType.NUM, 1), False)
    assert m.interpreter._scope.look_up("b") == Var("b", Value(DataType.NUM, -1), False)
    assert m.interpreter._scope.look_up("c") == Var(
        "c", Value(DataType.BOOL, True), False
    )


def test_visit_function_definition_statement(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"fn a(){return 1;}"))

    error_handler = ErrorHandler()
    m = Mock(error_handler)
    fn = m.interpreter._scope.look_up("a")
    assert type(fn) == Function
    assert fn.name == "a"


def test_visit_function_call_statement(mocker):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"fn a(){return 1;} a()"))

    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._last_value == Value(DataType.NUM, 1)
    assert len(m.interpreter._scope.stack) == 0


def test_loop(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let mut a = 1; while a < 5 {a = a + 1; }"),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 5


def test__if_matches_parity_odd():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, 1)]
    params2 = [Value(DataType.NUM, 2)]
    identifier = CaseIdentifier(CaseOperator.IS_ODD, Position(0, 0, 0))
    res = i._if_matches_parity(params1, identifier)
    assert res is True
    res = i._if_matches_parity(params2, identifier)
    assert res is False

    with pytest.raises(UnexpectedType):
        i._if_matches_parity([Value(DataType.STR, "1")], identifier)


def test__if_matches_parity_even():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, 1)]
    params2 = [Value(DataType.NUM, 2)]
    identifier = CaseIdentifier(CaseOperator.IS_EVEN, Position(0, 0, 0))
    res = i._if_matches_parity(params2, identifier)
    assert res is True
    res = i._if_matches_parity(params1, identifier)
    assert res is False

    with pytest.raises(UnexpectedType):
        i._if_matches_parity([Value(DataType.STR, "1")], identifier)


def test__if_matches_quarter_one():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, 1), Value(DataType.NUM, 2)]
    params2 = [Value(DataType.NUM, 1), Value(DataType.NUM, 10)]
    params3 = [Value(DataType.NUM, 0), Value(DataType.NUM, 10)]
    params4 = [Value(DataType.NUM, 1), Value(DataType.NUM, -10)]
    identifier = CaseIdentifier(CaseOperator.IS_QUARTERO, Position(0, 0, 0))
    res = i._if_matches_quarter(params1, identifier)
    assert res is True
    res = i._if_matches_quarter(params2, identifier)
    assert res is True
    res = i._if_matches_quarter(params3, identifier)
    assert res is False
    res = i._if_matches_quarter(params4, identifier)
    assert res is False

    with pytest.raises(MissingParameter):
        i._if_matches_quarter([Value(DataType.STR, "1")], identifier)


def test__if_matches_quarter_two():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, -1), Value(DataType.NUM, 2)]
    params2 = [Value(DataType.NUM, -1), Value(DataType.NUM, 10)]
    params3 = [Value(DataType.NUM, 0), Value(DataType.NUM, 10)]
    params4 = [Value(DataType.NUM, 1), Value(DataType.NUM, -10)]
    identifier = CaseIdentifier(CaseOperator.IS_QUARTERTW, Position(0, 0, 0))
    res = i._if_matches_quarter(params1, identifier)
    assert res is True
    res = i._if_matches_quarter(params2, identifier)
    assert res is True
    res = i._if_matches_quarter(params3, identifier)
    assert res is False
    res = i._if_matches_quarter(params4, identifier)
    assert res is False

    with pytest.raises(MissingParameter):
        i._if_matches_quarter([Value(DataType.STR, "1")], identifier)


def test__if_matches_quarter_three():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, -1), Value(DataType.NUM, -2)]
    params2 = [Value(DataType.NUM, -1), Value(DataType.NUM, -10)]
    params3 = [Value(DataType.NUM, 0), Value(DataType.NUM, 10)]
    params4 = [Value(DataType.NUM, 1), Value(DataType.NUM, 10)]
    identifier = CaseIdentifier(CaseOperator.IS_QUARTERTH, Position(0, 0, 0))
    res = i._if_matches_quarter(params1, identifier)
    assert res is True
    res = i._if_matches_quarter(params2, identifier)
    assert res is True
    res = i._if_matches_quarter(params3, identifier)
    assert res is False
    res = i._if_matches_quarter(params4, identifier)
    assert res is False

    with pytest.raises(MissingParameter):
        i._if_matches_quarter([Value(DataType.STR, "1")], identifier)


def test__if_matches_quarter_four():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params1 = [Value(DataType.NUM, 1), Value(DataType.NUM, -2)]
    params2 = [Value(DataType.NUM, 1), Value(DataType.NUM, -10)]
    params3 = [Value(DataType.NUM, 0), Value(DataType.NUM, 10)]
    params4 = [Value(DataType.NUM, 1), Value(DataType.NUM, 10)]
    identifier = CaseIdentifier(CaseOperator.IS_QUARTERF, Position(0, 0, 0))
    res = i._if_matches_quarter(params1, identifier)
    assert res is True
    res = i._if_matches_quarter(params2, identifier)
    assert res is True
    res = i._if_matches_quarter(params3, identifier)
    assert res is False
    res = i._if_matches_quarter(params4, identifier)
    assert res is False

    with pytest.raises(MissingParameter):
        i._if_matches_quarter([Value(DataType.STR, "1")], identifier)


def test__if_matches_types():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params = [Value(DataType.NUM, 1)]
    identifier = CaseIdentifier(LiteralType.NUM, Position(0, 0, 0))
    res = i._if_matches_types(params, identifier)
    assert res is True


def test__if_matches_literal():
    error_handler = ErrorHandler()
    i = Interpreter(error_handler)

    params = [Value(DataType.NUM, 1)]
    identifier = CaseIdentifier(
        Literal(LiteralType.NUM, 1, Position(0, 0, 0)), Position(0, 0, 0)
    )
    res = i._if_matches_literal(params, identifier)
    assert res is True

    with pytest.raises(UnexpectedType):
        i._if_matches_literal([Value(DataType.STR, "1")], identifier)


def test_match_odd(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 1; match a: case isOdd: {a=a+1} case isEven: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 2


def test_match_even(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 2; match a: case isOdd: {a=a+1} case isEven: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 4


def test_match_quarter(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 2; match a: case isOdd: {a=a+1} case isEven: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 4


def test_match_type(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 2; match a: case num: {a=a+1} case isEven: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 3


def test_match_literal(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 2; match a: case 2: {a=a+1} case isEven: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 3


def test_match_default(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(
            b"let mut a = 2; match a: case 1: {a=a+1} default: {a=a+2}"
        ),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value == 4


def test_or_expression(mocker):
    mocker.patch(
        "builtins.open",
        return_value=io.BytesIO(b"let a = true or false"),
    )
    error_handler = ErrorHandler()
    m = Mock(error_handler)
    assert m.interpreter._scope.look_up("a").value.value is True


def test_print(mocker, capsys):
    mocker.patch("builtins.open", return_value=io.BytesIO(b"print('s')"))
    error_handler = ErrorHandler()
    m = Mock(error_handler)

    out, err = capsys.readouterr()
    assert out == "s"
    assert len(m.interpreter._scope.stack) == 0
