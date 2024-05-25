from powdr import WitnessColumn, FixedColumn

import std
import memory
from powdr_asm_parser import parse_assembly
from processor_utils import AbstractProcessor, instruction


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

program = """
    A <== A + 3;
    A <== decr(A);
    branch_if_zero(A-2, 1);
    A <== incr(A + 3);
    A <== decr(A);
    A, B <== funky(A+3, B-4);
    return;
"""

RiscVProcessor.run(parse_assembly(program))
