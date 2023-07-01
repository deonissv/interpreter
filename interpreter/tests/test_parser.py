from typing import Optional
from unittest.mock import patch

import pytest

from interpreter.error_handler import ErrorType
from interpreter.error_handler.error_handler import ErrorHandler
from interpreter.lexer.ilexer import ILexer
from interpreter.parser.parser import Parser
from interpreter.program import (
    CaseIdentifier,
    LiteralType,
    Literal,
    Expression,
    OrExpression,
)
from interpreter.program.operator import CaseOperator
from interpreter.program.statement import *
from interpreter.reader.reader import Reader
from interpreter.token import Token, TokenType


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


@patch("builtins.open")
def test__consume_if(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        assert parser._consume_if(TokenType.IDENTIFIER)
        assert lexer.token.token_type == TokenType.LESS_OPERATOR


@patch("builtins.open")
def test__consume_if_false(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        assert parser._consume_if(TokenType.IDENTIFIER) is False
        assert lexer.token.token_type == TokenType.LESS_OPERATOR


@patch("builtins.open")
def test_consume_if_iter_list(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        assert parser._consume_if([TokenType.ELSE, TokenType.IDENTIFIER])
        assert lexer.token.token_type == TokenType.LESS_OPERATOR


@patch("builtins.open")
def test_consume_if_iter_tuple(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        assert parser._consume_if((TokenType.ELSE, TokenType.IDENTIFIER))
        assert lexer.token.token_type == TokenType.LESS_OPERATOR


@patch("builtins.open")
def test_consume_if_iter_false(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LESS_OPERATOR, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        assert parser._consume_if([TokenType.ELSE, TokenType.IDENTIFIER]) is False
        assert lexer.token.token_type == TokenType.LESS_OPERATOR


@patch("builtins.open")
def test_consume_if_iter_unknown_type(_mocker):
    with pytest.raises(Exception):
        with Reader("path") as _reader:
            position = Position(0, 0, 0)
            lexer = LexerMock(
                [
                    Token(TokenType.IDENTIFIER, position),
                    Token(TokenType.LESS_OPERATOR, position),
                ]
            )
            parser = Parser(lexer, ErrorHandler())
            parser._consume_if(1)


@patch("builtins.open")
def test__parse_var_definition(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        l_pos = Position(1, 1, 1)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, l_pos, 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert stmt.name == "id"
        assert stmt.expression == Literal(LiteralType.NUM, 123, l_pos)


@patch("builtins.open")
def test__parse_var_definition_name_expected(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )

        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert error_handler[0].type == ErrorType.VARIABLE_NAME_EXPECTED


@patch("builtins.open")
def test__parse_var_definition_assignment_operator_expected(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )

        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert error_handler[0].type == ErrorType.ASSIGNMENT_OPERATOR_EXPECTED


@patch("builtins.open")
def test__parse_var_definition_expression_expected(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.SEMICOLON, position),
            ]
        )

        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert error_handler[0].type == ErrorType.EXPRESSION_EXPECTED


@patch("builtins.open")
def test__parse_var_definition_semicolon_expected(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.NUM, position, 123),
            ]
        )

        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert error_handler[0].type == ErrorType.SEMICOLON_EXPECTED


@patch("builtins.open")
def test__parse_var_definition_mut(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.MUT, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, Position(1, 1, 1), 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_var_definition()
        assert type(stmt) == VarDefinition
        assert stmt.mut is True
        assert stmt.name == "id"
        assert stmt.expression == Literal(LiteralType.NUM, 123, Position(1, 1, 1))


@patch("builtins.open")
def test__parse_assignment(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, Position(1, 1, 1), 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_identifier_or_assignment_or_function_call()
        assert type(stmt) == Assignment
        assert stmt.name == "id"
        assert stmt.expression == Literal(LiteralType.NUM, 123, Position(1, 1, 1))


@patch("builtins.open")
def test__parse_assignment_fail(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.SEMICOLON, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_identifier_or_assignment_or_function_call()
        assert stmt is None


@patch("builtins.open")
def test__parse_conditional_statement(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IF, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.ELSE, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_conditional_statement()
        assert type(stmt) == ConditionalStatement
        assert type(stmt.else_block) == Block


@patch("builtins.open")
def test__parse_conditional_statement_no_else(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IF, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_conditional_statement()
        assert type(stmt) == ConditionalStatement
        assert stmt.else_block is None


@patch("builtins.open")
def test__parse_conditional_statement_no_condition(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IF, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_conditional_statement()
        assert type(stmt) == ConditionalStatement
        assert error_handler[0].type == ErrorType.EXPRESSION_EXPECTED


@patch("builtins.open")
def test__parse_conditional_statement_no_if_block(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IF, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.ELSE, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_conditional_statement()
        assert type(stmt) == ConditionalStatement
        assert error_handler[0].type == ErrorType.CODE_BLOCK_EXPECTED


@patch("builtins.open")
def test__parse_conditional_no_else_block(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IF, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.ELSE, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_conditional_statement()
        assert type(stmt) == ConditionalStatement
        assert error_handler[0].type == ErrorType.CODE_BLOCK_EXPECTED


@patch("builtins.open")
def test__loop_statement(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.WHILE, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_loop_statement()
        assert type(stmt) == LoopStatement


@patch("builtins.open")
def test__loop_statement_no_condition(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.WHILE, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_loop_statement()
        assert type(stmt) == LoopStatement
        assert error_handler[0].type == ErrorType.EXPRESSION_EXPECTED


@patch("builtins.open")
def test__loop_statement_no_body(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.WHILE, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.LESS_OPERATOR, position),
                Token(TokenType.NUM, position, 123),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_loop_statement()
        assert type(stmt) == LoopStatement
        assert error_handler[0].type == ErrorType.CODE_BLOCK_EXPECTED


@patch("builtins.open")
def test__parse_parameters(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(
                    TokenType.COMMA,
                    position,
                ),
                Token(TokenType.IDENTIFIER, position, "x"),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        param = parser._parse_parameter()
        assert type(param) == Parameter


@patch("builtins.open")
def test__parse_parameters_mut(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.MUT, position),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.COMMA, position),
                Token(TokenType.IDENTIFIER, position, "x"),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        param = parser._parse_parameter()
        assert type(param) == Parameter
        assert param.mut is True


@patch("builtins.open")
def test__parse_parameters_trailing_comma(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(
                    TokenType.COMMA,
                    position,
                ),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(
                    TokenType.COMMA,
                    position,
                ),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(
                    TokenType.COMMA,
                    position,
                ),
                Token(
                    TokenType.LEFT_BRACKET,
                    position,
                ),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_parameters()
        assert type(stmt) == list
        assert type(stmt[0]) == Parameter


@patch("builtins.open")
def test__parse_parameters_empty(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(
                    TokenType.CASE,
                    position,
                ),
                Token(
                    TokenType.EOF,
                    position,
                ),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        params = parser._parse_parameters()
        assert type(params) == list
        assert len(params) == 0


@patch("builtins.open")
def test__parse_match_statement(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.MATCH, position),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.COLON, position),
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.DEFAULT, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 12),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        stmt = parser._parse_match_statement()
        assert type(stmt) == MatchStatement


@patch("builtins.open")
def test__parse_case_identifier_identifier(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.STR, position, "n"),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        identifier = parser._parse_case_identifier()
        assert type(identifier) == CaseIdentifier


@patch("builtins.open")
def test__parse_case_identifier_case_operator(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        identifier = parser._parse_case_identifier()
        assert type(identifier) == CaseIdentifier
        assert identifier.identifier == CaseOperator.IS_EVEN


@patch("builtins.open")
def test__parse_case_identifier_type(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NUM_TYPE, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        identifier = parser._parse_case_identifier()
        assert type(identifier) == CaseIdentifier
        assert identifier.identifier == LiteralType.NUM


@patch("builtins.open")
def test__parse_case_identifier_fail(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.CASE, position),
                Token(TokenType.EOF, position),
            ]
        )
        parser = Parser(lexer, ErrorHandler())
        identifier = parser._parse_case_identifier()
        assert identifier is None


@patch("builtins.open")
def test__parse_case_stmt_no_identifier(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        case_stmt = parser._parse_case_stmts()
        assert type(case_stmt) == list
        assert type(case_stmt[0]) == CaseStatement


@patch("builtins.open")
def test__parse_case_stmt_no_colon(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        case_stmt = parser._parse_case_stmts()
        assert error_handler[0].type == ErrorType.COLON_EXPECTED


@patch("builtins.open")
def test__parse_default_stmt(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.DEFAULT, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 12),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_default_stmt()
        assert type(stmt) == CaseDefaultStatement


@patch("builtins.open")
def test__parse_default_stmt_no_colon(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.DEFAULT, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 12),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_default_stmt()
        assert error_handler[0].type == ErrorType.COLON_EXPECTED


@patch("builtins.open")
def test__parse_match_statement_no_pattern(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.MATCH, position),
                Token(TokenType.COLON, position),
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.DEFAULT, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 12),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_match_statement()
        assert type(stmt) == MatchStatement
        assert error_handler[0].type == ErrorType.EXPRESSION_EXPECTED


@patch("builtins.open")
def test__parse_match_statement_no_colon(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.MATCH, position),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.DEFAULT, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 12),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_match_statement()
        assert type(stmt) == MatchStatement
        assert error_handler[0].type == ErrorType.COLON_EXPECTED


@patch("builtins.open")
def test__parse_match_statement_no_default_stmt(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.MATCH, position),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.CASE, position),
                Token(TokenType.IS_EVEN_OPERATOR, position),
                Token(TokenType.COLON, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position, "id"),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position, 1),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_match_statement()
        assert type(stmt) == MatchStatement
        assert error_handler[0].type == ErrorType.COLON_EXPECTED


@patch("builtins.open")
def test__parse_function_definition(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.FN, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_function_definition()
        assert type(stmt) == FunctionDefinitionStatement


@patch("builtins.open")
def test__parse_function_definition_no_identifier(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.FN, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_function_definition()
        assert error_handler[0].type == ErrorType.IDENTIFIER_EXPECTED


@patch("builtins.open")
def test__parse_function_definition_no_left_bracket(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.FN, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_function_definition()
        assert type(stmt) == FunctionDefinitionStatement
        assert error_handler[0].type == ErrorType.LEFT_BRACKET_EXPECTED


@patch("builtins.open")
def test__parse_function_definition_no_right_bracket(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.FN, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.LEFT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
                Token(TokenType.LET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.ASSIGNMENT_OPERATOR, position),
                Token(TokenType.NUM, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.RIGHT_CURLY_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_function_definition()
        assert type(stmt) == FunctionDefinitionStatement
        assert error_handler[0].type == ErrorType.RIGHT_BRACKET_EXPECTED


@patch("builtins.open")
def test__parse_function_call(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_assignment_or_function_call()
        assert type(stmt) == FunctionCallStatement


@patch("builtins.open")
def test__parse_function_call_no_semicolon(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_assignment_or_function_call()
        assert type(stmt) == FunctionCallStatement
        assert error_handler[0].type == ErrorType.SEMICOLON_EXPECTED


@patch("builtins.open")
def test__parse_function_call_no_right_bracket(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.SEMICOLON, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_assignment_or_function_call()
        assert type(stmt) == FunctionCallStatement
        assert error_handler[0].type == ErrorType.RIGHT_BRACKET_EXPECTED


@patch("builtins.open")
def test__parse_return_statement(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.RETURN, position, "x"),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_return_statement()
        assert type(stmt) == ReturnStatement


@patch("builtins.open")
def test__parse_or_expression(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.OR_OPERATOR, position),
                Token(TokenType.IDENTIFIER, position, "y"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert type(stmt) == OrExpression


@patch("builtins.open")
def test__parse_or_expression_from_identifier(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.OR_OPERATOR, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)
        assert error_handler[0].type == ErrorType.EXPRESSION_EXPECTED


@patch("builtins.open")
def test__parse_or_expression_no_2_operand(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [Token(TokenType.IDENTIFIER, position, "x"), Token(TokenType.EOF, position)]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_and_expression_no_2_operand(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.AND_OPERATOR, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_relational_expression_no_2_operand(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.LESS_OPERATOR, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_additive_expression_no_2_operand(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.ADDITION_OPERATOR, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_multiplicative_expression_no_2_operand(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.MULTIPLICATION_OPERATOR, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_negated_expression_unary_minus(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.SUBTRACTION_OPERATOR, position, "x"),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_unary_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_negated_expression_not(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NOT_OPERATOR, position, "x"),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_unary_expression()
        assert isinstance(stmt, Expression)


@patch("builtins.open")
def test__parse_literal_num(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [Token(TokenType.NUM, position, 1), Token(TokenType.EOF, position)]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_literal()
        assert stmt.type == LiteralType.NUM


@patch("builtins.open")
def test__parse_literal_str(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [Token(TokenType.STR, position, "x"), Token(TokenType.EOF, position)]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_literal()
        assert stmt.type == LiteralType.STR


@patch("builtins.open")
def test__parse_literal_bool(_mocker):
    with Reader("path") as _reader:
        position1 = Position(0, 0, 0)
        position2 = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.FALSE_VAL, position1, "x"),
                Token(TokenType.TRUE_VAL, position2, "x"),
                Token(TokenType.EOF, position1),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_literal()
        assert stmt == Literal(LiteralType.BOOL, False, position1)
        stmt = parser._parse_literal()
        assert stmt == Literal(LiteralType.BOOL, True, position2)


@patch("builtins.open")
def test__parse_literal_null(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [Token(TokenType.NULL_VAL, position, "x"), Token(TokenType.EOF, position)]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        stmt = parser._parse_literal()
        assert stmt == Literal(LiteralType.NULL, None, position)


@patch("builtins.open")
def test__parse_arguments(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NULL_VAL, position, "x"),
                Token(TokenType.COMMA, position, "x"),
                Token(TokenType.NULL_VAL, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        args = parser._parse_arguments()
        assert isinstance(args, list)
        assert isinstance(args[0], Expression)
        assert len(args) == 2


@patch("builtins.open")
def test__parse_arguments_trailing_comma(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.NULL_VAL, position, "x"),
                Token(TokenType.COMMA, position, "x"),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        args = parser._parse_arguments()
        assert isinstance(args, list)
        assert isinstance(args[0], Expression)
        assert len(args) == 1


@patch("builtins.open")
def test__parse_parenthesis(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position, "x"),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        expr = parser._parse_parenthesis()
        assert isinstance(expr, Expression)


@patch("builtins.open")
def test__parse_parenthesis_no_expr(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.RIGHT_BRACKET, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        expr = parser._parse_parenthesis()
        assert expr is None


@patch("builtins.open")
def test__parse_parenthesis_no_right_bracket(_mocker):
    with Reader("path") as _reader:
        position = Position(0, 0, 0)
        lexer = LexerMock(
            [
                Token(TokenType.LEFT_BRACKET, position),
                Token(TokenType.IDENTIFIER, position),
                Token(TokenType.EOF, position),
            ]
        )
        error_handler = ErrorHandler()
        parser = Parser(lexer, error_handler)
        expr = parser._parse_parenthesis()
        assert expr is None
