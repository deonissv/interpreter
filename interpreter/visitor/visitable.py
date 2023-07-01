from abc import ABC, abstractmethod


class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        ...
