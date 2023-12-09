from Classes.Abstracts.Instruction import Instruction
from Classes.Abstracts.Expression import Expression
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Expressions.Primitive import Primitive
from Classes.Utils.TypeInst import TypeInst
from Classes.Utils.Type import Type

class Select(Instruction):
    def __init__(self, line: int, column: int, id: str, fields: list[list[any]] or str, condition: Expression):
        super().__init__(line, column, TypeInst.SELECT)
        self.id = id
        self.fields = fields
        self.condition = condition

    def execute(self, env: Env) -> any:
        self.condition = self.condition if self.condition else Primitive(self.line, self.column, 'true', Type.BOOLEAN)
        env.selectTable(self.id, self.fields, self.condition, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SELECT"];'
        dot += f'\nnode_{id}_id[label="{self.id}"];'
        dot += f'\nnode_{id} -> node_{id}_id;'
        dot += f'\nnode_{id}_fields[label="FIELDS"];'
        dot += f'\nnode_{id}_id -> node_{id}_fields;'
        dot += f'\nnode_{id}_condition[label="CONDITION"];'
        dot += f'\nnode_{id}_id -> node_{id}_condition;'
        if type(self.fields) == str:
            dot += f'\nnode_{id}_star[label="*"];'
            dot += f'\nnode_{id}_fields -> node_{id}_star;'
        else:
            value: ReturnAST
            for i in range(len(self.fields)):
                value = self.fields[i][0].ast(ast)
                if self.fields[i][1] != '':
                    dot += f'\nnode_{id}_AS${i}[label="AS"];'
                    dot += f'\nnode_{id}_fields -> node_{id}_AS{i};'
                    dot += f'\n{value.dot};'
                    dot += f'\nnode_{id}_AS{i} -> node_{value.id};'
                    dot += f'\nnode_{id}_ASTXT{i}[label="{self.fields[i][1]}"];'
                    dot += f'\nnode_{id}_AS{i} -> node_{id}_ASTXT{i};'
                else:
                    dot += f'\n{value.dot}'
                    dot += f'\nnode_{id}_fields -> node_{value.id};'
        if self.condition:
            condition = self.condition.ast(ast)
            dot += f'\n{condition.dot}'
            dot += f'\nnode_{id}_condition -> node_{condition.id};'
        return ReturnAST(dot, id)