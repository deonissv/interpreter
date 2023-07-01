from interpreter.interpreter.function import Function
from interpreter.program import Block, Parameter


class ToStr(Function):
    def __init__(self):
        super().__init__("to_str", [Parameter("arg", False)], Block([]), 1)

    def accept(self, visitor: "Visitor"):
        visitor.visit_to_str(self)
