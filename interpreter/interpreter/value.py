from dataclasses import dataclass
from enum import Enum, auto

from interpreter.program import Literal, LiteralType


class DataType(Enum):
    NUM = (auto(),)
    STR = (auto(),)
    BOOL = (auto(),)
    NULL = (auto(),)

    @staticmethod
    def from_literal_type(literal_type: LiteralType):
        match literal_type:
            case LiteralType.NUM:
                return DataType.NUM
            case LiteralType.STR:
                return DataType.STR
            case LiteralType.BOOL:
                return DataType.BOOL
            case LiteralType.NULL:
                return DataType.NULL

    def __str__(self) -> str:
        match self:
            case DataType.STR:
                return "str"
            case DataType.BOOL:
                return "bool"
            case DataType.NUM:
                return "num"
            case DataType.NULL:
                return "null"


@dataclass
class Value:
    type: DataType
    value: str | int | float | bool | None

    @staticmethod
    def from_literal(literal: Literal) -> "Value":
        data_type = DataType.from_literal_type(literal.type)
        return Value(data_type, literal.value)
