from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeExp import TypeExp
from Classes.Env.AST import AST, ReturnAST
from Classes.Abstracts.Expression import Expression
from Classes.Env.Env import Env

class Logic(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, sign: str, exp2: Expression):
        super().__init__(line, column, TypeExp.NATIVE_FUNC)
        self.exp1 = exp1
        self.sign = sign
        self.exp2 = exp2

    def setField(self, field: dict[str, Field]) -> any:
        if self.exp1:
            self.exp1.setField(field)
        self.exp2.setField(field)

    def execute(self, env: Env) -> ReturnType:
        match self.sign.upper():
            case 'AND':
                return self.and_(env)
            case 'OR':
                return self.or_(env)
            case 'NOT':
                return self.not_(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def and_(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(value1.value and value2.value, self.type)

    def or_(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(value1.value or value2.value, self.type)

    def not_(self, env: Env) -> ReturnType:
        value: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(not value.value, self.type)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.sign}"];'
        value1: ReturnAST
        if self.exp1 != None:
            value1 = self.exp1.ast(ast)
            dot += '\n' + value1.dot
            dot += f'\nnode_{id} -> node_{value1.id};'
        value2: ReturnAST = self.exp2.ast(ast)
        dot += '\n' + value2.dot
        dot += f'\nnode_{id} -> node_{value2.id};'
        return ReturnType(dot, id)