from Classes.Env.AST import AST, ReturnAST
from Classes.Abstracts.Instruction import Instruction
from Classes.Abstracts.Expression import Expression
from Classes.Utils.TypeInst import TypeInst
from Classes.Env.Env import Env

class Print(Instruction):
    def __init__(self, line: int, column: int, expression: Expression):
        super().__init__(line, column, TypeInst.PRINT)
        self.expression = expression

    def execute(self, env: Env) -> any:
        value = self.expression.execute(env)
        env.setPrint(value.value)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="PRINT"];'
        value: ReturnAST = self.expression.ast(ast)
        dot += '\n' + value.dot
        dot += f'\nnode_{id} -> node_{value.id};'
        return ReturnAST(dot, id)