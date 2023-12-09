from Classes.Abstracts.Expression import Expression
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Objects.Table import Field
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeExp import TypeExp
from Classes.Utils.DomineOp import plus, minus, mult, div, mod

class Arithmetic(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, sign: str, exp2: Expression):
        super().__init__(line, column, TypeExp.ARITHMETIC_OP)
        self.exp1 = exp1
        self.sign = sign
        self.exp2 = exp2
        self.type: Type = Type.NULL

    def setField(self, field: dict[str, Field]) -> any:
        if self.exp1:
            self.exp1.setField(field)
        self.exp2.setField(field)

    def execute(self, env: Env) -> ReturnType:
        match self.sign:
            case '+':
                return self.plus(env)
            case '-':
                if self.exp1 != None:
                    return self.minus(env)
                return self.negative(env)
            case '*':
                return self.mult(env)
            case '/':
                return self.div(env)
            case '%':
                return self.mod(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def plus(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = plus[value1.type.value][value2.type.value]
        if self.type != Type.NULL:
            if self.type == Type.INT:
                return ReturnType(int(int(value1.value) + int(value2.value)), self.type)
            elif self.type == Type.DOUBLE:
                return ReturnType(float(value1.value) + float(value2.value), self.type)
            elif self.type == Type.VARCHAR:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def minus(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = minus[value1.type.value][value2.type.value]
        if self.type != Type.NULL:
            if self.type == Type.INT:
                return ReturnType(int(value1.value) - int(value2.value), self.type)
            elif self.type == Type.DOUBLE:
                return ReturnType(float(value1.value) - float(value2.value), self.type)
            elif self.type == Type.VARCHAR:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def negative(self, env: Env) -> ReturnType:
        value: ReturnType = self.exp2.execute(env)
        self.type = value.type
        if self.type == Type.INT or self.type == Type.DOUBLE:
            return ReturnType(-value.value, self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def mult(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = mult[value1.type.value][value2.type.value]
        if self.type == Type.INT:
            return ReturnType(int(value1.value) * int(value2.value), self.type)
        if self.type == Type.DOUBLE:
            return ReturnType(float(value1.value) * float(value2.value), self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def div(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = div[value1.type.value][value2.type.value]
        if self.type == Type.INT:
            return ReturnType(int(float(value1.value) / float(value2.value)), self.type)
        if self.type == Type.DOUBLE:
            return ReturnType(float(value1.value) / float(value2.value), self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def mod(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = mod[value1.type.value][value2.type.value]
        if self.type == Type.INT:
            return ReturnType(int(float(value1.value) % float(value2.value)), self.type)
        if self.type == Type.DOUBLE:
            return ReturnType(float(value1.value) % float(value2.value), self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

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
        return ReturnAST(dot, id)