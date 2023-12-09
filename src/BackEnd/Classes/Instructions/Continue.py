from Classes.Abstracts.Instruction import Instruction
from Classes.Env.Env import Env
from Classes.Utils.TypeInst import TypeInst
from Classes.Utils.Type import ReturnType, Type
from Classes.Env.AST import AST, ReturnAST

class Continue(Instruction):
    def __init__(self, line: int, column: int):
        super().__init__(line, column, TypeInst.CONTINUE)

    def execute(self, _: Env) -> ReturnType:
        return ReturnType(self.typeInst, Type.NULL)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="CONTINUE"];'
        return ReturnAST(dot, id)