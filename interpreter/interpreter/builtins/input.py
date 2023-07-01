from interpreter.interpreter.function import Function
from interpreter.program import Block


class Input(Function):
    def __init__(self):
        super().__init__("input", [], Block([]), 0)

    def accept(self, visitor: "Visitor"):
        visitor.visit_input(self)
