from typing import List

from interpreter.program import Block
from dataclasses import dataclass


@dataclass()
class Param:
    name: str
    mut: bool


@dataclass
class Function:
    name: str
    params: List[Param]
    params_len: int
    body: Block

    def __init__(
        self, name: str, params: List["Parameter"], body: Block, param_len: int = None
    ):
        self.name = name
        self.params = params
        self.params_len = param_len if param_len else len(params)
        self.body = body
