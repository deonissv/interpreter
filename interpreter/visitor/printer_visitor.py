from typing import Callable, List

from interpreter.program import (
    IdentifierExpression,
    Literal,
    LiteralType,
    FunctionCallStatement,
    FunctionDefinitionStatement,
    MatchStatement,
    CaseDefaultStatement,
    CaseStatement,
    CaseIdentifier,
    LoopStatement,
    ConditionalStatement,
    Assignment,
    Block,
    Parameter,
    NegatedFactor,
    MultiplicativeExpression,
    AdditiveExpression,
    RelationalExpression,
    AndExpression,
    OrExpression,
    Statement,
    ReturnStatement,
    VarDefinition,
)
from interpreter.program.program import Program
from interpreter.program.statement import BreakStatement, ContinueStatement
from interpreter.visitor.visitor import Visitor


class PrinterVisitor(Visitor):
    def __init__(self, indent_len: int = 2, indent_char: str = " "):
        self._indent = 0
        self._indent_len = indent_len
        self._indent_char = indent_char

    @staticmethod
    def _make_indent(fn: Callable):
        def wrapper(self: "PrinterVisitor", stmt: Statement):
            self._print(stmt.__class__.__name__)
            self._indent += self._indent_len
            fn(self, stmt)
            self._indent -= self._indent_len

        return wrapper

    def _print(self, msg: str):
        print(f"{self._indent_char * self._indent}|{self._indent_char}{msg}")

    def _accept_params(self, params: List[Parameter], title="Parameters"):
        self._print(title)
        self._indent += self._indent_len
        for param in params:
            param.accept(self)
        self._indent -= self._indent_len

    def visit_program(self, program: Program):
        print(f"{program.__class__.__name__}")
        for stmt in program.statements:
            stmt.accept(self)

    def visit_continue_statement(self, statement: ContinueStatement):
        self._print(f"{statement.__class__.__name__}")

    def visit_break_statement(self, statement: BreakStatement):
        self._print(f"{statement.__class__.__name__}")

    def visit_identifier_expression(self, expression: IdentifierExpression):
        self._print(f"{expression.__class__.__name__}: {expression.name}")

    def visit_literal(self, expression: Literal):
        self._print(
            f"{expression.__class__.__name__}: {expression.type} | {expression.value}"
        )

    @_make_indent
    def visit_or_expression(self, expression: OrExpression):
        expression.left.accept(self)
        expression.right.accept(self)

    @_make_indent
    def visit_and_expression(self, expression: AndExpression):
        expression.left.accept(self)
        if expression.right is not None:
            expression.right.accept(self)

    @_make_indent
    def visit_relational_expression(self, expression: RelationalExpression):
        self._print(f"{expression.operator}")
        expression.left.accept(self)
        if expression.right is not None:
            expression.right.accept(self)

    @_make_indent
    def visit_additive_expression(self, expression: AdditiveExpression):
        self._print(f"Operator: {expression.operator}")
        expression.left.accept(self)
        if expression.right is not None:
            expression.right.accept(self)

    @_make_indent
    def visit_multiplicative_expression(self, expression: MultiplicativeExpression):
        self._print(f"Operator: {expression.operator}")
        expression.left.accept(self)
        if expression.right is not None:
            expression.right.accept(self)

    @_make_indent
    def visit_negated_expression(self, expression: NegatedFactor):
        expression.accept(self)

    def visit_parameter(self, parameter: Parameter):
        self._print(f"{parameter.__class__.__name__}: {parameter.name}")

    @_make_indent
    def visit_block(self, block: Block):
        for stmt in block.statements:
            stmt.accept(self)

    @_make_indent
    def visit_return_statement(self, statement: ReturnStatement):
        if statement.expression is not None:
            statement.expression.accept(self)

    @_make_indent
    def visit_assignment(self, statement: Assignment):
        statement.expression.accept(self)

    @_make_indent
    def visit_var_definition(self, statement: VarDefinition):
        statement.expression.accept(self)

    @_make_indent
    def visit_conditional_statement(self, statement: ConditionalStatement):
        statement.condition.accept(self)
        statement.if_block.accept(self)
        if statement.else_block is not None:
            statement.else_block.accept(self)

    @_make_indent
    def visit_loop_statement(self, statement: LoopStatement):
        statement.condition.accept(self)
        statement.body.accept(self)

    def visit_data_type(self, statement: LiteralType):
        self._print(f"{statement.__class__.__name__}")

    def visit_case_identifier(self, identifier: CaseIdentifier):
        self._print(f"{identifier.__class__.__name__}")

    @_make_indent
    def visit_case_statement(self, statement: CaseStatement):
        statement.identifier.accept(self)
        self._accept_params(statement.params)
        statement.body.accept(self)

    @_make_indent
    def visit_case_default_statement(self, statement: CaseDefaultStatement):
        self._accept_params(statement.params)
        statement.body.accept(self)

    @_make_indent
    def visit_match_statement(self, statement: MatchStatement):
        self._accept_params(statement.params)
        for case_stmt in statement.case_stmts:
            case_stmt.accept(self)
        statement.default_stmt.accept(self)

    @_make_indent
    def visit_function_definition_statement(
        self, statement: FunctionDefinitionStatement
    ):
        self._print(statement.name)
        self._accept_params(statement.params)
        statement.body.accept(self)

    @_make_indent
    def visit_function_call_statement(self, statement: FunctionCallStatement):
        self._print(f"Function name: {statement.name}")
        self._accept_params(statement.arguments, "Arguments")
