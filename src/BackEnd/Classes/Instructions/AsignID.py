from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Abstracts.Instruction import Instruction
from Classes.Abstracts.Expression import Expression
from Classes.Utils.TypeInst import TypeInst

class AsignID(Instruction):
    def __init__(self, line: int, column: int, id: str, value: Expression):
        super().__init__(line, column, TypeInst.ASIGN_ID)
        self.id = id
        self.value = value

    def execute(self, env: Env):
        value = self.value.execute(env)
        env.reasignID(self.id, value, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SET"];'
        value1: ReturnAST = self.value.ast(ast)
        dot += f'\nnode_{id}_id[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_id'
        dot += '\n' + value1.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)