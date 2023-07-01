from abc import ABC, abstractmethod

from interpreter.interpreter.builtins.input import Input
from interpreter.interpreter.builtins.str import ToStr
from interpreter.interpreter.builtins.print import Print

BUILTINS = [Print, ToStr, Input]


class Builtins(ABC):
    @abstractmethod
    def visit_print(self, fn: Print):
        ...

    @abstractmethod
    def visit_to_str(self, fn: ToStr):
        ...

    @abstractmethod
    def visit_input(self, fn: Input):
        ...
