from abc import ABC, abstractmethod
from Classes.Utils.TypeInst import TypeInst
from Classes.Env.Env import Env
from Classes.Env.AST import AST, ReturnAST

class Instruction(ABC):
    def __init__(self, line: int, column: int, typeInst: TypeInst):
        self.line = line
        self.column = column
        self.typeInst = typeInst

    @abstractmethod
    def execute(self, env: Env) -> any:
        pass

    @abstractmethod
    def ast(self, ast: AST) -> ReturnAST:
        pass