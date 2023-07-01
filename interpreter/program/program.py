from dataclasses import dataclass
from typing import List

from interpreter.program.statement import Statement
from interpreter.visitor.visitable import Visitable


@dataclass
class Program(Visitable):
    statements: List[Statement]

    def accept(self, visitor: "Visitor"):
        visitor.visit_program(self)
