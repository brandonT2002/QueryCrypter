from Classes.Abstracts.Expression import Expression
from Classes.Abstracts.Instruction import Instruction
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Utils.Type import ReturnType
from Classes.Utils.TypeInst import TypeInst

class If(Instruction):
    def __init__(self, line: int, column: int, condition: Expression, block: Instruction, except_: Instruction):
        super().__init__(line, column, TypeInst.IF)
        self.condition = condition
        self.block = block
        self.except_ = except_

    def execute(self, env: Env) -> any:
        condition: ReturnType = self.condition.execute(env)
        if condition.value: # if (condicion)
            block: ReturnType = self.block.execute(env) # instrucciones
            if block:
                return block
            return
        # else
        if self.except_:
            except_: ReturnType = self.except_.execute(env)
            if except_:
                return except_
        return

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="IF"];'
        cond: ReturnAST = self.condition.ast(ast)
        dot += '\n' + cond.dot
        inst: ReturnAST = self.block.ast(ast)
        dot += '\n' + inst.dot
        dot += f'\nnode_{id}_cnd[label="CONDICION"];'
        dot += f'\nnode_{id} -> node_{id}_cnd;'
        dot += f'\nnode_{id}_cnd -> node_{cond.id};'
        dot += f'\nnode_{id} -> node_{inst.id};'
        if self.except_:
            except_: ReturnAST = self.except_.ast(ast)
            dot += f'\nnode_{id}_else[label="ELSE"];'
            dot += f'\nnode_{id} -> node_{id}_else;'
            dot += f'\n' + except_.dot
            dot += f'\nnode_{id}_else -> node_{except_.id};'
        return ReturnAST(dot, id)