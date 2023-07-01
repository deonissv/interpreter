from abc import ABC, abstractmethod

from interpreter.program import (
    Program,
    IdentifierExpression,
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
    VarDefinition,
    Parameter,
    Literal,
    LiteralType,
    ReturnStatement,
    OrExpression,
    AndExpression,
    RelationalExpression,
    NegatedFactor,
    MultiplicativeExpression,
    AdditiveExpression,
)
from interpreter.program.statement import ContinueStatement, BreakStatement


class Visitor(ABC):
    @abstractmethod
    def visit_program(self, program: Program):
        ...

    @abstractmethod
    def visit_identifier_expression(self, expression: IdentifierExpression):
        ...

    @abstractmethod
    def visit_literal(self, expression: Literal):
        ...

    @abstractmethod
    def visit_or_expression(self, expression: OrExpression):
        ...

    @abstractmethod
    def visit_and_expression(self, expression: AndExpression):
        ...

    @abstractmethod
    def visit_relational_expression(self, expression: RelationalExpression):
        ...

    @abstractmethod
    def visit_additive_expression(self, expression: AdditiveExpression):
        ...

    @abstractmethod
    def visit_multiplicative_expression(self, expression: MultiplicativeExpression):
        ...

    @abstractmethod
    def visit_negated_expression(self, expression: NegatedFactor):
        ...

    @abstractmethod
    def visit_parameter(self, parameter: Parameter):
        ...

    @abstractmethod
    def visit_block(self, statements: Block):
        ...

    @abstractmethod
    def visit_assignment(self, statement: Assignment):
        ...

    @abstractmethod
    def visit_conditional_statement(self, statement: ConditionalStatement):
        ...

    @abstractmethod
    def visit_loop_statement(self, statement: LoopStatement):
        ...

    @abstractmethod
    def visit_case_identifier(self, identifier: CaseIdentifier):
        ...

    @abstractmethod
    def visit_case_statement(self, statement: CaseStatement):
        ...

    @abstractmethod
    def visit_case_default_statement(self, statement: CaseDefaultStatement):
        ...

    @abstractmethod
    def visit_match_statement(self, statement: MatchStatement):
        ...

    @abstractmethod
    def visit_function_definition_statement(
        self, statement: FunctionDefinitionStatement
    ):
        ...

    @abstractmethod
    def visit_function_call_statement(self, statement: FunctionCallStatement):
        ...

    @abstractmethod
    def visit_return_statement(self, statement: ReturnStatement):
        ...

    @abstractmethod
    def visit_var_definition(self, statement: VarDefinition):
        ...

    @abstractmethod
    def visit_data_type(self, statement: LiteralType):
        ...

    @abstractmethod
    def visit_continue_statement(self, statement: ContinueStatement):
        ...

    @abstractmethod
    def visit_break_statement(self, statement: BreakStatement):
        ...
