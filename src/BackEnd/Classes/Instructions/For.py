from Classes.Abstracts.Expression import Expression
from Classes.Abstracts.Instruction import Instruction
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Utils.Type import ReturnType, Type
from Classes.Utils.TypeInst import TypeInst

class For(Instruction):
    def __init__(self, line: int, column: int, iterator: str, limInf: Expression, limSup: Expression, block: Instruction):
        super().__init__(line, column, TypeInst.LOOP_FOR)
        self.iterator = iterator
        self.limInf = limInf
        self.limSup = limSup
        self.block = block

    def execute(self, env: Env) -> any:
        envFor: Env = Env(env, f'{env.name} for')
        limInf: ReturnType = self.limInf.execute(env)
        if limInf.type != Type.INT:
            env.setError("Tipo inválido para rango", self.line, self.column)
            return
        limSup: ReturnType = self.limSup.execute(env)
        if limSup.type != Type.INT:
            env.setError("Tipo inválido para rango", self.line, self.column)
            return
        block: ReturnType
        if env.getValue(self.iterator):
            for i in range(limInf.value, limSup.value + 1):
                envFor.reasignID(self.iterator, ReturnType(i, Type.INT), self.line, self.column)
                block = self.block.execute(envFor)
                if block:
                    if block.value == TypeInst.CONTINUE:
                        continue
                    if block.value == TypeInst.BREAK:
                        break
                    return block
            return
        env.setError("Iterador sin declarar", self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="FOR"];'
        dot += f'\nnode_{id}_lim[label="RANGE"]'
        limInf: ReturnAST = self.limInf.ast(ast)
        limSup: ReturnAST = self.limSup.ast(ast)
        dot += '\n' + limInf.dot
        dot += '\n' + limSup.dot
        dot += f'\nnode_{id}_lim -> node_{limInf.id};'
        dot += f'\nnode_{id}_lim -> node_{limSup.id};'
        inst: ReturnAST = self.block.ast(ast)
        dot += '\n' + inst.dot
        dot += f'\nnode_{id} -> node_{inst.id};'
        dot += f'\nnode_{id} -> node_{id}_lim;'
        return ReturnAST(dot, id)