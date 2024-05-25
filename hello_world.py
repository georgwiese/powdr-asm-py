from powdr import WitnessColumn, FixedColumn

import std
import memory
from powdr_asm_parser import parse_assembly
from processor_utils import AbstractProcessor, instruction


class RiscVProcessor(AbstractProcessor):
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

program = """
    // Writes some values to memory and then multiplies
    // all nonzero values up to cell 9.

    mstore(0, 2);
    mstore(7, 4);
    mstore(17, 22);
    
    // A stores the current index
    A <== 0;
    // B stores the product
    B <== 1;

    branch_if_zero(A - 10, 11);
    C <== mload(A);
    branch_if_zero(C, 9);
    B <== mul(B, C);
    A <== A + 1;
    jump(5);

    // The result should be 8
    assert_zero(B - 8);

    return;
"""

RiscVProcessor.run(parse_assembly(program), num_steps=2**16)
