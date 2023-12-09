from Classes.Abstracts.Expression import Expression
from Classes.Abstracts.Instruction import Instruction
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Utils.TypeInst import TypeInst

class DeleteTable(Instruction):
    def __init__(self, line: int, column: int, id: str, condition: Expression):
        super().__init__(line, column, TypeInst.DELETE_TABLE)
        self.id = id
        self.condition = condition

    def execute(self, env: Env) -> any:
        if self.condition:
            env.deleteTable(self.id, self.condition, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="DELETE"];'
        dot += f'\nnode_{id}_tableName[label="{self.id}"];'
        dot += f'\nnode_{id} -> node_{id}_tableName;'
        condition = self.condition.ast(ast)
        dot += f'\n{condition.dot}'
        dot += f'\nnode_{id} -> node_{condition.id};'
        return ReturnAST(dot, id)