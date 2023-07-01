from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from interpreter.position import Position
from interpreter.program.operator import (
    RelationalOperator,
    MultiplicativeOperator,
    AdditiveOperator,
    UnaryOperator,
    CaseOperator,
)
from interpreter.program.statement import Statement
from interpreter.token import Token, TokenType


class LiteralType(Enum):
    NUM = (auto(),)
    STR = (auto(),)
    BOOL = (auto(),)
    NULL = (auto(),)

    @staticmethod
    def from_token(token: Token):
        match token.token_type:
            case TokenType.NUM_TYPE:
                return LiteralType.NUM
            case TokenType.STR_TYPE:
                return LiteralType.STR
            case TokenType.BOOL_TYPE:
                return LiteralType.BOOL

    def __str__(self) -> str:
        match self:
            case LiteralType.STR:
                return "str"
            case LiteralType.BOOL:
                return "bool"
            case LiteralType.NUM:
                return "num"
            case LiteralType.NULL:
                return "null"


class Expression(Statement, ABC):
    ...


@dataclass
class Literal(Expression):
    type: LiteralType
    value: int | float | str | bool | None
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_literal(self)

    def __copy__(self) -> "Literal":
        return Literal(self.type, self.value, self.position)


@dataclass
class OrExpression(Expression):
    left: Expression
    right: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_or_expression(self)


@dataclass
class AndExpression(Expression):
    left: Expression
    right: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_and_expression(self)


@dataclass
class RelationalExpression(Expression):
    operator: RelationalOperator
    left: Expression
    right: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_relational_expression(self)


@dataclass
class AdditiveExpression(Expression):
    operator: AdditiveOperator
    left: Expression
    right: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_additive_expression(self)


@dataclass
class MultiplicativeExpression(Expression):
    operator: MultiplicativeOperator
    left: Expression
    right: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_multiplicative_expression(self)


@dataclass
class NegatedFactor(Expression):
    operator: UnaryOperator
    factor: Expression
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_negated_expression(self)


@dataclass
class IdentifierExpression(Expression):
    name: str
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_identifier_expression(self)


@dataclass
class CaseIdentifier(Expression):
    identifier: CaseOperator | Literal | LiteralType
    position: Position

    def accept(self, visitor: "Visitor"):
        visitor.visit_case_identifier(self)
