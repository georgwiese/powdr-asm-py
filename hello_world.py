from powdr import WitnessColumn, run, PIL
from asm_to_pil import transform_vm, Instruction, Statement

from processor_utils import AbstractProcessor, instruction


# machine HelloWorld with degree: 16 {
#     reg pc[@pc];
#     reg X[<=];
#     reg Y[<=];
#     reg A;
#     instr incr X -> Y {
#         Y = X + 1
#     }
#     instr decr X -> Y {
#         Y = X - 1
#     }
#     instr assert_zero X {
#         X = 0
#     }
#     // TODO: Auto-generate this instruction
#     instr _return {
#         pc' = pc
#     }
#     function main {
#         A <=X= A + 3;
#         A <== incr(A + 3);
#         A <== decr(A);
#         // TODO: Auto-generate this statement
#         _return;
#     }
# }


registers = ["A"]
assignment_registers = ["X", "Y", "OUT_0", "OUT_1", "OUT_2", "OUT_3"]


class Input(WitnessColumn):
    pass


class Output(WitnessColumn):
    pass


class RiscVProcessor(AbstractProcessor):
    pc = WitnessColumn("PC")

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

    @instruction(name="return")
    def _return(cls):
        yield cls.pc.n == cls.pc



instructions = RiscVProcessor.get_instructions()

#     function main {
#         A <=X= A + 3;
#         A <== incr(A + 3);
#         A <== decr(A);
#         return;
#     }

program = [
    Statement("X", [[("A", 1), ("CONST", 3)]], ["A"]),
    Statement("incr", [[("A", 1), ("CONST", 3)]], ["A"]),
    Statement("decr", [[("A", 1)]], ["A"]),
    Statement("return", [], [])
]


def hello_world() -> PIL:
    return transform_vm(registers, assignment_registers, instructions, program)

run(hello_world, 1024, "bn254", powdr_cmd=["pixi", "run", "powdr"])
# print(generate_pil(lambda: transform_vm(registers, assignment_registers, instructions, program), 1024))
