from Classes.Abstracts.Instruction import Instruction
from Classes.Env.AST import AST, ReturnAST
from Classes.Env.Env import Env
from Classes.Utils.TypeInst import TypeInst

class Block(Instruction):
    def __init__(self, line: int, column: int, instructions: list[Instruction]):
        super().__init__(line, column, TypeInst.BLOCK_INST)
        self.instructions = instructions

    def execute(self, env: Env) -> any:
        newEnv: Env = Env(env, env.name)
        for instruction in self.instructions:
            try:
                ret = instruction.execute(newEnv)
                if ret:
                    return ret
            except: {}

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="BEGIN-END"];'
        value1: ReturnAST
        for i in range(len(self.instructions)):
            value1 = self.instructions[i].ast(ast)
            dot += '\n' + value1.dot
            dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)