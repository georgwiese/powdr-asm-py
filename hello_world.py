from powdr import WitnessColumn, FixedColumn

import std
import memory
from powdr_asm_parser import parse_assembly
from processor_utils import AbstractProcessor, instruction


class RiscVProcessor(AbstractProcessor):
    pc = WitnessColumn("PC")
    registers = ["A", "B"]
    machines = [memory.memory]

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
    def mstore(addr, value):
        step = FixedColumn("STEP", "i")
        yield from memory.mstore(step, addr, value)

    @instruction(outputs=("value",))
    def mload(addr, value):
        step = FixedColumn("STEP", "i")
        yield from memory.mload(step, addr, value)

    @instruction(name="return")
    def _return(cls):
        yield cls.pc.n == cls.pc

program = """
    A <== A + 3;
    A <== decr(A);
    branch_if_zero(A-2, 1);
    A <== incr(A + 3);
    A <== decr(A);
    mstore(3, 4);
    A <== mload(3);
    A, B <== funky(A+3, B-4);
    return;
"""

RiscVProcessor.run(parse_assembly(program), num_steps=2**16)
