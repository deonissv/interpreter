from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from interpreter.position import Position
from interpreter.visitor.visitable import Visitable


@dataclass()
class Statement(Visitable, ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        visitor.visit_statement(self)


@dataclass
class Parameter(Statement):
    name: str
    mut: bool = False

    def accept(self, visitor: "Visitor"):
        visitor.visit_parameter(self)


@dataclass
class Block(Statement):
    statements: List[Statement]

    def accept(self, visitor: "Visitor"):
        visitor.visit_block(self)


@dataclass
class VarDefinition(Statement):
    name: str
    expression: "Expression"
    position: Position
    mut: bool = False

    def accept(self, visitor: "Visitor"):
        visitor.visit_var_definition(self)


@dataclass
class Assignment(Statement):
    name: str
    expression: "Expression"
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_assignment(self)


@dataclass
class ConditionalStatement(Statement):
    condition: "Expression"
    if_block: Block
    else_block: Block = None

    def accept(self, visitor: "Visitor"):
        visitor.visit_conditional_statement(self)


@dataclass
class LoopStatement(Statement):
    condition: "Expression"
    body: Block

    def accept(self, visitor: "Visitor"):
        visitor.visit_loop_statement(self)


@dataclass
class CaseStatement(Statement):
    identifier: "CaseIdentifier"
    params: List[Parameter]
    body: Block

    def accept(self, visitor: "Visitor"):
        visitor.visit_case_statement(self)


@dataclass
class CaseDefaultStatement(Statement):
    params: List[Parameter]
    body: Block

    def accept(self, visitor: "Visitor"):
        visitor.visit_case_default_statement(self)


@dataclass
class MatchStatement(Statement):
    args: List["Expression"]
    case_stmts: List[CaseStatement]
    default_stmt: CaseDefaultStatement
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_match_statement(self)


@dataclass
class FunctionDefinitionStatement(Statement):
    name: str
    params: List[Parameter]
    body: Block

    def accept(self, visitor: "Visitor"):
        visitor.visit_function_definition_statement(self)


@dataclass
class FunctionCallStatement(Statement):
    name: str
    arguments: List["Expression"]
    position: Position
    r_position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_function_call_statement(self)


@dataclass
class ReturnStatement(Statement):
    expression: "Expression" = None

    def accept(self, visitor: "Visitor"):
        visitor.visit_return_statement(self)


@dataclass
class ContinueStatement(Statement):
    def accept(self, visitor: "Visitor"):
        visitor.visit_continue_statement(self)


@dataclass
class BreakStatement(Statement):
    def accept(self, visitor: "Visitor"):
        visitor.visit_break_statement(self)
