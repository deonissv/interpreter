from dataclasses import dataclass

from interpreter.interpreter.value import Value


@dataclass
class Var:
    name: str
    value: Value
    mutable: bool
