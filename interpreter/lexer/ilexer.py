from abc import ABC, abstractmethod
from typing import Optional

from interpreter.token import Token


class ILexer(ABC):
    @abstractmethod
    def next_token(self) -> Optional[Token]:
        ...
