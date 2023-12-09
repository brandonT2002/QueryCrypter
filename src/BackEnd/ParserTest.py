from Language.Parser import *
from Classes.Abstracts.Expression import Expression
from Classes.Abstracts.Instruction import Instruction
from Classes.Env.Env import Env
from Classes.Utils.Outs import getStringOuts
from Classes.Utils.TypeExp import TypeExp
from Classes.Utils.TypeInst import TypeInst

input = open('../../Inputs/Pruebas.sql', encoding='utf-8').read()
Scanner.lineno = 1
instructions: list[Instruction] = parser.parse(input)

globalEnv: Env = Env(None, 'Global')

for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst == TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
    except ValueError as e: pass

for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst != TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
        elif isinstance(instruction, Expression) and instruction.typeExp == TypeExp.CALL_FUNC:
            instruction.execute(globalEnv)
    except ValueError as e: print(e)

print(getStringOuts())