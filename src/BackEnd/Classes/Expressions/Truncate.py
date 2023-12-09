from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeExp import TypeExp
from Classes.Env.AST import AST, ReturnAST
from Classes.Abstracts.Expression import Expression
from Classes.Env.Env import Env

class Truncate(Expression):
    def __init__(self, line: int, column: int, exp: Expression, truncate: Expression):
        super().__init__(line, column, TypeExp.NATIVE_FUNC)
        self.exp = exp
        self.truncate = truncate

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, env: Env) -> ReturnType:
        value_: str
        value: ReturnType = self.exp.execute(env)
        trunc: ReturnType = self.truncate.execute(env)
        if value.type == Type.DOUBLE:
            value_ = str(value.value)
            return ReturnType(self.truncateDigit(value_, trunc.value), Type.DOUBLE)

    def truncateDigit(self, value: str, trunc: int):
        parts = value.split('.')
        if len(parts) == 2:
            integer_ = parts[0]
            decimal_ = parts[1][:trunc]
            return f"{integer_}.{decimal_}" if len(decimal_) > 0 else integer_
        return value

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="TRUNCATE"];'
        value1: ReturnAST = self.exp.ast(ast)
        dot += '\n' + value1.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)