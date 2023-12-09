from Classes.Abstracts.Expression import Expression
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeExp import TypeExp

class Primitive(Expression):
    def __init__(self, line: int, column: int, value: any, type: Type):
        super().__init__(line, column, TypeExp.PRIMITIVE)
        self.value = value
        self.type = type

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, _: Env) -> ReturnType:
        match self.type:
            case Type.INT:
                return ReturnType(int(self.value), self.type)
            case Type.DOUBLE:
                return ReturnType(float(self.value), self.type)
            case Type.BOOLEAN:
                return ReturnType(str(self.value).lower() == 'true', self.type)
            case Type.DATE:
                return ReturnType(str(self.value), self.type)
            case _:
                self.value = self.value.replace('\\n', '\n')
                self.value = self.value.replace('\\t', '\t')
                self.value = self.value.replace('\\"', '\"')
                self.value = self.value.replace("\\'", '\'')
                self.value = self.value.replace('\\\\', '\\')
                return ReturnType(self.value, self.type)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.value}"];'
        return ReturnAST(dot, id)