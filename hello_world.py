from powdr import WitnessColumn, run, PIL, FixedColumn

import std
import memory
from asm_to_pil import transform_vm, Statement
from processor_utils import AbstractProcessor, instruction


assignment_registers = ["IN_0", "IN_1", "IN_2", "IN_3", "OUT_0", "OUT_1", "OUT_2", "OUT_3"]


class RiscVProcessor(AbstractProcessor):
    pc = WitnessColumn("PC")
    registers = ["A", "B"]

    @instruction
    def incr(x):
        # 1 output witness column
        return x + 1

    @instruction
    def funky(x, y):
        # 2 output witness columns
        return x + 1, y + 2

    @instruction
    def decr(x):
        return x - 1

    @instruction
    def assert_zero(x):
        yield x == 0

    @instruction
    def branch_if_zero(cls, x, y):
        x_is_zero = yield from std.is_zero(x)
        yield cls.pc.n == x_is_zero * y + (1 - x_is_zero) * (cls.pc + 1)

    @instruction
    def mload(x, y, num_steps: int):
        step = FixedColumn("STEP", values=list(range(num_steps)))
        yield from memory.mload(x=x, step=step, y=y)

    @instruction(name="return")
    def _return(cls):
        yield cls.pc.n == cls.pc

    @classmethod
    def run(cls, program: list, num_steps: int = 1024) -> PIL:
        instructions = cls.get_instructions(num_steps = num_steps)
        pil_generator = lambda: transform_vm(cls.registers, assignment_registers, instructions, program)
        run(pil_generator, num_steps, "bn254", powdr_cmd=["pixi", "run", "powdr"])

#     function main {
#         A <=X= A + 3;
#         A <== decr(A);
#         branch_if_zero(A-2, 1)
#         A <== incr(A + 3);
#         A <== decr(A);
#         A, B <== funky(A+3, B-4)
#         return;
#     }

program = [
    Statement("IN_0", [[("A", 1), ("CONST", 3)]], ["A"]),
    Statement("decr", [[("A", 1)]], ["A"]),
    Statement("branch_if_zero", [[("A", 1), ("CONST", -2)], [("CONST", 1)]], []),
    Statement("incr", [[("A", 1), ("CONST", 3)]], ["A"]),
    Statement("decr", [[("A", 1)]], ["A"]),
    Statement("funky", [[("A", 1), ("CONST", 3)], [("B", 1), ("CONST", 5)]], ["A", "B"]),
    Statement("return", [], [])
]

RiscVProcessor.run(program)
