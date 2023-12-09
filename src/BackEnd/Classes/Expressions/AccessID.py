from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Abstracts.Expression import Expression
from Classes.Env.Symbol import Symbol
from Classes.Utils.TypeExp import TypeExp

class AccessID(Expression):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeExp.ACCESS_ID)
        self.id = id

    def setField(self, _: dict[str, Field]):
        pass

    def execute(self, env: Env) -> ReturnType:
        value: Symbol | None = env.getValue(self.id)
        if value:
            return ReturnType(value.value, value.type)
        return ReturnType('NULL', Type.NULL)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.id}"];'
        return ReturnAST(dot, id)