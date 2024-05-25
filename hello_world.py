from powdr import WitnessColumn, Identity, generate_pil, run, PIL
from asm_to_pil import transform_vm
from typing import Tuple
from typing import List, Tuple


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

# Instructions return inputs, outputs, and (conditional) constraints
def incr() -> Tuple[List[str], List[str], List[Identity]]:
    X = WitnessColumn("X")
    Y = WitnessColumn("Y")
    return (["X"], ["Y"], [Y == X + 1])

def decr() -> Tuple[List[str], List[str], List[Identity]]:
    X = WitnessColumn("X")
    Y = WitnessColumn("Y")
    return (["X"], ["Y"], [Y == X - 1])

def assert_zero() -> Tuple[List[str], List[str], List[Identity]]:
    X = WitnessColumn("X")
    return (["X"], [], [X == 0])

def _return() -> Tuple[List[str], List[str], List[Identity]]:
    PC = WitnessColumn("PC")
    return ([], [], [PC.n == PC])

instructions = [incr, decr, assert_zero, _return]

#     function main {
#         A <=X= A + 3;
#         A <== incr(A + 3);
#         A <== decr(A);
#         return;
#     }

program = [
    {
        # One input for assignments, otherwise the number of inputs
        # should match the number of inputs to the instruction.
        # Each input is a list of (<register name>, <factor>) tuples.
        # A special "register" "CONST" is part of the program.
        # For example, this input corresponds to: A * 1 + 3.
        "inputs": [[("A", 1), ("CONST", 3)]],
        # If the instruction name is the name of an assignment register,
        # it means that this row is an assignment via that register.
        "instruction": "X",
        # Register names
        "outputs": ["A"]
    },
    {
        "inputs": [[("A", 1), ("CONST", 3)]],
        "instruction": "incr",
        "outputs": ["A"]
    },
    {
        "inputs": [[("A", 1)]],
        "instruction": "decr",
        "outputs": ["A"]
    },
    {
        "inputs": [],
        "instruction": "_return",
        "outputs": []
    }
]


def hello_world() -> PIL:
    return transform_vm(registers, assignment_registers, instructions, program)

run(hello_world, 1024, "bn254")