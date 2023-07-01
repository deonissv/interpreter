from typing import Dict, Optional

from interpreter.interpreter.function import Function
from interpreter.interpreter.var import Var


class Scope:
    def __init__(self, *args: [Var | Function]):
        self.var: Dict[str, Var | Function] = {}
        for arg in args:
            self.var.update({arg.name: arg})

    def look_up(self, name: str) -> Optional[Var | Function]:
        return self.var.get(name)

    def update(self, var: Var | Function) -> None:
        self.var.update({var.name: var})
