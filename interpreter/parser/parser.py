from collections.abc import Iterable
from typing import List, Optional

from interpreter.error_handler import ErrorHandler
from interpreter.lexer import ILexer
from interpreter.program import (
    Program,
    Statement,
    VarDefinition,
    ConditionalStatement,
    LoopStatement,
    MatchStatement,
    CaseStatement,
    CaseIdentifier,
    LiteralType,
    CaseDefaultStatement,
    FunctionDefinitionStatement,
    FunctionCallStatement,
    Assignment,
    IdentifierExpression,
    Parameter,
    ReturnStatement,
    Expression,
    OrExpression,
    AndExpression,
    RelationalExpression,
    AdditiveExpression,
    MultiplicativeExpression,
    NegatedFactor,
    Literal,
    Block,
)
from interpreter.program.operator import (
    CaseOperator,
    RelationalOperator,
    AdditiveOperator,
    MultiplicativeOperator,
    UnaryOperator,
)
from interpreter.program.statement import ContinueStatement, BreakStatement
from interpreter.token import Token, TokenType


class Parser:
    def __init__(self, lexer: ILexer, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._lexer = lexer
        self._token = lexer.next_token()

    def parse(self) -> Program:
        statements = []
        while statement := self._parse_statement():
            statements.append(statement)

        return Program(statements)

    def _parse_statement(self) -> Optional[Statement]:
        return (
            self._parse_var_definition()
            or self._parse_conditional_statement()
            or self._parse_loop_statement()
            or self._parse_match_statement()
            or self._parse_assignment_or_function_call()
            or self._parse_function_definition()
            or self._parse_return_statement()
            or self._parse_break_statement()
            or self._parse_continue_statement()
        )

    def _consume_if(self, token_type: TokenType | Iterable[TokenType]) -> bool:
        if type(token_type) is TokenType:
            return self.__consume_if(self._token.token_type == token_type)
        if isinstance(token_type, Iterable):
            return self.__consume_if(self._token.token_type in token_type)
        raise Exception("Unexpected token_type type")

    def __consume_if(self, condition: bool) -> bool:
        if condition:
            self.__consume()
            return True
        return False

    def __consume(self) -> Optional[Token]:
        token = self._lexer.next_token()
        self._token = token
        return self._token

    def _parse_var_definition(self) -> Optional[VarDefinition]:
        """
        assignment = "let", [ "mut"], identifier, assign_operator, expression, ";" ;

        :return:
        """
        if not self._consume_if(TokenType.LET):
            return None

        mut = self._consume_if(TokenType.MUT)

        position = self._token.position
        if self._token.token_type != TokenType.IDENTIFIER:
            self._error_handler.variable_name_expected(self._token.position)
        name = self._token.value
        self._token = self.__consume()

        if not self._consume_if(TokenType.ASSIGNMENT_OPERATOR):
            self._error_handler.assignment_operator_expected(self._token.position)

        expression = self._parse_expression()
        if not expression:
            self._error_handler.expression_expected(self._token.position)

        if not self._consume_if(TokenType.SEMICOLON):
            self._error_handler.semicolon_expected(self._token.position)

        return VarDefinition(name, expression, position, mut)

    def _parse_conditional_statement(self) -> Optional[ConditionalStatement]:
        """
        conditional_statement = "if", expression, code_block, [ "else", code_block ];

        :return:
        """
        if not self._consume_if(TokenType.IF):
            return None

        condition = self._parse_expression()
        if condition is None:
            self._error_handler.expression_expected(self._token.position)

        if_block = self._parse_block()
        if if_block is None:
            self._error_handler.code_block_expected(self._token.position)

        if not self._consume_if(TokenType.ELSE):
            return ConditionalStatement(condition, if_block)

        else_block = self._parse_block()
        if else_block is None:
            self._error_handler.code_block_expected(self._token.position)
        return ConditionalStatement(condition, if_block, else_block)

    def _parse_loop_statement(self) -> Optional[LoopStatement]:
        """
        loop_statement = "while", expression, code_block;

        :return:
        """
        if not self._consume_if(TokenType.WHILE):
            return None

        condition = self._parse_expression()
        if condition is None:
            self._error_handler.expression_expected(self._token.position)

        loop_body = self._parse_block()
        if loop_body is None:
            self._error_handler.code_block_expected(self._token.position)
        return LoopStatement(condition, loop_body)

    def _parse_match_statement(self) -> Optional[MatchStatement]:
        """
        match_statement = "match", match_arguments, ":", { case_statement }, default_statement;

        :return:
        """
        position = self._token.position
        if not self._consume_if(TokenType.MATCH):
            return None

        match_args = self._parse_arguments()
        if len(match_args) == 0:
            self._error_handler.expression_expected(self._token.position)

        if not self._consume_if(TokenType.COLON):
            self._error_handler.colon_expected(self._token.position)

        case_stmts = self._parse_case_stmts()

        default_stmt = self._parse_default_stmt()
        if default_stmt is None:
            self._error_handler.default_statement_expected(self._token.position)

        return MatchStatement(match_args, case_stmts, default_stmt, position)

    def _parse_case_stmts(self) -> List[CaseStatement]:
        """
        case_statement = "case", identifier, ":", case_parameters, code_block;

        :return:
        """
        stmts = []
        while self._consume_if(TokenType.CASE):
            case_identifier = self._parse_case_identifier()
            if case_identifier is None:
                self._error_handler.expression_expected(self._token.position)

            if not self._consume_if(TokenType.COLON):
                self._error_handler.colon_expected(self._token.position)

            case_params = self._parse_parameters()

            case_body = self._parse_block()
            stmts.append(CaseStatement(case_identifier, case_params, case_body))
        return stmts

    def _parse_case_identifier(self) -> Optional[CaseIdentifier]:
        """
        case_identifier = literal
                        | data_type;
                        | case_operator;

        :return:
        """
        case_identifier = None
        position = self._token.position
        if self._token.token_type in Token.CASE_OPERATORS:
            case_identifier = CaseIdentifier(
                CaseOperator.from_token(self._token), position
            )
            self._token = self.__consume()
        elif self._token.token_type in Token.DATA_TYPES:
            case_identifier = CaseIdentifier(
                LiteralType.from_token(self._token), position
            )
            self._token = self.__consume()
        elif literal := self._parse_literal():
            case_identifier = CaseIdentifier(literal, position)
        return case_identifier

    def _parse_default_stmt(self) -> Optional[CaseDefaultStatement]:
        """
        default_statement = "default", ":", case_parameters, code_block;

        :return:
        """

        if not self._consume_if(TokenType.DEFAULT):
            return None

        if not self._consume_if(TokenType.COLON):
            self._error_handler.colon_expected(self._token.position)

        params = self._parse_parameters()
        default_body = self._parse_block()

        return CaseDefaultStatement(params, default_body)

    def _parse_function_definition(self) -> Optional[FunctionDefinitionStatement]:
        """
        function_definition = "fn", identifier, "(", [function_parameters] ")", code_block;

        :return:
        """

        if not self._consume_if(TokenType.FN):
            return None

        if self._token.token_type != TokenType.IDENTIFIER:
            self._error_handler.identifier_expected(self._token.position)

        name = self._token.value
        self._token = self.__consume()

        if not self._consume_if(TokenType.LEFT_BRACKET):
            self._error_handler.left_bracket_expected(self._token.position)

        params = self._parse_parameters()

        if not self._consume_if(TokenType.RIGHT_BRACKET):
            self._error_handler.right_bracket_expected(self._token.position)

        function_body = self._parse_block()
        return FunctionDefinitionStatement(name, params, function_body)

    def _parse_assignment_or_function_call(
        self,
    ) -> Optional[Assignment | FunctionCallStatement]:
        stmt = self._parse_identifier_or_assignment_or_function_call()
        if stmt is None or type(stmt) == IdentifierExpression:
            return None
        if not self._consume_if(TokenType.SEMICOLON):
            self._error_handler.semicolon_expected(self._token.position)
        return stmt

    def _parse_parameters(self) -> List[Parameter]:
        """
        function_parameters = function_parameter, {",", function_parameter};

        :return:
        """
        parameters = []
        param = self._parse_parameter()
        if param is None:
            return parameters
        parameters.append(param)

        while self._consume_if(TokenType.COMMA):
            param = self._parse_parameter()
            if param is None:
                return parameters
            parameters.append(param)
        return parameters

    def _parse_parameter(self) -> Optional[Parameter]:
        """
        function_parameter = ["mut"], identifier;

        :return:
        """
        mut = self._consume_if(TokenType.MUT)
        if self._token.token_type != TokenType.IDENTIFIER:
            return None
        param = Parameter(self._token.value, mut)
        self._token = self.__consume()
        return param

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        if not self._consume_if(TokenType.RETURN):
            return None

        expression = self._parse_expression()
        if not self._consume_if(TokenType.SEMICOLON):
            self._error_handler.semicolon_expected(self._token.position)
        return ReturnStatement(expression)

    def _parse_continue_statement(self) -> Optional[ContinueStatement]:
        if not self._consume_if(TokenType.CONTINUE):
            return None

        if not self._consume_if(TokenType.SEMICOLON):
            self._error_handler.semicolon_expected(self._token.position)
        return ContinueStatement()

    def _parse_break_statement(self) -> Optional[BreakStatement]:
        if not self._consume_if(TokenType.BREAK):
            return None

        if not self._consume_if(TokenType.SEMICOLON):
            self._error_handler.semicolon_expected(self._token.position)
        return BreakStatement()

    def _parse_expression(self) -> Optional[Expression]:
        """
        expression = or_expression;

        :return:
        """
        return self._parse_or_expression()

    def _parse_or_expression(self) -> Optional[Expression]:
        """
        or_expression = and_expression, { "or", and_expression };

        :return:
        """
        left = self._parse_and_expression()
        if left is None:
            return None

        position = self._token.position
        while self._consume_if(TokenType.OR_OPERATOR):
            right = self._parse_and_expression()
            if right is None:
                self._error_handler.expression_expected(self._token.position)
            left = OrExpression(left, right, position)
            position = self._token.position

        return left

    def _parse_and_expression(self) -> Optional[Expression]:
        """
        and_expression = relational_expression, { "and", relational_expression };
        :return:
        """
        left = self._parse_relational_expression()
        if left is None:
            return None

        position = self._token.position
        while self._consume_if(TokenType.AND_OPERATOR):
            right = self._parse_relational_expression()
            if right is None:
                self._error_handler.expression_expected(self._token.position)
            left = AndExpression(left, right, position)
            position = self._token.position

        return left

    def _parse_relational_expression(self) -> Optional[Expression]:
        """
        relational_expression = additive_expression, { relational_operator, additive_expression};
        :return:
        """
        left = self._parse_additive_expression()
        if left is None:
            return None

        position = self._token.position
        while self._token.token_type in Token.RELATIONAL_OPERATORS:
            operator = RelationalOperator.from_token(self._token)
            self._token = self.__consume()

            right = self._parse_additive_expression()
            if right is None:
                self._error_handler.expression_expected(self._token.position)
            left = RelationalExpression(operator, left, right, position)
            position = self._token.position

        return left

    def _parse_additive_expression(self) -> Optional[Expression]:
        """
        additive_expression = multiplicative_expression, { additive_operator, multiplicative_expression };
        :return:
        """
        left = self._parse_multiplicative_expression()
        if left is None:
            return None

        position = self._token.position
        while self._token.token_type in Token.ADDITIVE_OPERATORS:
            operator = AdditiveOperator.from_token(self._token)
            self._token = self.__consume()

            right = self._parse_multiplicative_expression()
            if right is None:
                self._error_handler.expression_expected(self._token.position)
            left = AdditiveExpression(operator, left, right, position)
            position = self._token.position

        return left

    def _parse_multiplicative_expression(self) -> Optional[Expression]:
        """
        multiplicative_expression = unary_expression, { multiplicative_operator, unary_expression };
        :return:
        """
        left = self._parse_unary_expression()
        if left is None:
            return None

        position = self._token.position
        while self._token.token_type in Token.MULTIPLICATIVE_OPERATORS:
            operator = MultiplicativeOperator.from_token(self._token)
            self._token = self.__consume()

            right = self._parse_unary_expression()
            if right is None:
                self._error_handler.expression_expected(self._token.position)
            left = MultiplicativeExpression(operator, left, right, position)
            position = self._token.position

        return left

    def _parse_unary_expression(self) -> Optional[Expression]:
        """
        unary_expression = [ unary_operator ] factor;
        :return:
        """

        unary_operator = self._token
        position = self._token.position
        negated = self._consume_if(Token.UNARY_OPERATORS)
        factor = self._parse_factor()
        if negated:
            return NegatedFactor(
                UnaryOperator.from_token(unary_operator), factor, position
            )
        return factor

    def _parse_factor(self) -> Optional[Expression]:
        """
        factor = literal
                | identifier
                | function_call
                | "(", expression, ")";
        :return:
        """

        expression = (
            self._parse_literal()
            or self._parse_identifier_or_assignment_or_function_call()
            or self._parse_parenthesis()
        )

        if expression is None:
            return None
        return expression

    def _parse_literal(self) -> Optional[Literal]:
        """
        literal = number
                | string
                | bool
                | "null";
        :return:
        """
        token = self._token
        position = self._token.position
        if self._consume_if(TokenType.NUM):
            return Literal(LiteralType.NUM, float(token.value), position)
        if self._consume_if(TokenType.STR):
            return Literal(LiteralType.STR, token.value, position)
        if self._consume_if(TokenType.TRUE_VAL):
            return Literal(LiteralType.BOOL, True, position)
        if self._consume_if(TokenType.FALSE_VAL):
            return Literal(LiteralType.BOOL, False, position)
        if self._consume_if(TokenType.NULL_VAL):
            return Literal(LiteralType.NULL, None, position)

    def _parse_identifier_or_assignment_or_function_call(
        self,
    ) -> Optional[IdentifierExpression | Assignment | FunctionCallStatement]:
        identifier = self._token
        position = self._token.position

        if not self._consume_if(TokenType.IDENTIFIER):
            return None

        if self._consume_if(TokenType.ASSIGNMENT_OPERATOR):
            expression = self._parse_expression()
            return Assignment(identifier.value, expression, position)

        position = self._token.position
        if self._consume_if(TokenType.LEFT_BRACKET):
            arguments = self._parse_arguments()
            r_position = self._token.position
            if not self._consume_if(TokenType.RIGHT_BRACKET):
                self._error_handler.right_bracket_expected(self._token.position)
                r_position = position
            return FunctionCallStatement(
                identifier.value, arguments, position, r_position
            )

        return IdentifierExpression(identifier.value, position)

    def _parse_arguments(self) -> List[Expression]:
        """
        argument_list = expression, {",", expression};

        :return:
        """
        arguments = []
        expression = self._parse_expression()
        if expression is not None:
            arguments.append(expression)
        while self._consume_if(TokenType.COMMA):
            expression = self._parse_expression()
            if expression is None:
                return arguments
            arguments.append(expression)
        return arguments

    def _parse_parenthesis(self) -> Optional[Expression]:
        if not self._consume_if(TokenType.LEFT_BRACKET):
            return None

        expression = self._parse_expression()
        if expression is None:
            return None

        if not self._consume_if(TokenType.RIGHT_BRACKET):
            return None
        return expression

    def _parse_block(self) -> Optional[Block]:
        if not self._consume_if(TokenType.LEFT_CURLY_BRACKET):
            return None

        statements = []
        while statement := self._parse_statement():
            statements.append(statement)

        if not self._consume_if(TokenType.RIGHT_CURLY_BRACKET):
            self._error_handler.right_curly_bracket_expected(self._token.position)
            return None

        return Block(statements)
