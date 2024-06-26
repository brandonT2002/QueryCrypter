from Classes.Abstracts.Instruction import Instruction
from Classes.Abstracts.Expression import Expression
from Classes.Utils.TypeInst import TypeInst
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env

class UpdateTable(Instruction):
    def __init__(self, line: int, column: int, id: str, fields: list[str], values: list[Expression], condition: Expression):
        super().__init__(line, column, TypeInst.UPDATE_TABLE)
        self.id = id
        self.fields = fields
        self.values = values
        self.condition = condition

    def execute(self, env: Env) -> any:
        env.updateTable(self.id, self.fields, self.values, self.condition, self.line, self.column)
        return

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="UPDATE"];'
        dot += f'\nnode_{id}_set[label="SET"];'
        dot += f'\nnode_{id} -> node_{id}_set;'
        dot += f'\nnode_{id}_condition[label="CONDITION"];'
        dot += f'\nnode_{id} -> node_{id}_condition;'
        value: ReturnAST
        for i in range(len(self.fields)):
            dot += f'\nnode_{id}_field${i}[label="{self.fields[i]}"]'
            dot += f'\nnode_{id}_set -> node_{id}_field{i};'
            value = self.values[i].ast(ast)
            dot += f'\n${value.dot}'
            dot += f'\nnode_{id}_field{i} -> node_{value.id};'
        condition = self.condition.ast(ast)
        dot += f'\n{condition.dot}'
        dot += f'\nnode_{id}_condition -> node_{condition.id};'
        return ReturnAST(dot, id)