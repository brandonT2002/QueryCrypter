from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeExp import TypeExp
from Classes.Env.AST import AST, ReturnAST
from Classes.Abstracts.Expression import Expression
from Classes.Env.Env import Env

class Len(Expression):
    def __init__(self, line: int, column: int, exp: Expression):
        super().__init__(line, column, TypeExp.NATIVE_FUNC)
        self.exp = exp

    def setField(self, _: dict[str, Field]) -> any:
        pass
    
    def execute(self, env: Env) -> ReturnType:
        value: ReturnType = self.exp.execute(env)
        if value.type == Type.VARCHAR:
            return ReturnType(len(value.value), Type.INT)
        return ReturnType('NULL', Type.NULL)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="LEN"];'
        value1: ReturnAST = self.exp.ast(ast)
        dot += '\n' + value1.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)