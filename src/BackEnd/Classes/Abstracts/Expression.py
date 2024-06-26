from abc import ABC, abstractmethod
from Classes.Utils.TypeExp import TypeExp

class Expression(ABC):
    def __init__(self, line: int, column: int, typeExp: TypeExp):
        self.line = line
        self.column = column
        self.typeExp = typeExp

    @abstractmethod
    def setField(self, field):
        pass

    @abstractmethod
    def execute(self, env):
        pass

    @abstractmethod
    def ast(self, ast):
        pass