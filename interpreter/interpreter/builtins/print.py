from interpreter.interpreter.function import Function
from interpreter.program import Block, Parameter


class Print(Function):
    def __init__(self):
        super().__init__("print", [Parameter("arg", False)], Block([]), 1)

    def accept(self, visitor: "Visitor"):
        visitor.visit_print(self)
