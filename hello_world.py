from powdr import WitnessColumn, FixedColumn

import std
import memory
from processor_utils import AbstractProcessor, instruction


class HelloWorldProcessor(AbstractProcessor):
    pc = WitnessColumn("PC")
    registers = ["A", "B", "C"]
    machines = [memory.memory]

    @instruction
    def mul(cls, x, y):
        return x * y
    
    @instruction
    def assert_zero(x):
        yield x == 0

    @instruction
    def jump(cls, addr):
        yield cls.pc.n == addr
    
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

