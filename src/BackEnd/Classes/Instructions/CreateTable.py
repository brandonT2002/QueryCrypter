from Classes.Abstracts.Instruction import Instruction
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Objects.Table import Table
from Classes.Utils.Type import Type
from Classes.Utils.TypeInst import TypeInst

class CreateTable(Instruction):
    def __init__(self, line: int, column: int, name: str, nameFields: list[str], typeFields: list[Type]):
        super().__init__(line, column, TypeInst.CREATE_TABLE)
        self.name = name
        self.nameFields = nameFields
        self.typeFields = typeFields

    def execute(self, env: Env) -> any:
        table = Table(self.name.lower(), self.nameFields, self.typeFields)
        env.saveTable(self.name, table, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="TABLE"];'
        dot += f'\nnode_{id}_name[label="{self.name}"]'
        dot += f'\nnode_{id}_fields[label="CAMPOS"]'
        for i in range(len(self.nameFields)):
            dot += f'\nnode_{id}_field_{i}[label={self.nameFields[i]}]'
            dot += f'\nnode_{id}_fields -> node_{id}_field_{i};'
        dot += f'\nnode_{id} -> node_{id}_name;'
        dot += f'\nnode_{id} -> node_{id}_fields;'
        return ReturnAST(dot, id)