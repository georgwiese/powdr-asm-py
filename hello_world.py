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
assignment_registers = ["X", "Y"]

instr_incr = Instruction("incr", ["X"], ["Y"], [WitnessColumn("Y") == WitnessColumn("X") + 1])
instr_decr = Instruction("decr", ["X"], ["Y"], [WitnessColumn("Y") == WitnessColumn("X") - 1])
instr_assert_zero = Instruction("assert_zero", ["X"], [], [WitnessColumn("X") == 0])
instr_return = Instruction("return", [], [], [WitnessColumn("PC").n == WitnessColumn("PC")])

instructions = [instr_incr, instr_decr, instr_assert_zero, instr_return]

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
